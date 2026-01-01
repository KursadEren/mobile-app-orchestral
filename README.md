# 🤖 Orkestral Mobil Uygulama Üretici

**Gelişmiş AI Agent Sistemi** - Türkçe komutlarla otomatik Flutter uygulaması üretin!

## ✨ Özellikler

### 🎯 Çoklu Plan Seçenekleri
Her istek için **3 farklı seviye** plan üretir:
- **Basit**: Minimum özellikler, hızlı geliştirme
- **Orta**: Dengeli özellikler, çoğu kullanıcı için ideal
- **Gelişmiş**: Maksimum özellikler, profesyonel seviye

### 🔄 İterasyon Desteği
- Kodu beğenmedin mi? **"Yeniden yaz"** de
- Değişiklik mi istiyorsun? **Feedback ver**, AI düzeltsin
- **3 iterasyon** hakkınız var

### 🔍 AI Kod Review
- Otomatik kod kalite analizi
- Best practices kontrolü
- İyileştirme önerileri

### 💬 İnteraktif Kullanıcı Deneyimi
- Adım adım kullanıcı onayı
- Kod önizleme
- Detaylı plan görüntüleme

---

## 🚀 Hızlı Başlangıç

### 1. Bağımlılıkları Yükle

```bash
pip install -r requirements.txt
```

### 2. API Key Ekle

```bash
cp .env.example .env
```

`.env` dosyasını düzenle:
```env
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
```

> 💡 API key almak için: https://console.anthropic.com

### 3. Çalıştır

```bash
python main.py
```

---

## 📖 Nasıl Çalışır?

### Akış Diyagramı

```
Kullanıcı İsteği
      ↓
┌─────────────────────────────────┐
│  ADIM 1: PLANLAMA               │
│  3 farklı plan seçeneği sunulur │
│  Kullanıcı birini seçer         │
└─────────────────────────────────┘
      ↓
┌─────────────────────────────────┐
│  ADIM 2: KOD YAZIMI             │
│  Flutter kodu üretilir          │
│  Kullanıcı onayla/değiştir      │
│  (İterasyon desteği)            │
└─────────────────────────────────┘
      ↓
┌─────────────────────────────────┐
│  ADIM 3: TEST YAZIMI            │
│  Otomatik test kodları          │
│  Kullanıcı onayı                │
└─────────────────────────────────┘
      ↓
┌─────────────────────────────────┐
│  ADIM 4: AI REVIEW              │
│  Kod kalite analizi             │
│  İyileştirme önerileri          │
└─────────────────────────────────┘
      ↓
📦 Çıktı Dosyaları
```

---

## 📁 Proje Yapısı

```
mobile-app-orchestral/
├── agents/
│   ├── __init__.py
│   ├── orchestrator.py   # Ana koordinatör
│   ├── planner.py        # 3 plan seçeneği üreticisi
│   ├── coder.py          # İterasyonlu kod üreticisi
│   ├── tester.py         # Test üreticisi
│   └── reviewer.py       # Kod review uzmanı
├── output/               # Üretilen dosyalar
│   ├── plan.json
│   ├── main.dart
│   ├── main_test.dart
│   └── review.json
├── main.py               # İnteraktif ana program
├── requirements.txt
├── .env.example
├── README.md
└── NASIL_KULLANILIR.md
```

---

## 💡 Kullanım Örnekleri

### Örnek 1: Todo Uygulaması

