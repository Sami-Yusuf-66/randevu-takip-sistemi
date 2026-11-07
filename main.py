import json
import os
from datetime import datetime
import numpy as np
import pandas as pd

doya_yolu = os.path.join(os.path.dirname(__file__), "randevular.json")

hizmetler = {
    "1": {"ad": "Diyetisyen", "tur": "Beslenme", "ucret": 800, "maliyet": 250},
    "2": {"ad": "Fizyoterapi", "tur": "Tedavi", "ucret": 600, "maliyet": 200},
    "3": {"ad": "Masaj", "tur": "Spa", "ucret": 400, "maliyet": 100},
    "4": {"ad": "Fitness", "tur": "Spor", "ucret": 300, "maliyet": 100},
    "5": {"ad": "Cilt Bakimi", "tur": "Bakim", "ucret": 700, "maliyet": 250}
}


class TemelRandevu:
    def __init__(self, randevu_id, musteri_adi, tarih, saat, ucret, maliyet, durum = "Bekliyor"):
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
    def __init__(self, randevu_id, musteri_adi, hizmet_adi, hizmet_turu, tarih, saat, ucret, maliyet, durum = "Bekliyor"):
        
        super().__init__(randevu_id, musteri_adi, hizmet_adi, hizmet_turu, tarih, saat, ucret, maliyet, durum)
        self.hizmet_adi = hizmet_adi
        self.hizmet_turu = hizmet_turu

    def to_dict(self):
        return {
            "id": self.randevu_id,
            "musteri_adi": self.musteri_adi,
            "hizmet_adi": self.hizmet_adi,
            "hizmet_turu": self.hizmet_turu,
            "tarih": self.tarih,
            "saat": self.tarih,
            "ucret": self.ucret,
            "maliyet": self.maliyet,
            "durum": self.durum
        }

    @classmethod
    def from_dict(cls, veri):
        return cls(
            randevu_id = veri["id"],
            musteri_adi = veri["musteri_adi"],
            hizmet_adi = veri["hizmet_adi"],
            hizmet_turu = veri["hizmet_turu"],
            tarih = veri["tarih"],
            saat = veri["saat"],
            ucret = veri["ucret"],
            maliyet = veri.get("maliyet", veri["ucret"] * 0.3),
            durum = veri.get("durum", "Bekliyor")
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

