import json
import os
from datetime import datetime
import numpy as np
import pandas as pd

dosya_yolu = os.path.join(os.path.dirname(__file__), "randevular.json")

hizmetler = {
    "1": {"ad": "Diyetisyen", "tur": "Beslenme", "ucret": 500, "maliyet": 150},
    "2": {"ad": "Fizyoterapi", "tur": "Tedavi", "ucret": 600, "maliyet": 200},
    "3": {"ad": "Masaj", "tur": "Spa", "ucret": 400, "maliyet": 100},
    "4": {"ad": "Fitness", "tur": "Spor", "ucret": 300, "maliyet": 100},
    "5": {"ad": "Cilt Bakimi", "tur": "Bakim", "ucret": 700, "maliyet": 250}
}

class TemelRandevu:
    def __init__(self, randevu_id, musteri_adi, tarih, saat, ucret, maliyet, durum="Bekliyor"):
        self.randevu_id = randevu_id
        self.musteri_adi = musteri_adi
        self.tarih = tarih
        self.saat = saat
        self.ucret = ucret
        self.maliyet = maliyet
        self.durum = durum

    def durum_guncelle(self, yeni_durum):
        self.durum = yeni_durum

    def kar_hesapla(self):
        return self.ucret - self.maliyet

class SaglikliYasamRandevu(TemelRandevu):
    def __init__(self, randevu_id, musteri_adi, hizmet_adi, hizmet_turu,
                 tarih, saat, ucret, maliyet, durum="Bekliyor"):
        super().__init__(randevu_id, musteri_adi, tarih, saat, ucret, maliyet, durum)
        self.hizmet_adi = hizmet_adi
        self.hizmet_turu = hizmet_turu

    def to_dict(self):
        return {
            "id": self.randevu_id,
            "musteri_adi": self.musteri_adi,
            "hizmet_adi": self.hizmet_adi,
            "hizmet_turu": self.hizmet_turu,
            "tarih": self.tarih,
            "saat": self.saat,
            "ucret": self.ucret,
            "maliyet": self.maliyet,
            "durum": self.durum
        }

    @classmethod
    def from_dict(cls, veri):
        return cls(
            randevu_id=veri["id"],
            musteri_adi=veri["musteri_adi"],
            hizmet_adi=veri["hizmet_adi"],
            hizmet_turu=veri.get("hizmet_turu", "Genel"),
            tarih=veri["tarih"],
            saat=veri["saat"],
            ucret=veri["ucret"],
            maliyet=veri.get("maliyet", veri["ucret"] * 0.3),
            durum=veri.get("durum", "Bekliyor")
        )

def randevulari_yukle():
    if not os.path.exists(dosya_yolu):
        return []
    try:
        with open(dosya_yolu, "r", encoding="utf-8") as f:
            veriler = json.load(f)
            return [SaglikliYasamRandevu.from_dict(v) for v in veriler]
    except Exception as hata:
        print(f"[HATA] Dosya okunurken sorun olustu: {hata}")
        return []

def randevulari_kaydet(randevular):
    try:
        with open(dosya_yolu, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in randevular], f, ensure_ascii=False, indent=2)
        return True
    except Exception as hata:
        print(f"[HATA] Dosya kaydedilirken sorun olustu: {hata}")
        return False

def yeni_id_belirle(randevular):
    if not randevular:
        return 1
    return max(r.randevu_id for r in randevular) + 1

def cakisma_var_mi(randevular, tarih, saat):
    for r in randevular:
        if r.tarih == tarih and r.saat == saat and r.durum == "Bekliyor":
            print(f"\n[UYARI] {tarih} günü saat {saat} zaten DOLU! Lütfen başka bir saat seçiniz.")
            return True
    return False

