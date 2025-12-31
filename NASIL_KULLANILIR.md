# 🚀 Hızlı Başlangıç Rehberi

## ⚡ 3 Adımda Başla

### 1️⃣ API Key Al

https://console.anthropic.com adresine git:
- Kayıt ol (ücretsiz)
- "API Keys" bölümüne git
- "Create Key" tıkla
- Key'i kopyala (sk-ant-api03-... ile başlar)

💰 **Maliyet:** İlk kayıtta $5 ücretsiz kredi! Bir uygulama üretmek ~$0.01-0.05

---

### 2️⃣ API Key'i Ekle

Terminal'de şu komutu çalıştır:

```bash
cp .env.example .env
```

Sonra [.env](/.env) dosyasını aç ve şunu değiştir:

```env
ANTHROPIC_API_KEY=buraya_kendi_keyini_yapıştır
```

Örnek:
```env
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxx
```

---

### 3️⃣ Çalıştır!

```bash
python main.py
```

Şunu soracak:

```
Ne tür bir mobil uygulama istiyorsun?
➜
```

**Örnek girişler:**
- Bir todo listesi uygulaması
- Hesap makinesi
- Not defteri uygulaması
- Quiz oyunu
- Hava durumu uygulaması

---

## 📦 Çıktılar

Sistem 3 dosya oluşturur:

```
output/
├── plan.json         → Uygulama planı (JSON)
├── main.dart         → Flutter kodu
└── main_test.dart    → Test kodu
```

---

## 🧪 Oluşturulan Uygulamayı Test Et

### Flutter Kurulu İse:

```bash
# Yeni proje oluştur
flutter create my_app
cd my_app

# Kodu kopyala
cp ../output/main.dart lib/main.dart

# Çalıştır
flutter run
```

### Flutter Yok İse:

Kodu kopyala ve https://dartpad.dev adresinde test et!

---

## 🎯 İpuçları

### ✅ İyi Promptlar:
- "Basit bir todo listesi uygulaması, ekleme ve silme fonksiyonlu"
- "Hesap makinesi, 4 işlem yapabilsin"
- "Not defteri, notları kaydedip listeleyebileyim"

### ❌ Kötü Promptlar:
- "Uygulama yap" (çok belirsiz)
- "Instagram benzeri app" (çok karmaşık)

---

## 🛠️ Sorun Giderme

### Hata: "API key bulunamadı"
- `.env` dosyası var mı kontrol et
- Key doğru kopyalandı mı kontrol et

### Hata: "Module not found"
```bash
pip install -r requirements.txt
```

### Kod çalışmıyor
- Üretilen kod temel seviyededir
- Kopyala-yapıştır hataları olabilir
- Manuel düzenleme gerekebilir

---

## 📞 Yardım

Sorun mu yaşıyorsun?
- GitHub Issues: [Sorun bildir](https://github.com/KursadEren/mobile-app-orchestral/issues)
- README.md dosyasına bak
