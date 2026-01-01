# 🚀 Orkestral AI - Detaylı Kullanım Rehberi

## 📋 İçindekiler

1. [Kurulum](#kurulum)
2. [İlk Kullanım](#ilk-kullanım)
3. [Adım Adım Kullanım](#adım-adım-kullanım)
4. [İterasyon Kullanımı](#iterasyon-kullanımı)
5. [Sorun Giderme](#sorun-giderme)

---

## ⚡ Kurulum

### 1️⃣ API Key Al

1. https://console.anthropic.com adresine git
2. Kayıt ol (ücretsiz)
3. "API Keys" bölümüne git
4. "Create Key" butonuna tıkla
5. Key'i kopyala (örnek: `sk-ant-api03-xxxxx...`)

💰 **Maliyet:** İlk kayıtta $5 ücretsiz kredi! Bir uygulama ~$0.02-0.10

---

### 2️⃣ API Key'i Projeye Ekle

Terminal'de:

```bash
cp .env.example .env
```

Sonra `.env` dosyasını bir text editörle aç ve şunu değiştir:

**Öncesi:**
```env
ANTHROPIC_API_KEY=buraya_api_keyini_yaz
```

**Sonrası:**
```env
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxx
```

> ⚠️ **ÖNEMLİ:** `.env` dosyası asla GitHub'a yüklenmez (`.gitignore` koruyor)

---

### 3️⃣ Bağımlılıkları Yükle

```bash
pip install -r requirements.txt
```

Kurulum 1-2 dakika sürer.

---

## 🎯 İlk Kullanım

### Programı Başlat

```bash
python main.py
```

### Karşılama Ekranı

```
╔══════════════════════════════════════════════════╗
║                                                  ║
║     🤖 ORKESTRAL MOBİL UYGULAMA ÜRETİCİ         ║
║                                                  ║
║     AI Agent Sistemi - Flutter Generator        ║
║                                                  ║
╚══════════════════════════════════════════════════╝

Birden fazla plan seçeneği • İterasyon desteği • AI Kod Review

🔧 AI modeli başlatılıyor...
🤖 AI agentlar hazırlanıyor...
✅ Sistem hazır!

Ne tür bir mobil uygulama istiyorsun?

💡 Örnekler:
  • Bir todo listesi uygulaması
  • Hesap makinesi
  • Not defteri uygulaması
  • Hava durumu uygulaması
  • Quiz oyunu

➜ _
```

---

## 📖 Adım Adım Kullanım

### ADIM 1: İstek Girişi

**İyi Promptlar:**
- ✅ "Basit bir todo listesi uygulaması"
- ✅ "4 işlem yapabilen hesap makinesi"
- ✅ "Günlük not defteri, notları kaydedip listeleyebilsin"

**Kötü Promptlar:**
- ❌ "Uygulama" (çok belirsiz)
- ❌ "Instagram gibi app" (çok karmaşık)
- ❌ "Yapay zeka" (ne yapacak?)

---

### ADIM 2: Plan Seçimi

Program 3 farklı plan sunar:

```
📋 ADIM 1: PLANLAMA

3 farklı plan oluşturuluyor... ✅
✅ 3 Plan Hazır!

┌───┬───────────┬─────────────────────────────┬──────────────────┐
│ # │ Seviye    │ Özellikler                  │ Ekranlar         │
├───┼───────────┼─────────────────────────────┼──────────────────┤
│ 1 │ Basit     │ • Basit todo listesi        │ • HomeScreen     │
│   │           │ • Ekleme/Silme              │                  │
│   │           │ • Local storage             │                  │
├───┼───────────┼─────────────────────────────┼──────────────────┤
│ 2 │ Orta      │ • Kategoriler               │ • HomeScreen     │
│   │           │ • Öncelik seviyeleri        │ • DetailScreen   │
│   │           │ • Firebase entegrasyonu     │ • SettingsScreen │
├───┼───────────┼─────────────────────────────┼──────────────────┤
│ 3 │ Gelişmiş  │ • Takım işbirliği           │ • HomeScreen     │
│   │           │ • Push notifications        │ • DetailScreen   │
│   │           │ • İstatistikler & Analytics │ • ProfileScreen  │
│   │           │ • Dark mode                 │ • StatsScreen    │
└───┴───────────┴─────────────────────────────┴──────────────────┘

Hangi planı seçiyorsun? (1/2/3/detay/iptal): _
```

**Seçeneklerin:**
- `1` / `2` / `3` → Plan seç
- `detay` → Bir planın tam detayını gör
- `iptal` → İşlemi iptal et

**Örnek: Detay Görme**

```
Hangi planı seçiyorsun? detay
Hangi planın detayını görmek istersin? (1/2/3): 2

╭───── Plan 2 Detayı ─────╮
│                         │
│ Todo Uygulaması - Orta  │
│                         │
│ Açıklama:               │
│ Kategorilere ayrılmış   │
│ todo listesi. Firebase  │
│ ile senkronizasyon.     │
│                         │
│ Ekranlar:               │
│ • HomeScreen            │
│ • DetailScreen          │
│ • SettingsScreen        │
│                         │
│ Özellikler:             │
│ • Kategoriler           │
│ • Öncelik seviyeleri    │
│ • Firebase sync         │
│ • Responsive tasarım    │
╰─────────────────────────╯

Hangi planı seçiyorsun? 2
✅ Plan 2 seçildi!
```

---

### ADIM 3: Kod Yazımı (İterasyon Desteği)

```
📋 ADIM 2: KOD YAZIMI

İterasyon 1/3

Flutter kodu yazılıyor... ✅
✅ Kod yazıldı!

╭───── Kod Önizleme ─────╮
│ import 'package:flutter/material.dart';
│
│ void main() {
│   runApp(const MyApp());
│ }
│
│ class MyApp extends StatelessWidget {
│   const MyApp({super.key});
│
│   @override
│   Widget build(BuildContext context) {
│     return MaterialApp(
│       title: 'Todo App',
│       theme: ThemeData(
│         colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
│         useMaterial3: true,
│       ),
│ ...
│ (Toplam 234 satır)
╰────────────────────────╯

Ne yapmak istersin?
Seçim yapın (onayla/değiştir/yeniden/iptal): _
```

**Seçeneklerin:**
- `onayla` → Kodu kabul et, devam et
- `değiştir` → Spesifik değişiklik iste
- `yeniden` → Tamamen yeni kod yaz
- `iptal` → İşlemi iptal et

---

### ADIM 4: Test Yazımı

```
📋 ADIM 3: TEST YAZIMI

Test kodları yazılıyor... ✅
✅ Testler yazıldı!

╭───── Test Önizleme ─────╮
│ import 'package:flutter_test/flutter_test.dart';
│ import 'package:your_app/main.dart';
│
│ void main() {
│   testWidgets('Todo app smoke test', (WidgetTester tester) async {
│     await tester.pumpWidget(const MyApp());
│     expect(find.text('Todo App'), findsOneWidget);
│   });
│ }
│ ...
│ (Toplam 87 satır)
╰─────────────────────────╯

Testleri onayla? (Y/n): y
```

---

### ADIM 5: AI Review

```
📋 ADIM 4: FİNAL REVIEW

AI review yapılıyor... ✅
✅ Review Tamamlandı!

╭───── 🔍 AI Review Sonucu ─────╮
│                               │
│ ✅ Kod kalitesi iyi           │
│                               │
│ Puan: 85/100                  │
│                               │
│ Güçlü Yönler:                 │
│ • Temiz kod yapısı            │
│ • Material Design 3 kullanımı │
│ • İyi yorum satırları         │
│                               │
│ İyileştirme Alanları:         │
│ • State management eklenebilir│
│ • Error handling geliştirilebilir
│                               │
│ Öneriler:                     │
│ • Provider paketi ekle        │
│ • Try-catch bloklarını artır  │
╰───────────────────────────────╯
```

---

### Çıktı Dosyaları

```
✅ UYGULAMA BAŞARIYLA OLUŞTURULDU!

📁 Oluşturulan Dosyalar:
  • output/plan.json      → Seçilen plan detayları
  • output/main.dart      → Flutter uygulama kodu
  • output/main_test.dart → Test kodları
  • output/review.json    → AI kod review raporu

📝 Sonraki Adımlar:
  1. Flutter projesine kodu kopyalayın
  2. flutter run ile uygulamayı çalıştırın
  3. flutter test ile testleri çalıştırın
```

---

## 🔄 İterasyon Kullanımı

### Senaryo 1: Yeniden Yaz

```
Ne yapmak istersin? yeniden

🔄 Kod yeniden yazılıyor...

İterasyon 2/3

Flutter kodu yazılıyor... ✅
✅ Kod yazıldı!

[Yeni kod önizleme]
```

### Senaryo 2: Değişiklik İste

```
Ne yapmak istersin? değiştir
Ne değişmesini istersin? Butonlar daha renkli ve büyük olsun

🔄 'Butonlar daha renkli ve büyük olsun' uygulanıyor...

Kod güncelleniyor... ✅
✅ Kod güncellendi!

[Güncellenmiş kod önizleme]
```

### İterasyon Limiti

```
İterasyon 3/3

[Kod yazılır...]

⚠️ Maksimum iterasyon sayısına ulaşıldı
Mevcut kodu kabul ediyor musun? (Y/n): _
```

---

## 🛠️ Sorun Giderme

### Hata: "API key bulunamadı"

**Çözüm:**
```bash
# .env dosyası var mı kontrol et
ls -la .env

# Yoksa oluştur
cp .env.example .env

# İçeriği kontrol et
cat .env
```

### Hata: "Module not found"

**Çözüm:**
```bash
pip install -r requirements.txt
```

### Kod Çalışmıyor

**Olası Nedenler:**
1. Üretilen kod temel seviyedir
2. Flutter sürüm uyumsuzluğu olabilir
3. Dependency'ler eksik olabilir

**Çözüm:**
```bash
# Flutter projesinde
flutter pub get
flutter clean
flutter run
```

### API Hatası

**Çözüm:**
- API key doğru mu kontrol et
- İnternet bağlantını kontrol et
- Anthropic console'da kredi var mı kontrol et

---

## 💡 İpuçları

### İyi Sonuç İçin

1. ✅ **Spesifik ol**: "Todo uygulaması" yerine "Basit todo listesi, ekleme ve silme fonksiyonlu"
2. ✅ **Basit başla**: İlk defa kullanıyorsan Basit planı seç
3. ✅ **İterasyon kullan**: İlk kod mükemmel olmayabilir, düzeltmelerden çekinme
4. ✅ **Review'ı oku**: AI'nın önerileri değerli

### Maliyet Optimizasyonu

- Basit planlar daha ucuz
- Az iterasyon daha ucuz
- Kısa promptlar daha ucuz

---

## 📞 Yardım

Sorun mu yaşıyorsun?

1. **README.md** dosyasına bak
2. **GitHub Issues** açabilirsin
3. **Logs kontrol et**: Terminal çıktılarını oku

---

**Başarılar! 🚀**
