from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QMessageBox, QGroupBox, QHeaderView, QInputDialog, QFrame, QLabel)
from UI.icons import get_icon
from BLL import kargo_logic

class BasePage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.card = QFrame()
        self.card.setObjectName("content_card")
        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setContentsMargins(20, 20, 20, 20)
        self.layout.addWidget(self.card)

# --- 1. MÜŞTERİ PAGE ---
class MusteriPage(BasePage):
    def __init__(self):
        super().__init__()
        # Toolbar
        toolbar = QHBoxLayout()
        self.btn_yeni = QPushButton(" Yeni Ekle"); self.btn_yeni.setIcon(get_icon("add"))
        self.btn_guncelle = QPushButton(" Düzenle"); self.btn_guncelle.setIcon(get_icon("edit"))
        self.btn_sil = QPushButton(" Sil"); self.btn_sil.setIcon(get_icon("delete")); self.btn_sil.setObjectName("btn_sil")
        self.btn_yenile = QPushButton(" Yenile"); self.btn_yenile.setIcon(get_icon("refresh"))
        for btn in [self.btn_yeni, self.btn_guncelle, self.btn_sil, self.btn_yenile]: toolbar.addWidget(btn)
        toolbar.addStretch()
        self.card_layout.addLayout(toolbar)

        # Form
        self.grup_form = QGroupBox("Müşteri Formu"); self.grup_form.hide()
        form_layout = QHBoxLayout(self.grup_form)
        self.txt_id = QLineEdit(); self.txt_id.setPlaceholderText("ID")
        self.txt_ad = QLineEdit(); self.txt_ad.setPlaceholderText("Ad")
        self.txt_soyad = QLineEdit(); self.txt_soyad.setPlaceholderText("Soyad")
        self.txt_tel = QLineEdit(); self.txt_tel.setPlaceholderText("Telefon")
        self.txt_mail = QLineEdit(); self.txt_mail.setPlaceholderText("Mail")
        self.txt_ulke = QLineEdit(); self.txt_ulke.setPlaceholderText("Ülke")
        for w in [self.txt_id, self.txt_ad, self.txt_soyad, self.txt_tel, self.txt_mail, self.txt_ulke]: form_layout.addWidget(w)
        self.btn_kaydet = QPushButton("Kaydet"); self.btn_kaydet.setObjectName("btn_kaydet")
        self.btn_iptal = QPushButton("İptal")
        form_layout.addWidget(self.btn_kaydet); form_layout.addWidget(self.btn_iptal)
        self.card_layout.addWidget(self.grup_form)

        # Table
        self.tablo = QTableWidget(); self.tablo.setColumnCount(6)
        self.tablo.setHorizontalHeaderLabels(["ID", "Müşteri Adı", "Soyad", "Telefon", "Mail", "Ülke"])
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tablo.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tablo.verticalHeader().setVisible(False)
        self.card_layout.addWidget(self.tablo)

        self.btn_yeni.clicked.connect(lambda: self.goster_form("EKLE")); self.btn_guncelle.clicked.connect(lambda: self.goster_form("GUNCELLE"))
        self.btn_iptal.clicked.connect(self.grup_form.hide); self.btn_kaydet.clicked.connect(self.kaydet)
        self.btn_sil.clicked.connect(self.sil); self.btn_yenile.clicked.connect(self.yenile)
        self.mod = "EKLE"; self.yenile()

    def goster_form(self, mod):
        self.mod = mod; self.txt_id.setEnabled(mod == "EKLE")
        if mod == "EKLE": [w.clear() for w in [self.txt_id, self.txt_ad, self.txt_soyad, self.txt_tel, self.txt_mail, self.txt_ulke]]
        else:
            s = self.tablo.currentRow()
            if s < 0: return QMessageBox.warning(self, "Uyarı", "Lütfen bir kayıt seçin!")
            self.txt_id.setText(self.tablo.item(s,0).text()); self.txt_ad.setText(self.tablo.item(s,1).text())
            self.txt_soyad.setText(self.tablo.item(s,2).text()); self.txt_tel.setText(self.tablo.item(s,3).text())
            self.txt_mail.setText(self.tablo.item(s,4).text()); self.txt_ulke.setText(self.tablo.item(s,5).text())
        self.grup_form.show()

    def kaydet(self):
        d = [self.txt_id.text(), self.txt_ad.text(), self.txt_soyad.text(), self.txt_tel.text(), self.txt_mail.text(), self.txt_ulke.text()]
        b, m = kargo_logic.musteri_kaydet_bll(*d) if self.mod == "EKLE" else kargo_logic.musteri_guncelle_bll(*d)
        if b: QMessageBox.information(self, "Başarılı", m); self.grup_form.hide(); self.yenile()
        else: QMessageBox.warning(self, "Hata", m)

    def sil(self):
        s = self.tablo.currentRow()
        if s < 0: return QMessageBox.warning(self, "Uyarı", "Lütfen silinecek satırı seçin!")
        
        # PERBAIKAN: Menambahkan tombol YES dan NO
        cevap = QMessageBox.question(self, "Onay", "Seçili müşteriyi silmek istediğinize emin misiniz?", 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if cevap == QMessageBox.StandardButton.Yes:
            if kargo_logic.musteri_sil_bll(self.tablo.item(s,0).text())[0]: 
                self.yenile()

    def yenile(self):
        b, v = kargo_logic.musteri_getir_bll()
        if b:
            self.tablo.setRowCount(0)
            for i, row in enumerate(v):
                self.tablo.insertRow(i)
                for j, val in enumerate(row): self.tablo.setItem(i, j, QTableWidgetItem(str(val)))


# --- 2. GÖNDERİ PAGE ---
class GonderiPage(BasePage):
    def __init__(self):
        super().__init__()
        toolbar = QHBoxLayout()
        self.btn_yeni = QPushButton(" Yeni Ekle"); self.btn_yeni.setIcon(get_icon("add"))
        self.btn_guncelle = QPushButton(" Düzenle"); self.btn_guncelle.setIcon(get_icon("edit"))
        self.btn_sil = QPushButton(" Sil"); self.btn_sil.setIcon(get_icon("delete")); self.btn_sil.setObjectName("btn_sil")
        self.btn_yenile = QPushButton(" Yenile"); self.btn_yenile.setIcon(get_icon("refresh"))
        for btn in [self.btn_yeni, self.btn_guncelle, self.btn_sil, self.btn_yenile]: toolbar.addWidget(btn)
        toolbar.addStretch()
        self.card_layout.addLayout(toolbar)

        self.grup_form = QGroupBox("Kargo Detayları"); self.grup_form.hide()
        form_layout = QHBoxLayout(self.grup_form)
        self.txt_id = QLineEdit(); self.txt_id.setPlaceholderText("Kargo ID")
        self.txt_mid = QLineEdit(); self.txt_mid.setPlaceholderText("Müşteri ID")
        self.txt_cikis = QLineEdit(); self.txt_cikis.setPlaceholderText("Çıkış Şubesi ID")
        self.txt_varis = QLineEdit(); self.txt_varis.setPlaceholderText("Varış Adresi ID")
        self.txt_kg = QLineEdit(); self.txt_kg.setPlaceholderText("Ağırlık (kg)")
        self.txt_durum = QLineEdit(); self.txt_durum.setPlaceholderText("Durum")
        for w in [self.txt_id, self.txt_mid, self.txt_cikis, self.txt_varis, self.txt_kg, self.txt_durum]: form_layout.addWidget(w)
        self.btn_kaydet = QPushButton("Kaydet"); self.btn_kaydet.setObjectName("btn_kaydet")
        self.btn_iptal = QPushButton("İptal")
        form_layout.addWidget(self.btn_kaydet); form_layout.addWidget(self.btn_iptal)
        self.card_layout.addWidget(self.grup_form)

        self.tablo = QTableWidget(); self.tablo.setColumnCount(8)
        self.tablo.setHorizontalHeaderLabels(["Kargo ID", "Müşteri", "Çıkış Şubesi", "Varış Adresi", "Ağırlık (kg)", "Ücret (₺)", "Durum", "Tarih"])
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tablo.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tablo.verticalHeader().setVisible(False)
        self.card_layout.addWidget(self.tablo)

        self.btn_yeni.clicked.connect(lambda: self.goster_form("EKLE")); self.btn_guncelle.clicked.connect(lambda: self.goster_form("GUNCELLE"))
        self.btn_iptal.clicked.connect(self.grup_form.hide); self.btn_kaydet.clicked.connect(self.kaydet)
        self.btn_sil.clicked.connect(self.sil); self.btn_yenile.clicked.connect(self.yenile)
        self.mod = "EKLE"; self.yenile()

    def goster_form(self, mod):
        self.mod = mod; self.txt_id.setEnabled(mod == "EKLE")
        if mod == "EKLE": [w.clear() for w in [self.txt_id, self.txt_mid, self.txt_cikis, self.txt_varis, self.txt_kg]]; self.txt_durum.setText("Beklemede")
        else:
            s = self.tablo.currentRow()
            if s < 0: return QMessageBox.warning(self, "Uyarı", "Lütfen bir kayıt seçin!")
            self.txt_id.setText(self.tablo.item(s,0).text()); self.txt_mid.setText(self.tablo.item(s,1).text())
            self.txt_cikis.setText(self.tablo.item(s,2).text()); self.txt_varis.setText(self.tablo.item(s,3).text())
            self.txt_kg.setText(self.tablo.item(s,4).text()); self.txt_durum.setText(self.tablo.item(s,6).text())
        self.grup_form.show()

    def kaydet(self):
        d = [self.txt_id.text(), self.txt_mid.text(), self.txt_cikis.text(), self.txt_varis.text(), self.txt_kg.text(), self.txt_durum.text()]
        b, m = kargo_logic.gonderi_kaydet_bll(*d) if self.mod == "EKLE" else kargo_logic.gonderi_guncelle_bll(*d)
        if b: QMessageBox.information(self, "Başarılı", m); self.grup_form.hide(); self.yenile()
        else: QMessageBox.warning(self, "Hata", m)

    def sil(self):
        s = self.tablo.currentRow()
        if s < 0: return QMessageBox.warning(self, "Uyarı", "Lütfen silinecek satırı seçin!")
        
        # PERBAIKAN: Menambahkan tombol YES dan NO
        cevap = QMessageBox.question(self, "Onay", "Seçili kargoyu silmek istediğinize emin misiniz?", 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if cevap == QMessageBox.StandardButton.Yes:
            if kargo_logic.gonderi_sil_bll(self.tablo.item(s,0).text())[0]: 
                self.yenile()

    def yenile(self):
        b, v = kargo_logic.gonderi_getir_bll()
        if b:
            self.tablo.setRowCount(0)
            for i, row in enumerate(v):
                self.tablo.insertRow(i)
                for j, val in enumerate(row): self.tablo.setItem(i, j, QTableWidgetItem(str(val)))


# --- 3. ŞUBE PAGE ---
class SubePage(BasePage):
    def __init__(self):
        super().__init__()
        toolbar = QHBoxLayout()
        self.btn_yeni = QPushButton(" Yeni Ekle"); self.btn_yeni.setIcon(get_icon("add"))
        self.btn_guncelle = QPushButton(" Düzenle"); self.btn_guncelle.setIcon(get_icon("edit"))
        self.btn_sil = QPushButton(" Sil"); self.btn_sil.setIcon(get_icon("delete")); self.btn_sil.setObjectName("btn_sil")
        self.btn_yenile = QPushButton(" Yenile"); self.btn_yenile.setIcon(get_icon("refresh"))
        for btn in [self.btn_yeni, self.btn_guncelle, self.btn_sil, self.btn_yenile]: toolbar.addWidget(btn)
        toolbar.addStretch()
        self.card_layout.addLayout(toolbar)

        self.grup_form = QGroupBox("Şube Formu"); self.grup_form.hide()
        form_layout = QHBoxLayout(self.grup_form)
        self.txt_id = QLineEdit(); self.txt_id.setPlaceholderText("Şube ID")
        self.txt_ad = QLineEdit(); self.txt_ad.setPlaceholderText("Şube Adı")
        self.txt_ulke = QLineEdit(); self.txt_ulke.setPlaceholderText("Ülke")
        self.txt_sehir = QLineEdit(); self.txt_sehir.setPlaceholderText("Şehir")
        for w in [self.txt_id, self.txt_ad, self.txt_ulke, self.txt_sehir]: form_layout.addWidget(w)
        self.btn_kaydet = QPushButton("Kaydet"); self.btn_kaydet.setObjectName("btn_kaydet")
        self.btn_iptal = QPushButton("İptal")
        form_layout.addWidget(self.btn_kaydet); form_layout.addWidget(self.btn_iptal)
        self.card_layout.addWidget(self.grup_form)

        self.tablo = QTableWidget(); self.tablo.setColumnCount(4)
        self.tablo.setHorizontalHeaderLabels(["Şube ID", "Şube Adı", "Ülke", "Şehir"])
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tablo.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tablo.verticalHeader().setVisible(False)
        self.card_layout.addWidget(self.tablo)

        self.btn_yeni.clicked.connect(lambda: self.goster_form("EKLE")); self.btn_guncelle.clicked.connect(lambda: self.goster_form("GUNCELLE"))
        self.btn_iptal.clicked.connect(self.grup_form.hide); self.btn_kaydet.clicked.connect(self.kaydet)
        self.btn_sil.clicked.connect(self.sil); self.btn_yenile.clicked.connect(self.yenile)
        self.mod = "EKLE"; self.yenile()

    def goster_form(self, mod):
        self.mod = mod; self.txt_id.setEnabled(mod == "EKLE")
        if mod == "EKLE": [w.clear() for w in [self.txt_id, self.txt_ad, self.txt_ulke, self.txt_sehir]]
        else:
            s = self.tablo.currentRow()
            if s < 0: return QMessageBox.warning(self, "Uyarı", "Lütfen bir kayıt seçin!")
            self.txt_id.setText(self.tablo.item(s,0).text()); self.txt_ad.setText(self.tablo.item(s,1).text())
            self.txt_ulke.setText(self.tablo.item(s,2).text()); self.txt_sehir.setText(self.tablo.item(s,3).text())
        self.grup_form.show()

    def kaydet(self):
        d = [self.txt_id.text(), self.txt_ad.text(), self.txt_ulke.text(), self.txt_sehir.text()]
        b, m = kargo_logic.sube_kaydet_bll(*d) if self.mod == "EKLE" else kargo_logic.sube_guncelle_bll(*d)
        if b: QMessageBox.information(self, "Başarılı", m); self.grup_form.hide(); self.yenile()
        else: QMessageBox.warning(self, "Hata", m)

    def sil(self):
        s = self.tablo.currentRow()
        if s < 0: return QMessageBox.warning(self, "Uyarı", "Lütfen silinecek satırı seçin!")
        
        # PERBAIKAN: Menambahkan tombol YES dan NO
        cevap = QMessageBox.question(self, "Onay", "Seçili şubeyi silmek istediğinize emin misiniz?", 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if cevap == QMessageBox.StandardButton.Yes:
            if kargo_logic.sube_sil_bll(self.tablo.item(s,0).text())[0]: 
                self.yenile()

    def yenile(self):
        b, v = kargo_logic.sube_getir_bll()
        if b:
            self.tablo.setRowCount(0)
            for i, row in enumerate(v):
                self.tablo.insertRow(i)
                for j, val in enumerate(row): self.tablo.setItem(i, j, QTableWidgetItem(str(val)))


# --- 4. HAREKET PAGE ---
class HareketPage(BasePage):
    def __init__(self):
        super().__init__()
        toolbar = QHBoxLayout()
        self.txt_gid_sorgu = QLineEdit(); self.txt_gid_sorgu.setPlaceholderText("Gönderi ID Girin..."); self.txt_gid_sorgu.setFixedWidth(200)
        self.btn_ara = QPushButton(" Sorgula"); self.btn_ara.setObjectName("btn_kaydet")
        
        self.btn_yeni = QPushButton(" Yeni Ekle"); self.btn_yeni.setIcon(get_icon("add"))
        self.btn_sil = QPushButton(" Sil"); self.btn_sil.setIcon(get_icon("delete")); self.btn_sil.setObjectName("btn_sil")
        
        for w in [self.txt_gid_sorgu, self.btn_ara, self.btn_yeni, self.btn_sil]: toolbar.addWidget(w)
        toolbar.addStretch()
        self.card_layout.addLayout(toolbar)

        self.grup_form = QGroupBox("Hareket Kaydı Ekle"); self.grup_form.hide()
        form_layout = QHBoxLayout(self.grup_form)
        self.txt_id = QLineEdit(); self.txt_id.setPlaceholderText("Hareket ID")
        self.txt_gid = QLineEdit(); self.txt_gid.setPlaceholderText("Gönderi ID")
        self.txt_sid = QLineEdit(); self.txt_sid.setPlaceholderText("Şube ID")
        self.txt_durum = QLineEdit(); self.txt_durum.setPlaceholderText("Durum (Örn: Yolda)")
        for w in [self.txt_id, self.txt_gid, self.txt_sid, self.txt_durum]: form_layout.addWidget(w)
        self.btn_kaydet = QPushButton("Kaydet"); self.btn_kaydet.setObjectName("btn_kaydet")
        self.btn_iptal = QPushButton("İptal")
        form_layout.addWidget(self.btn_kaydet); form_layout.addWidget(self.btn_iptal)
        self.card_layout.addWidget(self.grup_form)

        # Add a hidden first column to store the Hareket ID so users can select rows to delete
        self.tablo = QTableWidget(); self.tablo.setColumnCount(4)
        self.tablo.setHorizontalHeaderLabels(["Hareket ID", "İşlem Tarihi", "Şube Adı", "Durum"])
        # hide the internal id column from the user
        self.tablo.setColumnHidden(0, True)
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tablo.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tablo.verticalHeader().setVisible(False)
        self.card_layout.addWidget(self.tablo)

        self.btn_ara.clicked.connect(self.ara)
        self.btn_yeni.clicked.connect(self.goster_form); self.btn_iptal.clicked.connect(self.grup_form.hide)
        self.btn_kaydet.clicked.connect(self.kaydet); self.btn_sil.clicked.connect(self.sil)

    def goster_form(self):
        [w.clear() for w in [self.txt_id, self.txt_gid, self.txt_sid, self.txt_durum]]
        self.grup_form.show()

    def ara(self):
        g_id = self.txt_gid_sorgu.text()
        if not g_id: return QMessageBox.warning(self, "Uyarı", "Lütfen bir Gönderi ID girin!")
        b, v = kargo_logic.hareket_getir_bll(g_id)
        if b:
            self.tablo.setRowCount(0)
            for i, row in enumerate(v):
                self.tablo.insertRow(i)
                # Expect row to contain the hareket id as first element. Store it in hidden col 0.
                # Then put the remaining values into visible columns 1..n
                try:
                    h_id = row[0]
                    rest = row[1:]
                except Exception:
                    # Fallback if row is shorter/structured differently
                    h_id = ""
                    rest = row

                self.tablo.setItem(i, 0, QTableWidgetItem(str(h_id)))
                for j, val in enumerate(rest):
                    # put into column index offset by 1
                    self.tablo.setItem(i, j+1, QTableWidgetItem(str(val)))
        else: QMessageBox.critical(self, "Hata", str(v))

    def kaydet(self):
        b, m = kargo_logic.hareket_kaydet_bll(self.txt_id.text(), self.txt_gid.text(), self.txt_sid.text(), self.txt_durum.text())
        if b: QMessageBox.information(self, "Başarılı", m); self.grup_form.hide(); self.ara()
        else: QMessageBox.warning(self, "Hata", m)

    def sil(self):
        # Delete the selected row's hareket using its hidden ID column
        s = self.tablo.currentRow()
        if s < 0: return QMessageBox.warning(self, "Uyarı", "Lütfen silinecek satırı seçin!")

        cevap = QMessageBox.question(self, "Onay", "Seçili hareketi silmek istediğinize emin misiniz?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if cevap == QMessageBox.StandardButton.Yes:
            item = self.tablo.item(s, 0)
            h_id = item.text() if item else None
            if not h_id:
                return QMessageBox.warning(self, "Hata", "Hareket ID bulunamadı!")
            if kargo_logic.hareket_sil_bll(h_id)[0]:
                self.ara()