Target: 
Ilk ay icerisinde 3'ten fazla office visiti olan
Ilk ay icerisinde ER visiti olan 
Ilk ay icerisinde yeniden yatisi olan hastalar 

Inclusion
Mumkun olan tum hastalar --> tarih araligini yaz

======================================================================================================================================================================

Metod: Calisma 2016 yilindan itibare 6 senelik donemde CC de NICU dan taburcu olan 4100 tane hastanin verisi kullanilarak gelistirilmistir. Calisma grubu 30 gunluk sure icerisinde 3'ten fazla office visiti, ER visiti veya NICU'ya yeniden yatis yapan hastalar tekrar basvuru olarak belirlendi. Internal validasyon icin veri setinin %20 si test verisi olarak ayrilmis, kayip veriler MICE ile doldurulmustur. Feature selection islemi featurelarin klinik, geleneksel istatistiksel ozelliklerine gore manuel olarak secilmistir. Veri seti Ardindan egiim veri setinin %80'i egitim %20'si egitim validasyonu olarak ayrilmis olup stratified fold ile cross validation ile ten fold olarak CatBoost LightGBM ve XGBoost modelleri egitilmistir. Modeller egitildikten sonra optuna ile hiperparametreleri optimize edilmistir. 

Results: NICU'dan taburcu edilen hastalarin %21'i (871) yeniden basvuru olarak tanimlandi. Gelistirilen en yuksek performansli ML modeli LightGBM oldu ROC-AUC %79.3 (95% CI: 76.7% - 82.8%) ve PR-AUC 49.3% (95% CI: 42.3% - 56.0%) olarak gozlendi. Bu modelin SHAP degerlerine gore readmissionu ongormede en etkili bes variable NICU Lenght of stay, gestational week, weight loss percent, min hemoglobin level, max blood glucose level olarak bulundu. 



The study was developed using data from 4,100 neonates discharged from the neonatal intensive care unit (NICU) at the Cleveland Clinic over a six-year period beginning in 2016. Patients who had more than three subsequent office visits, emergency room visits, or NICU readmissions within 30 days post-discharge were defined as having experienced readmission. The dataset was partitioned with 20% reserved for internal validation, and missing data were imputed using Multiple Imputation by Chained Equations (MICE). Feature selection was manually performed based on clinical relevance and statistical properties. The training subset was further divided into training (80%) and validation (20%) sets, and CatBoost, LightGBM, and XGBoost models were trained using stratified ten-fold cross-validation. Following model training, hyperparameter optimization was conducted using Optuna.

Results indicated that 21% (n=871) of neonates discharged from the NICU met the readmission criteria. Among the machine learning models developed, the LightGBM model exhibited the highest predictive performance, achieving a ROC-AUC of 79.3% (95% CI: 76.7%-82.8%) and a PR-AUC of 49.3% (95% CI: 42.3%-56.0%). SHapley Additive exPlanations (SHAP) analysis demonstrated that the five most influential variables in predicting NICU readmission were NICU length of stay, gestational week at birth, percent weight loss, minimum hemoglobin level, and maximum blood glucose level.













noSMOTE+OUTLIER
ROC-AUC: 0.713 (95% CI: 0.687 - 0.748)
PR-AUC: 0.413 (95% CI: 0.343 - 0.480)
Precision: 0.450 (95% CI: 0.229 - 0.598)
Recall: 0.190 (95% CI: 0.117 - 0.311)
F1 Score: 0.263 (95% CI: 0.155 - 0.396)
Brier Score: 0.162 (95% CI: 0.150 - 0.177)
Balanced Accuracy: 0.561 (95% CI: 0.505 - 0.622)
F2 Score: 0.214 (95% CI: 0.130 - 0.340)

SMOTE+OUTLIER

ROC-AUC: 0.694 (95% CI: 0.669 - 0.730)
PR-AUC: 0.371 (95% CI: 0.330 - 0.397)
Precision: 0.580 (95% CI: 0.410 - 0.950)
Recall: 0.052 (95% CI: 0.031 - 0.059)
F1 Score: 0.093 (95% CI: 0.060 - 0.103)
Brier Score: 0.159 (95% CI: 0.152 - 0.165)
Balanced Accuracy: 0.519 (95% CI: 0.515 - 0.521)
F2 Score: 0.063 (95% CI: 0.039 - 0.071)


