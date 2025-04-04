import pandas as pd
import numpy as np
import re
import statsmodels.formula.api as smf
from scipy.stats import chi2_contingency

def calculate_odds_ratio(data, variable, target_feature='target', threshold=0, drop9=False):
    """
    Kategorik değişkenin, binary target ile ilişkisine göre odds ratio hesaplar,
    her unique kategori için (referans dahil) 2x2 chi-square testi yapar ve
    frekans bilgisini "x% (n=y)" formatında tek sütunda gösterir.
    
    Parameters:
    -----------
    data : pandas.DataFrame
        Analiz edilecek verileri içeren DataFrame.
    variable : str
        İncelenecek kategorik değişkenin adı.
    target_feature : str, default='target'
        Hedef/çıktı değişkenin adı.
    threshold : float, default=0
        Hedef değişkendeki bu eşik değerinin üzerindeki değerler 1, altındaki değerler 0 kabul edilir.
    
    Returns:
    --------
    pandas.DataFrame
        Odds ratio, %95 güven aralıkları, p-değerleri, 
        frekans ("x% (n=y)") ve her kategoriye ait chi-square test sonuçlarını içeren DataFrame.
    """

    if drop9:
        # 9 değerini çıkaralım
        data = data[data[variable] != 9]
    # Veri kopyasını oluşturup eksik gözlemleri çıkaralım
    df = data[[variable, target_feature]].copy().dropna()
    
    # Target'ı eşik değerine göre binary yapalım
    df[target_feature] = (df[target_feature] > threshold).astype(int)
    
    # Kategorik değişkeni string'e çevirip category tipine alalım
    if pd.api.types.is_integer_dtype(df[variable]):
        df[variable] = df[variable].astype(str)
    df[variable] = df[variable].astype('category')
    
    # Frekans tablosunu oluşturup "x% (n=y)" formatında string üretiyoruz
    freq_df = df[variable].value_counts(dropna=False).reset_index()
    freq_df.columns = ['Value', 'Count']
    freq_df['Percentage'] = (freq_df['Count'] / len(df) * 100).round(2)
    freq_df['freq_str'] = freq_df['Percentage'].astype(str) + '% (n=' + freq_df['Count'].astype(str) + ')'
    # Örneğin: {'0': '95.08% (n=2127)', '9': '2.5% (n=56)', '1': '2.41% (n=54)'}
    freq_map = dict(zip(freq_df['Value'].astype(str), freq_df['freq_str']))
    
    # Referans kategori: alfabetik olarak ilk gelen (string karşılaştırması)
    reference_category = sorted(df[variable].unique(), key=lambda x: str(x))[0]
    
    # Logistic regresyon (Treatment kodlamasıyla) ile odds ratio hesaplama
    formula = f"{target_feature} ~ C({variable}, Treatment(reference='{reference_category}'))"
    model = smf.logit(formula, data=df)
    result = model.fit(disp=0)
    
    odds_ratios = pd.DataFrame({
        'Odds Ratio': np.exp(result.params),
        '95% CI Lower': np.exp(result.conf_int()[0]),
        '95% CI Upper': np.exp(result.conf_int()[1]),
        'p-value': result.pvalues
    })
    odds_ratios['OR with CI'] = odds_ratios.apply(
        lambda row: f"{row['Odds Ratio']:.2f} ({row['95% CI Lower']:.2f}-{row['95% CI Upper']:.2f})", axis=1)
    
    # Resetleyip kategori isimlerini içeren sütun ekleyelim
    odds_ratios = odds_ratios.reset_index().rename(columns={'index': 'Category'})
    
    # Temiz kategori ismi elde etmek için yardımcı fonksiyon:
    # Eğer "Intercept" ise referans kategoriyi döndür;
    # aksi halde "T.<değer>" ifadesindeki değeri (parantez veya ek karakterlerden arındırarak) çıkar.
    def clean_category(cat):
        cat = cat.strip()
        if cat == "Intercept":
            return str(reference_category)
        m = re.search(r"T\.([^]]+)", cat)
        if m:
            return m.group(1).strip()
        # Eğer T. içermiyorsa, parantezleri temizle
        return cat.replace("]", "").replace("[", "").strip()
    
    # Logistic regresyon çıktısındaki kategori isimlerini temizleyelim
    odds_ratios['clean_cat'] = odds_ratios['Category'].apply(clean_category)
    
    # Frekans bilgisini, temiz kategori ismi üzerinden eşleştiriyoruz
    odds_ratios['Frequency'] = odds_ratios['clean_cat'].map(lambda x: freq_map.get(x, np.nan))
    
    # Her unique kategori için 2x2 chi-square testi (o kategori vs. diğerleri) yapalım
    chi2_map = {}
    for cat in df[variable].unique():
        mask = (df[variable] == cat)
        contingency = pd.crosstab(mask, df[target_feature])
        chi2_stat, chi2_p, dof, expected = chi2_contingency(contingency)
        chi2_map[str(cat)] = (chi2_stat, chi2_p)
    
    # Temiz kategori ismine göre chi-square sonuçlarını eşleştiriyoruz
    odds_ratios['x2_test'] = odds_ratios['clean_cat'].map(lambda x: chi2_map.get(x, (np.nan, np.nan))[0])
    odds_ratios['x2_p'] = odds_ratios['clean_cat'].map(lambda x: chi2_map.get(x, (np.nan, np.nan))[1])
    
    # Category sütununu temiz kategori ile güncelleyelim ve yardımcı sütunu silelim
    odds_ratios['Category'] = odds_ratios['clean_cat']
    odds_ratios = odds_ratios.drop(columns=['clean_cat'])
    odds_ratios = odds_ratios.round(3)
    # Referans bilgisini ekleyelim
    odds_ratios['Reference'] = reference_category
    # Format chi-square test results in a clear and consistent format
    odds_ratios['Chi2'] = odds_ratios.apply(
        lambda row: f"X²={row['x2_test']:.2f}, p={row['x2_p']:.3f}" 
        if not pd.isna(row['x2_test']) and not pd.isna(row['x2_p']) 
        else "", 
        axis=1
    )
    # Remove the individual chi-square columns now that we've combined them
    odds_ratios = odds_ratios.drop(columns=['x2_test', 'x2_p'])
    # Sütun sıralaması
    final_cols = ['Reference', 'Category', 'Frequency', 'Chi2', 'OR with CI', 'p-value', ]
    odds_ratios = odds_ratios[final_cols]
    
    return odds_ratios


