import mysql.connector

def baglanti_olustur():
    return mysql.connector.connect(host="localhost", user="root", password="asyraf12345", database="globalroute_db", use_pure=True)

# --- 1. MÜŞTERİ DAL ---
def musteri_ekle_dal(m_id, ad, soyad, tel, mail, ulke):
    conn = None; cursor = None  
    try:
        conn = baglanti_olustur(); cursor = conn.cursor()
        cursor.callproc('sp_MusteriEkle', (m_id, ad, soyad, tel, mail, ulke)); conn.commit(); return True, "Müşteri eklendi."
    except Exception as e: return False, f"Hata: {str(e)}"
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()
def musteri_guncelle_dal(m_id, ad, soyad, tel, mail, ulke):
    conn = None; cursor = None  
    try:
        conn = baglanti_olustur(); cursor = conn.cursor()
        cursor.callproc('sp_MusteriGuncelle', (m_id, ad, soyad, tel, mail, ulke)); conn.commit(); return True, "Müşteri güncellendi."
    except Exception as e: return False, f"Hata: {str(e)}"
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()
def musteri_sil_dal(m_id):
    conn = None; cursor = None  
    try:
        conn = baglanti_olustur(); cursor = conn.cursor()
        cursor.callproc('sp_MusteriSil', (m_id,)); conn.commit(); return True, "Müşteri silindi."
    except Exception as e: return False, f"Hata: {str(e)}"
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()
def musteri_listele_dal():
    conn = None; cursor = None
    try:
        conn = baglanti_olustur(); cursor = conn.cursor()
        cursor.callproc('sp_MusteriListele'); sonuclar = []
        for result in cursor.stored_results(): sonuclar = result.fetchall()
        return True, sonuclar
    except Exception as e: return False, str(e)
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()

# --- 2. GÖNDERİ / KARGO DAL ---
def gonderi_ekle_dal(g_id, m_id, cikis, varis, agirlik, ucret, durum, tarih):
    conn = None; cursor = None
    try:
        conn = baglanti_olustur(); cursor = conn.cursor()
        cursor.callproc('sp_GonderiEkle', (g_id, m_id, cikis, varis, agirlik, ucret, durum, tarih)); conn.commit(); return True, "Kargo eklendi."
    except Exception as e: return False, f"Hata: {str(e)}"
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()
def gonderi_guncelle_dal(g_id, agirlik, ucret, durum):
    conn = None; cursor = None
    try:
        conn = baglanti_olustur(); cursor = conn.cursor()
        # HANYA MENGIRIM 4 DATA SESUAI PERMINTAAN MYSQL
        cursor.callproc('sp_GonderiGuncelle', (g_id, agirlik, ucret, durum))
        conn.commit()
        return True, "Kargo güncellendi."
    except Exception as e: return False, f"Hata: {str(e)}"
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()
    conn = None; cursor = None
    try:
        conn = baglanti_olustur(); cursor = conn.cursor()
        cursor.callproc('sp_GonderiGuncelle', (g_id, m_id, cikis, varis, agirlik, ucret, durum)); conn.commit(); return True, "Kargo güncellendi."
    except Exception as e: return False, f"Hata: {str(e)}"
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()
def gonderi_sil_dal(g_id):
    conn = None; cursor = None
    try:
        conn = baglanti_olustur(); cursor = conn.cursor()
        cursor.callproc('sp_GonderiSil', (g_id,)); conn.commit(); return True, "Kargo silindi."
    except Exception as e: return False, f"Hata: {str(e)}"
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()
def gonderi_listele_dal():
    conn = None; cursor = None
    try:
        conn = baglanti_olustur(); cursor = conn.cursor()
        cursor.callproc('sp_GonderiListeleDetay'); sonuclar = []
        for result in cursor.stored_results(): sonuclar = result.fetchall()
        return True, sonuclar
    except Exception as e: return False, str(e)
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()

# --- 3. ŞUBE DAL ---
def sube_ekle_dal(s_id, ad, ulke, sehir):
    conn = None; cursor = None  
    try:
        conn = baglanti_olustur(); cursor = conn.cursor()
        cursor.callproc('sp_SubeEkle', (s_id, ad, ulke, sehir)); conn.commit(); return True, "Şube eklendi."
    except Exception as e: return False, f"Hata: {str(e)}"
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()
def sube_guncelle_dal(s_id, ad, ulke, sehir):
    conn = None; cursor = None  
    try:
        conn = baglanti_olustur(); cursor = conn.cursor()
        cursor.callproc('sp_SubeGuncelle', (s_id, ad, ulke, sehir)); conn.commit(); return True, "Şube güncellendi."
    except Exception as e: return False, f"Hata: {str(e)}"
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()
def sube_sil_dal(s_id):
    conn = None; cursor = None  
    try:
        conn = baglanti_olustur(); cursor = conn.cursor()
        cursor.callproc('sp_SubeSil', (s_id,)); conn.commit(); return True, "Şube silindi."
    except Exception as e: return False, f"Hata: {str(e)}"
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()
def sube_listele_dal():
    conn = None; cursor = None
    try:
        conn = baglanti_olustur(); cursor = conn.cursor()
        cursor.callproc('sp_SubeListele'); sonuclar = []
        for result in cursor.stored_results(): sonuclar = result.fetchall()
        return True, sonuclar
    except Exception as e: return False, str(e)
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()

# --- 4. KARGO HAREKETLERİ DAL ---
def hareket_ekle_dal(h_id, g_id, s_id, durum, tarih):
    conn = None; cursor = None  
    try:
        conn = baglanti_olustur(); cursor = conn.cursor()
        cursor.callproc('sp_HareketEkle', (h_id, g_id, s_id, durum, tarih)); conn.commit(); return True, "Hareket eklendi."
    except Exception as e: return False, f"Hata: {str(e)}"
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()
def hareket_sil_dal(h_id):
    conn = None; cursor = None  
    try:
        conn = baglanti_olustur(); cursor = conn.cursor()
        cursor.callproc('sp_HareketSil', (h_id,)); conn.commit(); return True, "Hareket silindi."
    except Exception as e: return False, f"Hata: {str(e)}"
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()
def hareket_listele_dal(g_id):
    conn = None; cursor = None
    try:
        conn = baglanti_olustur(); cursor = conn.cursor()
        cursor.callproc('sp_GonderiHareketleri', (g_id,)); sonuclar = []
        for result in cursor.stored_results(): sonuclar = result.fetchall()
        return True, sonuclar
    except Exception as e: return False, str(e)
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()