# AI Snake - Yapay Zeka ile Öğrenen Klasik Yılan Oyunu 🐍

<div align="center">
  <img src="docs/snake-ai-logo.png" alt="AI Snake Logo" width="200" height="200"/>
</div>

## 📝 Proje Hakkında

AI Snake, klasik Nokia yılan oyununun modern bir yapay zeka implementasyonudur. Deep Q-Learning kullanarak kendi kendine oynamayı ve gelişmeyi öğrenen bir sistem içerir.

## 🚀 Teknoloji Stack'i

### Frontend
- Pygame (Python oyun geliştirme kütüphanesi)
- Modern ve retro görünüm için pixel art tasarım

### Yapay Zeka
- PyTorch veya TensorFlow (Derin Öğrenme framework'ü)
- Deep Q-Learning (DQN) algoritması
- Reinforcement Learning yaklaşımı

## 🎮 Temel Özellikler

### Oyun Modları
- **Klasik Mod:** Kullanıcının klasik yılan oyununu oynayabildiği mod
  - Klavye kontrolleri (Ok tuşları veya WASD)
  - Skor tablosu
  - Zorluk seviyeleri (Kolay, Orta, Zor)
  - Yüksek skor kaydetme

- **AI Mod:** Yapay zekanın kendi kendine öğrendiği mod
  - Gerçek zamanlı eğitim görselleştirmesi
  - Model performans metrikleri
  - Eğitim durumu kaydetme/yükleme
  - Eğitim parametrelerini ayarlama seçenekleri

### Oyun Mekanikleri
- Klasik Nokia tarzı grid-bazlı oyun alanı
- Yılanın temel hareketleri (yukarı, aşağı, sağ, sol)
- Random konumlarda spawn olan yemler
- Yılan yemi yedikçe uzama mekanizması
- Çarpışma sistemi (duvarlara ve kendine çarpma)
- Progressive zorluk sistemi (hız artışı)

### Yapay Zeka Özellikleri
- Deep Q-Learning tabanlı öğrenme sistemi
- Her oyun sonrası kendini geliştiren model
- Skor bazlı ödül sistemi
- Deneyim tekrarı (Experience Replay) mekanizması
- Adaptif öğrenme hızı

### Görselleştirme ve UI
- Retro stil piksel grafikleri
- Skor göstergesi
- Yapay zeka performans metrikleri
- Hız göstergesi
- Jenerasyon/Deneme sayısı göstergesi

## 🛠 Teknik Gereksinimler

### Oyun Motoru Gereksinimleri
- 60 FPS sabit frame rate
- Grid bazlı hareket sistemi
- Çarpışma algılama sistemi
- Yem spawn algoritması
- Mod değiştirme sistemi
- Kullanıcı kontrol sistemi (Klasik mod için)
- Ayarlar menüsü

### Yapay Zeka Gereksinimleri
- **State space:** Yılanın pozisyonu, yönü, yem konumu, engeller
- **Action space:** 4 yön (yukarı, aşağı, sağ, sol)
- **Reward sistemi:**
  - Yem yeme: +10 puan
  - Ölüm: -10 puan
  - Her hareket: -0.01 puan (optimal yol seçimi için)

### Veri Yönetimi
- En iyi modelin kaydedilmesi
- Performans metriklerinin loglanması
- Öğrenme sürecinin görselleştirilmesi

## 📊 Performans Metrikleri
- Ortalama skor
- En yüksek skor
- Yaşam süresi
- Öğrenme eğrisi grafiği
- Başarılı hamle oranı

## 📅 Geliştirme Fazları

### Faz 1: Temel Oyun Mekanikleri
- [ ] Oyun alanının oluşturulması
- [ ] Temel yılan hareketleri
- [ ] Yem sistemi
- [ ] Çarpışma kontrolü

### Faz 2: Yapay Zeka Entegrasyonu
- [ ] DQN modelinin implementasyonu
- [ ] Reward sisteminin kurulması
- [ ] Training loop'unun oluşturulması

### Faz 3: UI ve Görselleştirme
- [ ] Retro grafiklerin implementasyonu
- [ ] Performans metriklerinin görselleştirilmesi
- [ ] Kullanıcı arayüzü geliştirmeleri

### Faz 4: Optimizasyon ve İyileştirmeler
- [ ] Model performans optimizasyonu
- [ ] Hız ve zorluk dengesi
- [ ] Bug fixes ve polish

## 🎯 Başarı Kriterleri
- Yapay zekanın minimum 50 skor yapabilmesi
- Ortalama yaşam süresinin 2 dakikanın üzerine çıkması
- Yılanın kendini tekrar etmeyen stratejiler geliştirebilmesi
- 60 FPS'de stabil çalışma

## 🚀 Kurulum

```bash
# Repository'yi klonlayın
git clone https://github.com/yourusername/ai-snake.git

# Proje dizinine gidin
cd ai-snake

# Gerekli paketleri yükleyin
pip install -r requirements.txt

# Oyunu başlatın
python src/main.py

# Mod Seçimi:
# 1. Klasik Mod için: python main.py --mode classic
# 2. AI Mod için: python main.py --mode ai
```

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için [LICENSE](LICENSE) dosyasına bakın.

## 🤝 Katkıda Bulunma

1. Fork'layın
2. Feature branch'i oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'feat: Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📞 İletişim

Proje Sahibi - [@yourusername](https://twitter.com/yourusername)

Proje Linki: [https://github.com/yourusername/ai-snake](https://github.com/yourusername/ai-snake) 
