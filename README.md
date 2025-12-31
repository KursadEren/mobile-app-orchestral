# 🤖 Mobil Uygulama Üretici - AI Agent Sistemi

Türkçe komutlarla otomatik Flutter uygulaması üreten AI agent sistemi.

## 📋 Ne Yapar?

Kullanıcıdan aldığı açıklamaya göre:
1. **Uygulama planı** oluşturur
2. **Flutter kodu** yazar
3. **Test kodları** üretir

Tüm işlemi otomatik yapar!

## 🚀 Kurulum

### 1. Gereksinimler

- Python 3.8+
- Anthropic API Key ([buradan alabilirsin](https://console.anthropic.com))

### 2. Bağımlılıkları Yükle

```bash
pip install -r requirements.txt
```

### 3. API Key Ekle

`.env.example` dosyasını kopyala ve `.env` olarak kaydet:

```bash
cp .env.example .env
```

Sonra `.env` dosyasını aç ve API key'ini ekle:

```env
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
```

## 💻 Kullanım

```bash
python main.py
```

Sonra istediğin uygulamayı açıkla:

```
Ne tür bir mobil uygulama istiyorsun?
➜ Bir todo listesi uygulaması
```

Sistem otomatik olarak:
- ✅ Uygulama planı çıkarır → `output/plan.json`
- ✅ Flutter kodu yazar → `output/main.dart`
- ✅ Test kodları üretir → `output/main_test.dart`

## 📁 Proje Yapısı

```
mobile-app-orchestral/
├── agents/
│   ├── __init__.py
│   ├── planner.py    # Uygulama planı yapan agent
│   ├── coder.py      # Kod yazan agent
│   └── tester.py     # Test yazan agent
├── output/           # Üretilen dosyalar buraya kaydedilir
├── main.py           # Ana program
├── requirements.txt  # Python bağımlılıkları
├── .env.example      # API key şablonu
└── README.md
```

## 🔧 Üretilen Kodu Kullanma

### Flutter Projesine Entegre Etme

1. Yeni Flutter projesi oluştur:
```bash
flutter create my_app
cd my_app
```

2. `output/main.dart` dosyasını kopyala:
```bash
cp ../output/main.dart lib/main.dart
```

3. Çalıştır:
```bash
flutter run
```

4. Testleri çalıştır:
```bash
cp ../output/main_test.dart test/main_test.dart
flutter test
```

## 🎯 Örnek Komutlar

- "Bir hesap makinesi uygulaması"
- "Hava durumu gösteren uygulama"
- "Not defteri uygulaması"
- "Quiz oyunu"
- "Alışveriş listesi uygulaması"

## 🛠️ Geliştirme

### Yeni Agent Eklemek

1. `agents/` klasöründe yeni dosya oluştur
2. `agents/__init__.py` dosyasına ekle
3. `main.py` içinde kullan

### Farklı Platform Desteği

Şu an sadece Flutter destekleniyor. React Native veya native Android/iOS eklemek için:
- `CoderAgent` sınıfına platform seçimi ekle
- Platform bazlı kod üretim metodları ekle

## 📝 Notlar

- API kullanımı ücretlidir (~$0.01-0.05 per uygulama)
- Üretilen kod temel seviyededir, production için geliştirme gerekir
- Kompleks uygulamalar için ek düzenleme gerekebilir

## 🤝 Katkıda Bulunma

Pull request'ler memnuniyetle karşılanır!

## 📄 Lisans

MIT License