def tarih_dogrula(tarih_metni):
    try:
        datetime.strptime(tarih_metni, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def saat_dogrula(saat_metni):
    try:
        datetime.strptime(saat_metni, "%H:%M")
        return True
    except ValueError:
        return False

def randevulari_listele(randevular):
    print("\n--- KAYITLI RANDEVULAR ---")
    if not randevular:
        print("Sistemde henuz kayitli randevu bulunmamaktadir.")
        return

    print("-" * 85)
    print(f"{'ID':<4} | {'Müşteri Adı':<18} | {'Hizmet Adı':<15} | {'Tarih':<10} | {'Saat':<6} | {'Ücret':<8} | {'Durum':<10}")
    print("-" * 85)
    for r in randevular:
        print(f"{r.randevu_id:<4} | {r.musteri_adi:<18} | {r.hizmet_adi:<15} | {r.tarih:<10} | {r.saat:<6} | {r.ucret:<8} | {r.durum:<10}")
    print("-" * 85)
    print(f"Toplam Kayıt Sayısı: {len(randevular)}")

def randevu_ara(randevular):
    print("\n--- RANDEVU ARA ---")
    aranan = input("Aramak istediğiniz müşteri adı: ").strip().lower()
    if not aranan:
        print("[UYARI] Arama için bir isim girmelisiniz!")
        return

    bulunanlar = [r for r in randevular if aranan in r.musteri_adi.lower()]

    if not bulunanlar:
        print(f"'{aranan}' adına uygun bir randevu kaydı bulunamadı.")
        return

    print(f"\nBulunan Randevular ({len(bulunanlar)} adet):")
    print("-" * 85)
    print(f"{'ID':<4} | {'Müşteri Adı':<18} | {'Hizmet Adı':<15} | {'Tarih':<10} | {'Saat':<6} | {'Ücret':<8} | {'Durum':<10}")
    print("-" * 85)
    for r in bulunanlar:
        print(f"{r.randevu_id:<4} | {r.musteri_adi:<18} | {r.hizmet_adi:<15} | {r.tarih:<10} | {r.saat:<6} | {r.ucret:<8} | {r.durum:<10}")
    print("-" * 85)

def randevu_ekle(randevular):
    print("\n--- YENİ RANDEVU EKLE ---")
    musteri_adi = input("Müşteri Adı Soyadı: ").strip()
    if not musteri_adi:
        print("[UYARI] Müşteri adı boş bırakılamaz!")
        return

    tarih = input("Randevu Tarihi (YYYY-AA-GG, Örn: 2026-11-15): ").strip()
    if not tarih_dogrula(tarih):
        print("[UYARI] Geçersiz tarih formatı! Lütfen YYYY-AA-GG şeklinde giriniz.")
        return

    saat = input("Randevu Saati (SS:00, Örn: 14:00): ").strip()
    if not saat_dogrula(saat):
        print("[UYARI] Geçersiz saat formatı! Lütfen 10:00, 14:00 şeklinde giriniz.")
        return

    if cakisma_var_mi(randevular, tarih, saat):
        return

    print("\nMevcut Hizmetler:")
    for k, v in hizmetler.items():
        print(f"  [{k}] {v['ad']} - {v['ucret']} TL")

    secim = input("Hizmet Numarası (1-5): ").strip()
    if secim not in hizmetler:
        print("[UYARI] Geçersiz hizmet seçimi yaptınız!")
        return

    secilen = hizmetler[secim]
    yeni_id = yeni_id_belirle(randevular)

    yeni_randevu = SaglikliYasamRandevu(
        randevu_id=yeni_id,
        musteri_adi=musteri_adi,
        hizmet_adi=secilen["ad"],
        hizmet_turu=secilen["tur"],
        tarih=tarih,
        saat=saat,
        ucret=secilen["ucret"],
        maliyet=secilen["maliyet"],
        durum="Bekliyor"
    )

    randevular.append(yeni_randevu)
    if randevulari_kaydet(randevular):
        print(f"\n[BAŞARILI] {musteri_adi} adına {tarih} {saat} için randevu oluşturuldu! (ID: {yeni_id})")

def randevu_tamamla(randevular):
    print("\n--- RANDEVU TAMAMLA ---")
    try:
        randevu_id = int(input("Tamamlandı yapılacak Randevu ID: ").strip())
    except ValueError:
        print("[HATA] Lütfen geçerli bir sayı giriniz!")
        return

    for r in randevular:
        if r.randevu_id == randevu_id:
            if r.durum == "Tamamlandı":
                print(f"[UYARI] {randevu_id} numaralı randevu zaten tamamlanmış.")
                return
            r.durum_guncelle("Tamamlandı")
            randevulari_kaydet(randevular)
            print(f"[BAŞARILI] {randevu_id} numaralı randevu 'Tamamlandı' olarak işaretlendi.")
            return

    print(f"[UYARI] {randevu_id} numaralı randevu bulunamadı.")

def randevu_iptal_et(randevular):
    print("\n--- RANDEVU İPTAL ET ---")
    try:
        randevu_id = int(input("İptal edilecek Randevu ID: ").strip())
    except ValueError:
        print("[HATA] Lütfen geçerli bir sayı giriniz!")
        return

    for r in randevular:
        if r.randevu_id == randevu_id:
            if r.durum == "İptal":
                print(f"[UYARI] {randevu_id} numaralı randevu zaten iptal edilmiş.")
                return
            r.durum_guncelle("İptal")
            randevulari_kaydet(randevular)
            print(f"[BAŞARILI] {randevu_id} numaralı randevu başarıyla iptal edildi.")
            return

    print(f"[UYARI] {randevu_id} numaralı randevu bulunamadı.")



def gelir_kar_hesapla(randevular):
    print("\n" + "=" * 60)
    print("      GELİR VE KAR ANALİZ RAPORRU")
    print("=" * 60)

    tamamlananlar =[r for r in randevular if r.durum == "Tamamlandı"]

    if not tamamlananlar:
        print("\nHenüz tamamlanmış bir randevu bulunmamaktadır.")
        return

    ucretler_dizisi = np.array([r.ucret for r in tamamlananlar], dtype = float)
    ortalama_ucret = np.mean(ucretler_dizisi)
    toplam_gelir = np.sum(ucretler_dizisi)

    maliyetler_dizisi = np.array([r.maliyet for r in tamamlananlar], dtype = float)
    toplam_maliyet = np.sum(maliyetler_dizisi)
    toplam_kar = toplam_gelir - toplam_maliyet
    kar_yuzdesi = (toplam_kar / toplam_gelir) * 100 if toplam_gelir > 0 else 0


    print(f"\n[GENEL ÖZET]")
    print(f"Tamamlanan Randevu Sayısı: {len(tamamlananlar)}")
    print(f"Toplam Gelir             : {toplam_gelir} TL")
    print(f"Toplam Maliyet           : {toplam_maliyet} TL")
    print(f"Net Kar                  : {toplam_kar} TL")
    print(f"Kar Yüzdesi              : %{kar_yuzdesi:.2f}")
    print(f"Ortalama Hizmet Ücreti   : {ortalama_ucret:.2f} TL")

    print("\n[HİZMET TÜRÜNE GÖRE DETAYLI ANALİZ]")
    veri_listesi = [
        {
            "Hizmet Türü": r.hizmet_turu,
            "Hizmet Adı": r.hizmet_adi,
            "Ücret": r.ucret,
            "Maliyet": r.maliyet,
            "Kar": r.kar_hesapla()
        }
        for r in tamamlananlar
    ]

    df = pd.DataFrame(veri_listesi)

    ozet_tablo = df.groupby("Hizmet Türü").agg(
        Tamamlanan_Randevu = ("Ücret", "count"),
        Toplam_Gelir_TL = ("Ücret", "sum"),
        Toplam_Kar_TL = ("Kar", "sum")
    ).reset_index()

    ozet_tablo["Kar_Yuzdesi_%"] = ((ozet_tablo["Toplam_Kar_TL"] / ozet_tablo["Toplam_Gelir_TL"]) * 100).round(2)

    print("-" * 70)
    print(ozet_tablo.to_string(index = False))
    print("-" * 70)



def ana_menu():
    randevular = randevulari_yukle()

    while True:
        print("\n" + "=" * 45)
        print(" SAĞLIKLI YAŞAM MERKEZİ RANDEVU SİSTEMİ")
        print("=" * 45)
        print("1. Randevuları Listele")
        print("2. Yeni Rnadevu Ekle")
        print("3. Randevu Ara")
        print("4. Randevu Tamamla")
        print("5. Randevu İptal Et")
        print("6. Gelir ve Kar Analizi")
        print("0. Çıkış")
        print("=" * 45)

        secim = input("Yapmak istediğiniz işlemi seçiniz (0-6): ").strip()

        try:
            if secim =="1":
                randevulari_listele(randevular)
            
            elif secim == "2":
                randevu_ekle(randevular)
            
            elif secim == "3":
                randevu_ara(randevular)

            elif secim == "4":
                randevu_tamamla(randevular)

            elif secim == "5":
                randevu_iptal_et(randevular)

            elif secim == "6":
                gelir_kar_hesapla(randevular)

            elif secim == "0":
                print("\nProgramdan çıkılıyor. Sağlıklı Günler Dileriz!")
                break

            else:
                print("\n[UYARI] Lütfen 0 ile 6 arasında bir rakam giriniz.")
        
        except Exception as hata:
            print(f"\n[BEKLENMEYEN HATA] Sir sorun oluştu: {hata}")

if __name__ == "__main__":
    ana_menu()
