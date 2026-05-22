from DAL import kargo_dal
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# ==========================================
# FUNGSI RAHASIA: KALKULASI JARAK OTOMATIS
# ==========================================
def hitung_ucret_otomatis(cikis, varis, agirlik_float):
    tarif_dasar = 150.0
    tarif_per_kg = 15.0 # 15 Lira per KG
    tarif_per_km = 3.5  # 3.5 Lira per Kilometer
    
    biaya_berat = agirlik_float * tarif_per_kg
    
    try:
        # Menghubungi satelit/OpenStreetMap
        geolocator = Nominatim(user_agent="GlobalRouteLojistik_App")
        lokasi_asal = geolocator.geocode(cikis, timeout=3)
        lokasi_tujuan = geolocator.geocode(varis, timeout=3)
        
        # Jika kedua kota ditemukan di peta dunia
        if lokasi_asal and lokasi_tujuan:
            koordinat_asal = (lokasi_asal.latitude, lokasi_asal.longitude)
            koordinat_tujuan = (lokasi_tujuan.latitude, lokasi_tujuan.longitude)
            
            # Hitung jarak asli dalam Kilometer
            jarak_km = geodesic(koordinat_asal, koordinat_tujuan).kilometers
            
            # Rumus Baru: Dasar + Berat + Jarak
            biaya_jarak = jarak_km * tarif_per_km
            total_ucret = tarif_dasar + biaya_berat + biaya_jarak
            return round(total_ucret, 2)
            
        else:
            # Fallback 1: Kota tidak dikenali (Typo/Fiktif), pakai rumus lama
            return round(tarif_dasar + (agirlik_float * 45.5), 2)
            
    except Exception:
        # Fallback 2: Tidak ada internet saat presentasi, pakai rumus lama
        return round(tarif_dasar + (agirlik_float * 45.5), 2)

# ==========================================
# 1. MÜŞTERİ BLL
# ==========================================
def musteri_kaydet_bll(m_id, ad, soyad, tel, mail, ulke):
    if not m_id or not ad: return False, "Hata: ID ve Ad boş bırakılamaz!"
    return kargo_dal.musteri_ekle_dal(m_id, ad, soyad, tel, mail, ulke)
def musteri_guncelle_bll(m_id, ad, soyad, tel, mail, ulke):
    if not m_id or not ad: return False, "Hata: ID ve Ad boş bırakılamaz!"
    return kargo_dal.musteri_guncelle_dal(m_id, ad, soyad, tel, mail, ulke)
def musteri_sil_bll(m_id):
    if not m_id: return False, "Hata: ID bulunamadı!"
    return kargo_dal.musteri_sil_dal(m_id)
def musteri_getir_bll(): return kargo_dal.musteri_listele_dal()

# ==========================================
# 2. GÖNDERİ (KARGO) BLL
# ==========================================
def gonderi_kaydet_bll(g_id, m_id, cikis, varis, agirlik, durum="Beklemede"):
    if not g_id or not m_id: return False, "Hata: ID bilgileri eksik!"
    try: agirlik_float = float(agirlik)
    except ValueError: return False, "Hata: Ağırlık sayısal olmalıdır!"
    
    # Panggil AI Penghitung Jarak
    ucret = hitung_ucret_otomatis(cikis, varis, agirlik_float)
    
    tarih = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return kargo_dal.gonderi_ekle_dal(g_id, m_id, cikis, varis, agirlik_float, ucret, durum, tarih)

def gonderi_guncelle_bll(g_id, m_id, cikis, varis, agirlik, durum):
    if not g_id: return False, "Hata: Kargo ID eksik!"
    try: agirlik_float = float(agirlik)
    except ValueError: return False, "Hata: Ağırlık sayısal olmalıdır!"
    
    # Hitung ulang harga jika beratnya berubah (tetap memanggil AI Penghitung Jarak)
    ucret = hitung_ucret_otomatis(cikis, varis, agirlik_float)
    
    # HANYA MENGIRIM 4 DATA KE DAL (g_id, agirlik, ucret, durum)
    return kargo_dal.gonderi_guncelle_dal(g_id, agirlik_float, ucret, durum)
    if not g_id or not m_id: return False, "Hata: ID bilgileri eksik!"
    try: agirlik_float = float(agirlik)
    except ValueError: return False, "Hata: Ağırlık sayısal olmalıdır!"
    
    # Panggil AI Penghitung Jarak
    ucret = hitung_ucret_otomatis(cikis, varis, agirlik_float)
    
    return kargo_dal.gonderi_guncelle_dal(g_id, m_id, cikis, varis, agirlik_float, ucret, durum)

def gonderi_sil_bll(g_id):
    if not g_id: return False, "Hata: Kargo ID bulunamadı!"
    return kargo_dal.gonderi_sil_dal(g_id)
def gonderi_getir_bll(): return kargo_dal.gonderi_listele_dal()

# ==========================================
# 3. ŞUBE BLL
# ==========================================
def sube_kaydet_bll(s_id, ad, ulke, sehir):
    if not s_id or not ad: return False, "Hata: Şube ID ve Ad eksik!"
    return kargo_dal.sube_ekle_dal(s_id, ad, ulke, sehir)
def sube_guncelle_bll(s_id, ad, ulke, sehir):
    if not s_id or not ad: return False, "Hata: Şube ID ve Ad eksik!"
    return kargo_dal.sube_guncelle_dal(s_id, ad, ulke, sehir)
def sube_sil_bll(s_id):
    if not s_id: return False, "Hata: Şube ID bulunamadı!"
    return kargo_dal.sube_sil_dal(s_id)
def sube_getir_bll(): return kargo_dal.sube_listele_dal()

# ==========================================
# 4. HAREKET BLL
# ==========================================
def hareket_kaydet_bll(h_id, g_id, s_id, durum):
    if not h_id or not g_id or not s_id: return False, "Hata: Tüm ID alanları doldurulmalı!"
    tarih = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return kargo_dal.hareket_ekle_dal(h_id, g_id, s_id, durum, tarih)
def hareket_sil_bll(h_id):
    if not h_id: return False, "Hata: Hareket ID bulunamadı!"
    return kargo_dal.hareket_sil_dal(h_id)
def hareket_getir_bll(g_id): 
    if not g_id: return False, "Gönderi ID Girilmelidir!"
    return kargo_dal.hareket_listele_dal(g_id)