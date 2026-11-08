# Sağlıklı Yaşam Randevu ve Gelir Takip Sistemi

Bu proje, **İleri Yazılım Teknikleri** dersi için hazırlanmış terminal tabanlı bir randevu ve gelir takip programıdır.

## Programın Amacı ve Özellikleri
Sağlıklı yaşam merkezindeki randevuların düzenli bir şekilde yönetilmesini ve gelir/kâr analizinin yapılmasını sağlar:
- **Randevu Ekleme:** Müşteri adı, tarih, saat ve hizmet seçimiyle yeni randevu oluşturur (Aynı gün ve saatte çakışan randevuları engeller).
- **Randevuları Listeleme:** Kayıtlı tüm randevuları tablo halinde ekranda gösterir.
- **Randevu Arama:** Müşteri adına göre filtreleme yapar.
- **Randevu Tamamlama:** Hizmeti yapılan randevuyu tamamlandı olarak işaretler.
- **Randevu İptal Etme:** İstenilen randevuyu iptal durumuna getirir.
- **Gelir ve Kâr Analizi:**
  - **NumPy:** Tamamlanan randevuların ortalama hizmet ücretini ve toplam ciroyu hesaplar.
  - **Pandas:** Hizmet türlerine göre randevu sayısını, toplam geliri ve net kârı tablo halinde gösterir.
- **JSON Veritabanı:** Tüm veriler `randevular.json` dosyasında saklanır, program kapatılıp açıldığında kayıtlar kaybolmaz.

## Kullanılan Teknolojiler
- Python 3
- Nesne Yönelimli Programlama (OOP) ve Kalıtım (Inheritance)
- NumPy & Pandas
- JSON Dosya Yönetimi

## Nasıl Çalıştırılır?
1. Gerekli kütüphaneleri yükleyin:
```bash
pip install numpy pandas
```

2. Programı başlatın:
```bash
python main.py
```

## Geliştirici
- **Öğrenci:** Sami Yusuf
- **Bölüm:** Bilgisayar Programcılığı (2. Sınıf)
- **Ders:** İleri Yazılım Teknikleri