Yenidoğan tıbbi verileri, sağlık sektöründe kritik bilgiler barındırmakta olup bu verilerin etkili bir şekilde analiz edilmesi büyük önem taşımaktadır. Makine öğrenimi algoritmaları, yenidoğanlara ait tıbbi verilerden anlamlı içgörüler elde etmek ve tedavi süreçlerini iyileştirmek için güçlü araçlar sunmaktadır. Hastanede kalış süresinin önceden bilinmesi, hastane kaynaklarının, sağlık personelinin ve maliyetlerin yönetimi açısından oldukça önemlidir. Bu nedenle, bu çalışma, Yenidoğan Yoğun Bakım Ünitesi'nde (YYBÜ) tedavi gören bebeklerin hastanede kalış sürelerini makine öğrenimi algoritmaları kullanarak tahmin etmeyi amaçlamaktadır.

Çalışmamız, uzun ve kısa süreli kalış süreleri için iki sınıflı bir tahmin gerçekleştirmiş ve benzersiz bir veri seti kullanmıştır. Classifier Fusion-LoS adlı hibrit bir yaklaşım benimsenmiş ve çalışma iki aşamadan oluşmuştur. İlk aşamada, Lojistik Regresyon, ExtraTrees, Random Forest, KNN, Destek Vektör Sınıflandırıcısı gibi klasik modellerin yanı sıra AdaBoost, GradientBoosting, XGBoost ve CatBoost gibi topluluk (ensemble) modelleri de dahil olmak üzere çeşitli sınıflandırıcılar kullanılmıştır. Random Forest modeli, 0.94 doğrulama doğruluğu ile en yüksek başarıyı elde etmiştir. İkinci aşamada ise, bir topluluk yöntemi olan Oylama Sınıflandırıcısı (Voting Classifier) uygulanmış ve doğruluk oranı 0.96’ya yükselmiştir.

Önerilen yöntemimiz, doğruluk açısından hem yenidoğana özgü hastanede kalış süresi tahmini çalışmalarını hem de genel kalış süresi tahmini araştırmalarını geride bırakmıştır. Kalış süresi tahmini, her şehirde bulunmayan YYBÜ’lerdeki kuvözlerin hasta kabulü için uygunluğunu değerlendirmeye dair önemli içgörüler sunmasının yanı sıra, hasta tedavi protokollerinin belirlenmesinde de kritik bir rol oynamaktadır. Ayrıca, araştırma; yatak, ekipman, personel ve maliyet planlaması gibi konularda hastane yönetimine de önemli bilgiler sağlamaktadır.

======================================================================================================================================================================

**Yöntemler:** Bu gözlemsel kohort çalışması, Amerika Birleşik Devletleri’nde yaklaşık 600 yatak kapasiteli bir akademik hastanede yürütülmüştür. Toplam 24.885 yoğun bakım ünitesinden (YBÜ) servislere yapılan hasta transferi çalışmaya dahil edilmiştir. Bu transferlerin 14.962’si (%60) eğitim kohortunu, 9.923’ü (%40) ise dahili doğrulama kohortunu oluşturmuştur. Elektronik sağlık kayıtlarından elde edilen hasta özellikleri, hemşire değerlendirmeleri, önceki yatışlara ait Uluslararası Hastalık Sınıflaması (ICD-9) kodları, ilaçlar, YBÜ müdahaleleri, tanısal testler, hayati bulgular ve laboratuvar sonuçları, gradient-boosted makine öğrenimi modelinde öngörücü değişkenler olarak kullanılmıştır. YBÜ’ye yeniden yatış tahmini doğruluğu, Stability and Workload Index for Transfer (SWIFT) skoru ve Modified Early Warning Score (MEWS) ile hem dahili doğrulama kohortunda hem de Medical Information Mart for Intensive Care (MIMIC) veri tabanı (n = 42.303 YBÜ transferi) kullanılarak karşılaştırılmıştır.

**Bulgular:** Servislere taburcu edilen hastaların %11’i (2.834 hasta) daha sonra yeniden YBÜ’ye yatırılmıştır. Makine öğrenimine dayalı geliştirilen model, YBÜ’ye yeniden yatışı tahmin etmede istatistiksel olarak anlamlı şekilde daha iyi bir performans göstermiştir (ROC eğrisi altında kalan alan [AUC], 0.76); bu oran SWIFT skoru için 0.65, MEWS için ise 0.58’dir (tüm karşılaştırmalar için P değeri < 0.0001). %95 özgüllük düzeyinde, geliştirilen modelin duyarlılığı %28 iken, bu oran SWIFT skoru için %15, MEWS için ise yalnızca %7 olarak bulunmuştur. Geliştirilen modelin doğruluk açısından sağladığı iyileşmeler, MIMIC-III kohortunda da MEWS ve SWIFT skorlarına benzer şekilde gözlenmiştir.