```
Ne tür bir mobil uygulama istiyorsun?
➜ Bir todo listesi uygulaması

3 Plan Hazır!
┌───┬─────────────┬──────────────────────┐
│ # │ Seviye      │ Özellikler           │
├───┼─────────────┼──────────────────────┤
│ 1 │ Basit       │ • Ekleme/Silme       │
│   │             │ • Basit liste        │
├───┼─────────────┼──────────────────────┤
│ 2 │ Orta        │ • Kategoriler        │
│   │             │ • Öncelik            │
│   │             │ • Local storage      │
├───┼─────────────┼──────────────────────┤
│ 3 │ Gelişmiş    │ • Firebase sync      │
│   │             │ • Bildirimler        │
│   │             │ • İstatistikler      │
└───┴─────────────┴──────────────────────┘

Hangi planı seçiyorsun? (1/2/3/detay/iptal): 2

✅ Plan 2 seçildi!

[Kod yazılıyor...]
✅ Kod yazıldı!

Ne yapmak istersin?
Seçim yapın (onayla/değiştir/yeniden/iptal): onayla

✅ Kod onaylandı!
```

### Örnek 2: Hesap Makinesi

```
➜ Basit bir hesap makinesi

[3 plan gösterilir, sen seçersin]
[Kod yazılır]

Ne yapmak istersin? değiştir
Ne değişmesini istersin? Butonlar daha büyük olsun

🔄 Kod güncelleniyor...
✅ Kod güncellendi!
```

---

## 🎨 Çıktılar

Program başarıyla tamamlandığında `output/` klasöründe:

- **plan.json** - Seçilen plan detayları
- **main.dart** - Tam çalışır Flutter kodu
- **main_test.dart** - Widget ve unit testler
- **review.json** - AI kod review raporu

---

## 🔧 Flutter Projesine Entegre Etme

### Yöntem 1: Yeni Proje

```bash
flutter create my_app
cd my_app
cp ../output/main.dart lib/main.dart
flutter run
```

### Yöntem 2: Mevcut Proje

```bash
# Kodu kopyala
cp output/main.dart your_flutter_project/lib/main.dart

# Testleri kopyala
cp output/main_test.dart your_flutter_project/test/

# Çalıştır
cd your_flutter_project
flutter run
```

---

## 🛠️ Gelişmiş Kullanım

### İterasyon Kullanımı

Kod beğenmediğinde:

1. **"yeniden"** → Tamamen yeni kod yazar
2. **"değiştir"** → Feedback ver, spesifik değişiklik yapsın
3. **"onayla"** → Kodu kabul et, devam et

### Plan Detayları

Plan seçiminde **"detay"** yazarak her planın tam açıklamasını görebilirsin.

---

## 📊 Özellik Karşılaştırması

| Özellik | Basit Sistem | Orkestral Sistem |
|---------|--------------|------------------|
| Plan sayısı | 1 | 3 seçenek |
| İterasyon | ❌ | ✅ 3 iterasyon |
| Kod review | ❌ | ✅ AI review |
| Kullanıcı onayı | ❌ | ✅ Her adımda |
| Feedback | ❌ | ✅ Çift yönlü |

---

## 💰 Maliyet

- İlk kayıtta **$5 ücretsiz kredi**
- Bir uygulama: **~$0.02-0.10**
- Plan seçimi ve iterasyon daha fazla token kullanır

---

## 🤝 Katkıda Bulunma

Pull request'ler memnuniyetle karşılanır!

### Geliştirme Fikirleri

- [ ] React Native desteği
- [ ] SwiftUI / Jetpack Compose
- [ ] Web socket ile canlı önizleme
- [ ] Daha fazla iterasyon seçeneği
- [ ] Kod diff gösterimi

---

## 📝 Notlar

- Üretilen kod **temel seviyedir**, production için geliştirme gerekir
- Kompleks uygulamalar için manuel düzenleme gerekebilir
- API kullanımı ücretlidir
- İnternete bağlı olmanız gerekir

---

## 📄 Lisans

MIT License

---

## 📞 Destek

- 📚 [Detaylı Kullanım](NASIL_KULLANILIR.md)
- 🐛 [Sorun Bildir](https://github.com/KursadEren/mobile-app-orchestral/issues)
- 💬 Sorularınız için Issue açın

---

**Made with ❤️ using Claude AI**