import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from scipy.stats import mannwhitneyu

def calculate_odds_ratio_mwu(data, variable, target_feature='target', threshold=0):
    """
    Numeric (sürekli) bir değişkenin, binary target ile ilişkisine göre odds ratio hesaplar,
    logit regresyonu üzerinden 1 birim artışa karşılık gelen odds ratio, %95 güven aralıkları 
    ve p-değerini verir. Ek olarak, hedef gruplar arasında Mann–Whitney U testi yaparak
    numeric değişkenin dağılımlarını karşılaştırır.
    
    Parametreler:
    -----------
    data : pandas.DataFrame
        Analiz edilecek verileri içeren DataFrame.
    variable : str
        İncelenecek numeric değişkenin adı.
    target_feature : str, default='target'
        Hedef/çıktı değişkenin adı. (binary olarak değerlendirilir, threshold üstü 1 kabul edilir)
    threshold : float, default=0
        Hedef değişkendeki bu eşik değerinin üzerindeki değerler 1, altındaki değerler 0 kabul edilir.
    
    Dönüş:
    --------
    pandas.DataFrame
        Odds ratio, %95 güven aralıkları, logit regresyon p-değeri,
        Mann–Whitney U testi istatistiği ve p-değerini içeren tek satırlık sonuç DataFrame'i.
    """
    # Veri kopyasını oluşturup eksik gözlemleri çıkaralım
    df = data[[variable, target_feature]].copy().dropna()
    
    # Target'ı eşik değerine göre binary yapalım
    df[target_feature] = (df[target_feature] > threshold).astype(int)
    
    # Logistic regresyon (numeric değişken için)
    formula = f"{target_feature} ~ {variable}"
    model = smf.logit(formula, data=df)
    result = model.fit(disp=0)
    
    # Değişken katsayısı üzerinden odds ratio hesaplama
    odds_ratio = np.exp(result.params[variable])
    conf_int = result.conf_int().loc[variable]
    lower_ci = np.exp(conf_int[0])
    upper_ci = np.exp(conf_int[1])
    p_value_lr = result.pvalues[variable]
    or_with_ci = f"{odds_ratio:.2f} ({lower_ci:.2f}-{upper_ci:.2f})"
    
    # Mann–Whitney U testi: target=0 ve target=1 gruplarının numeric değişken dağılımlarını karşılaştıralım
    group0 = df.loc[df[target_feature] == 0, variable]
    group1 = df.loc[df[target_feature] == 1, variable]
    u_stat, p_value_mwu = mannwhitneyu(group0, group1, alternative='two-sided')
    mwu_result = f"U={u_stat:.2f}, p={p_value_mwu:.3f}"
    
    # Sonuçları tek satırlık DataFrame olarak hazırlayalım
    result_df = pd.DataFrame({
        'Feature': [variable],
        'Odds Ratio': [odds_ratio],
        '95% CI': [f"{lower_ci:.2f}-{upper_ci:.2f}"],
        'Logistic p-value': [p_value_lr],
        'MWU U': [u_stat],
        'MWU p-value': [p_value_mwu],
        'MWU Result': [mwu_result]
    })
    
    return result_df.round(3)
