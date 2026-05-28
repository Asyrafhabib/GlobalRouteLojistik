from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QMessageBox, QHeaderView, QFrame, QDialog, QFormLayout, QLabel, QComboBox)
from PyQt6.QtCore import Qt
from UI.icons import get_icon
from BLL import kargo_logic

MODAL_STYLE = """
QDialog { background-color: #1E293B; }
QLabel { font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; font-weight: 600; color: #F8FAFC; }
QLineEdit { background-color: #0F172A; border: 1px solid #334155; border-radius: 8px; padding: 10px 14px; color: #F8FAFC; font-size: 13px; }
QLineEdit:focus { border: 2px solid #3B82F6; background-color: #0F172A; }
QPushButton { font-family: 'Segoe UI', Arial, sans-serif; font-weight: bold; font-size: 13px; border-radius: 8px; padding: 10px 20px; }
QPushButton#btn_iptal { background-color: #334155; color: #F8FAFC; border: 1px solid #475569; }
QPushButton#btn_iptal:hover { background-color: #475569; }
QPushButton#btn_kaydet { background-color: #2563EB; color: #FFFFFF; border: none; }
QPushButton#btn_kaydet:hover { background-color: #1D4ED8; }
"""

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
        toolbar = QHBoxLayout()
        self.btn_yeni = QPushButton(" Yeni Ekle"); self.btn_yeni.setIcon(get_icon("add"))
        self.btn_guncelle = QPushButton(" Düzenle"); self.btn_guncelle.setIcon(get_icon("edit"))
        self.btn_sil = QPushButton(" Sil"); self.btn_sil.setIcon(get_icon("delete")); self.btn_sil.setObjectName("btn_sil")
        self.btn_yenile = QPushButton(" Yenile"); self.btn_yenile.setIcon(get_icon("refresh"))
        for btn in [self.btn_yeni, self.btn_guncelle, self.btn_sil, self.btn_yenile]: toolbar.addWidget(btn)
        toolbar.addStretch()
        self.card_layout.addLayout(toolbar)

        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Müşteri İşlemleri")
        self.dialog.setModal(True)
        self.dialog.setFixedSize(450, 460)
        self.dialog.setStyleSheet(MODAL_STYLE)
        dialog_layout = QVBoxLayout(self.dialog)
        dialog_layout.setContentsMargins(30, 30, 30, 30)
        dialog_layout.setSpacing(15)

        title_label = QLabel("👥 Müşteri Detayları")
        title_label.setStyleSheet("font-size: 20px; font-weight: 800; color: #F8FAFC; margin-bottom: 10px;")
        dialog_layout.addWidget(title_label)

        self.txt_id = QLineEdit(); self.txt_ad = QLineEdit(); self.txt_soyad = QLineEdit()
        self.txt_tel = QLineEdit(); self.txt_mail = QLineEdit(); self.txt_ulke = QLineEdit()

        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.addRow("Müşteri ID:", self.txt_id); form_layout.addRow("Ad:", self.txt_ad)
        form_layout.addRow("Soyad:", self.txt_soyad); form_layout.addRow("Telefon:", self.txt_tel)
        form_layout.addRow("Mail:", self.txt_mail); form_layout.addRow("Ülke:", self.txt_ulke)
        dialog_layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.btn_iptal = QPushButton("İptal"); self.btn_iptal.setObjectName("btn_iptal")
        self.btn_kaydet = QPushButton("Kaydet"); self.btn_kaydet.setObjectName("btn_kaydet")
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_iptal); btn_layout.addWidget(self.btn_kaydet)
        dialog_layout.addLayout(btn_layout)

        self.tablo = QTableWidget(); self.tablo.setColumnCount(7) # Kolom ditambah 1 untuk "No."
        self.tablo.setHorizontalHeaderLabels(["No.", "ID", "Müşteri Adı", "Soyad", "Telefon", "Mail", "Ülke"])
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tablo.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.setAlternatingRowColors(True) # Efek warna selang-seling diaktifkan
        self.card_layout.addWidget(self.tablo)

        self.btn_yeni.clicked.connect(lambda: self.goster_form("EKLE")); self.btn_guncelle.clicked.connect(lambda: self.goster_form("GUNCELLE"))
        self.btn_iptal.clicked.connect(self.dialog.reject); self.btn_kaydet.clicked.connect(self.kaydet)
        self.btn_sil.clicked.connect(self.sil); self.btn_yenile.clicked.connect(self.yenile)
        self.mod = "EKLE"; self.yenile()

    def goster_form(self, mod):
        self.mod = mod; self.txt_id.setEnabled(mod == "EKLE")
        if mod == "EKLE": [w.clear() for w in [self.txt_id, self.txt_ad, self.txt_soyad, self.txt_tel, self.txt_mail, self.txt_ulke]]
        else:
            s = self.tablo.currentRow()
            if s < 0: return QMessageBox.warning(self, "Uyarı", "Lütfen bir kayıt seçin!")
            # Ambil data digeser 1 kolom karena kolom 0 sekarang adalah "No."
            self.txt_id.setText(self.tablo.item(s,1).text()); self.txt_ad.setText(self.tablo.item(s,2).text())
            self.txt_soyad.setText(self.tablo.item(s,3).text()); self.txt_tel.setText(self.tablo.item(s,4).text())
            self.txt_mail.setText(self.tablo.item(s,5).text()); self.txt_ulke.setText(self.tablo.item(s,6).text())
        self.dialog.exec()

    def kaydet(self):
        d = [self.txt_id.text(), self.txt_ad.text(), self.txt_soyad.text(), self.txt_tel.text(), self.txt_mail.text(), self.txt_ulke.text()]
        b, m = kargo_logic.musteri_kaydet_bll(*d) if self.mod == "EKLE" else kargo_logic.musteri_guncelle_bll(*d)
        if b: QMessageBox.information(self, "Başarılı", m); self.dialog.accept(); self.yenile()
        else: QMessageBox.warning(self, "Hata", m)

    def sil(self):
        s = self.tablo.currentRow()
        if s < 0: return QMessageBox.warning(self, "Uyarı", "Lütfen silinecek satırı seçin!")
        cevap = QMessageBox.question(self, "Onay", "Seçili müşteriyi silmek istediğinize emin misiniz?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if cevap == QMessageBox.StandardButton.Yes:
            if kargo_logic.musteri_sil_bll(self.tablo.item(s,1).text())[0]: self.yenile()

    def yenile(self):
        b, v = kargo_logic.musteri_getir_bll()
        if b:
            self.tablo.setRowCount(0)
            for i, row in enumerate(v):
                self.tablo.insertRow(i)
                # Sisipkan Penomoran (No.) di kolom 0, letakkan di tengah
                item_no = QTableWidgetItem(str(i + 1))
                item_no.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tablo.setItem(i, 0, item_no)
                
                # Masukkan data asli ke kolom selanjutnya
                for j, val in enumerate(row): 
                    self.tablo.setItem(i, j + 1, QTableWidgetItem(str(val)))


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

        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Kargo İşlemleri")
        self.dialog.setModal(True)
        self.dialog.setFixedSize(450, 480)
        self.dialog.setStyleSheet(MODAL_STYLE)
        dialog_layout = QVBoxLayout(self.dialog)
        dialog_layout.setContentsMargins(30, 30, 30, 30)
        dialog_layout.setSpacing(15)

        title_label = QLabel("📦 Kargo Formu")
        title_label.setStyleSheet("font-size: 20px; font-weight: 800; color: #F8FAFC; margin-bottom: 10px;")
        dialog_layout.addWidget(title_label)

        self.txt_id = QLineEdit(); self.txt_mid = QLineEdit()
        self.txt_cikis = QLineEdit(); self.txt_varis = QLineEdit()
        self.txt_kg = QLineEdit(); self.txt_durum = QLineEdit()

        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.addRow("Kargo ID:", self.txt_id); form_layout.addRow("Müşteri ID:", self.txt_mid)
        form_layout.addRow("Çıkış Şubesi:", self.txt_cikis); form_layout.addRow("Varış Adresi:", self.txt_varis)
        form_layout.addRow("Ağırlık (kg):", self.txt_kg); form_layout.addRow("Durum:", self.txt_durum)
        dialog_layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.btn_iptal = QPushButton("İptal"); self.btn_iptal.setObjectName("btn_iptal")
        self.btn_kaydet = QPushButton("Kaydet"); self.btn_kaydet.setObjectName("btn_kaydet")
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_iptal); btn_layout.addWidget(self.btn_kaydet)
        dialog_layout.addLayout(btn_layout)

        self.tablo = QTableWidget(); self.tablo.setColumnCount(9) # Ditambah 1 untuk "No."
        self.tablo.setHorizontalHeaderLabels(["No.", "Kargo ID", "Müşteri", "Çıkış Şubesi", "Varış Adresi", "Ağırlık (kg)", "Ücret (₺)", "Durum", "Tarih"])
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tablo.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.setAlternatingRowColors(True)
        self.card_layout.addWidget(self.tablo)

        self.btn_yeni.clicked.connect(lambda: self.goster_form("EKLE")); self.btn_guncelle.clicked.connect(lambda: self.goster_form("GUNCELLE"))
        self.btn_iptal.clicked.connect(self.dialog.reject); self.btn_kaydet.clicked.connect(self.kaydet)
        self.btn_sil.clicked.connect(self.sil); self.btn_yenile.clicked.connect(self.yenile)
        self.mod = "EKLE"; self.yenile()

    def goster_form(self, mod):
        self.mod = mod; self.txt_id.setEnabled(mod == "EKLE")
        if mod == "EKLE": 
            for w in [self.txt_id, self.txt_mid, self.txt_cikis, self.txt_varis, self.txt_kg]: w.clear()
            self.txt_durum.setText("Beklemede")
        else:
            s = self.tablo.currentRow()
            if s < 0: return QMessageBox.warning(self, "Uyarı", "Lütfen bir kayıt seçin!")
            self.txt_id.setText(self.tablo.item(s,1).text()); self.txt_mid.setText(self.tablo.item(s,2).text())
            self.txt_cikis.setText(self.tablo.item(s,3).text()); self.txt_varis.setText(self.tablo.item(s,4).text())
            self.txt_kg.setText(self.tablo.item(s,5).text()); self.txt_durum.setText(self.tablo.item(s,7).text())
        self.dialog.exec()

    def kaydet(self):
        d = [self.txt_id.text(), self.txt_mid.text(), self.txt_cikis.text(), self.txt_varis.text(), self.txt_kg.text(), self.txt_durum.text()]
        b, m = kargo_logic.gonderi_kaydet_bll(*d) if self.mod == "EKLE" else kargo_logic.gonderi_guncelle_bll(*d)
        if b: QMessageBox.information(self, "Başarılı", m); self.dialog.accept(); self.yenile()
        else: QMessageBox.warning(self, "Hata", m)

    def sil(self):
        s = self.tablo.currentRow()
        if s < 0: return QMessageBox.warning(self, "Uyarı", "Lütfen silinecek satırı seçin!")
        cevap = QMessageBox.question(self, "Onay", "Seçili kargoyu silmek istediğinize emin misiniz?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if cevap == QMessageBox.StandardButton.Yes:
            if kargo_logic.gonderi_sil_bll(self.tablo.item(s,1).text())[0]: self.yenile()

    def yenile(self):
        b, v = kargo_logic.gonderi_getir_bll()
        if b:
            self.tablo.setRowCount(0)
            for i, row in enumerate(v):
                self.tablo.insertRow(i)
                item_no = QTableWidgetItem(str(i + 1))
                item_no.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tablo.setItem(i, 0, item_no)
                for j, val in enumerate(row): 
                    self.tablo.setItem(i, j + 1, QTableWidgetItem(str(val)))

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

        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Şube İşlemleri")
        self.dialog.setModal(True)
        self.dialog.setFixedSize(450, 360)
        self.dialog.setStyleSheet(MODAL_STYLE)
        dialog_layout = QVBoxLayout(self.dialog)
        dialog_layout.setContentsMargins(30, 30, 30, 30)
        dialog_layout.setSpacing(15)

        title_label = QLabel("🏢 Şube Detayları")
        title_label.setStyleSheet("font-size: 20px; font-weight: 800; color: #F8FAFC; margin-bottom: 10px;")
        dialog_layout.addWidget(title_label)

        self.txt_id = QLineEdit(); self.txt_ad = QLineEdit()
        self.txt_ulke = QLineEdit(); self.txt_sehir = QLineEdit()

        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.addRow("Şube ID:", self.txt_id); form_layout.addRow("Şube Adı:", self.txt_ad)
        form_layout.addRow("Ülke:", self.txt_ulke); form_layout.addRow("Şehir:", self.txt_sehir)
        dialog_layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.btn_iptal = QPushButton("İptal"); self.btn_iptal.setObjectName("btn_iptal")
        self.btn_kaydet = QPushButton("Kaydet"); self.btn_kaydet.setObjectName("btn_kaydet")
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_iptal); btn_layout.addWidget(self.btn_kaydet)
        dialog_layout.addLayout(btn_layout)

        self.tablo = QTableWidget(); self.tablo.setColumnCount(5) # Ditambah 1 untuk "No."
        self.tablo.setHorizontalHeaderLabels(["No.", "Şube ID", "Şube Adı", "Ülke", "Şehir"])
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tablo.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.setAlternatingRowColors(True)
        self.card_layout.addWidget(self.tablo)

        self.btn_yeni.clicked.connect(lambda: self.goster_form("EKLE")); self.btn_guncelle.clicked.connect(lambda: self.goster_form("GUNCELLE"))
        self.btn_iptal.clicked.connect(self.dialog.reject); self.btn_kaydet.clicked.connect(self.kaydet)
        self.btn_sil.clicked.connect(self.sil); self.btn_yenile.clicked.connect(self.yenile)
        self.mod = "EKLE"; self.yenile()

    def goster_form(self, mod):
        self.mod = mod; self.txt_id.setEnabled(mod == "EKLE")
        if mod == "EKLE": 
            for w in [self.txt_id, self.txt_ad, self.txt_ulke, self.txt_sehir]: w.clear()
        else:
            s = self.tablo.currentRow()
            if s < 0: return QMessageBox.warning(self, "Uyarı", "Lütfen bir kayıt seçin!")
            self.txt_id.setText(self.tablo.item(s,1).text()); self.txt_ad.setText(self.tablo.item(s,2).text())
            self.txt_ulke.setText(self.tablo.item(s,3).text()); self.txt_sehir.setText(self.tablo.item(s,4).text())
        self.dialog.exec()

    def kaydet(self):
        d = [self.txt_id.text(), self.txt_ad.text(), self.txt_ulke.text(), self.txt_sehir.text()]
        b, m = kargo_logic.sube_kaydet_bll(*d) if self.mod == "EKLE" else kargo_logic.sube_guncelle_bll(*d)
        if b: QMessageBox.information(self, "Başarılı", m); self.dialog.accept(); self.yenile()
        else: QMessageBox.warning(self, "Hata", m)

    def sil(self):
        s = self.tablo.currentRow()
        if s < 0: return QMessageBox.warning(self, "Uyarı", "Lütfen silinecek satırı seçin!")
        cevap = QMessageBox.question(self, "Onay", "Seçili şubeyi silmek istediğinize emin misiniz?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if cevap == QMessageBox.StandardButton.Yes:
            if kargo_logic.sube_sil_bll(self.tablo.item(s,1).text())[0]: self.yenile()

    def yenile(self):
        b, v = kargo_logic.sube_getir_bll()
        if b:
            self.tablo.setRowCount(0)
            for i, row in enumerate(v):
                self.tablo.insertRow(i)
                item_no = QTableWidgetItem(str(i + 1))
                item_no.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tablo.setItem(i, 0, item_no)
                for j, val in enumerate(row): 
                    self.tablo.setItem(i, j + 1, QTableWidgetItem(str(val)))


# --- 4. HAREKET PAGE ---
class HareketPage(BasePage):
    def __init__(self):
        super().__init__()
        toolbar = QHBoxLayout()
        
        lbl = QLabel("📦 Kargo Seç:")
        lbl.setStyleSheet("font-weight: bold; font-size: 14px; margin-right: 5px;")
        toolbar.addWidget(lbl)
        
        self.cmb_gonderi = QComboBox()
        self.cmb_gonderi.setFixedWidth(200)
        toolbar.addWidget(self.cmb_gonderi)
        
        self.btn_yeni = QPushButton(" Yeni Ekle"); self.btn_yeni.setIcon(get_icon("add"))
        self.btn_yenile = QPushButton(" Yenile"); self.btn_yenile.setIcon(get_icon("refresh"))
        
        for w in [self.btn_yeni, self.btn_yenile]: toolbar.addWidget(w)
        toolbar.addStretch()
        self.card_layout.addLayout(toolbar)

        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Hareket Kaydı Ekle")
        self.dialog.setModal(True)
        self.dialog.setFixedSize(450, 360)
        self.dialog.setStyleSheet(MODAL_STYLE)
        dialog_layout = QVBoxLayout(self.dialog)
        dialog_layout.setContentsMargins(30, 30, 30, 30)
        dialog_layout.setSpacing(15)

        title_label = QLabel("🔄 Yeni Hareket Ekle")
        title_label.setStyleSheet("font-size: 20px; font-weight: 800; color: #F8FAFC; margin-bottom: 10px;")
        dialog_layout.addWidget(title_label)

        self.txt_id = QLineEdit(); self.txt_id.setPlaceholderText("Örn: HK-101")
        self.txt_gid = QLineEdit() 
        self.txt_sid = QLineEdit(); self.txt_sid.setPlaceholderText("Örn: TR-34A")
        self.txt_durum = QLineEdit(); self.txt_durum.setPlaceholderText("Örn: Transfer aracına yüklendi")

        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.addRow("Hareket ID:", self.txt_id); form_layout.addRow("Gönderi ID:", self.txt_gid)
        form_layout.addRow("Şube ID:", self.txt_sid); form_layout.addRow("Durum:", self.txt_durum)
        dialog_layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.btn_iptal = QPushButton("İptal"); self.btn_iptal.setObjectName("btn_iptal")
        self.btn_kaydet = QPushButton("Kaydet"); self.btn_kaydet.setObjectName("btn_kaydet")
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_iptal); btn_layout.addWidget(self.btn_kaydet)
        dialog_layout.addLayout(btn_layout)

        self.tablo = QTableWidget(); self.tablo.setColumnCount(4) # Ditambah 1 untuk "No."
        self.tablo.setHorizontalHeaderLabels(["No.", "İşlem Tarihi", "Şube Adı", "Durum"])
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tablo.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # Khusus kolom No. dibuat kecil
        self.tablo.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.setAlternatingRowColors(True)
        self.card_layout.addWidget(self.tablo)

        self.cmb_gonderi.currentTextChanged.connect(self.ara)
        self.btn_yenile.clicked.connect(self.populate_dropdown)
        self.btn_yeni.clicked.connect(self.goster_form)
        self.btn_iptal.clicked.connect(self.dialog.reject)
        self.btn_kaydet.clicked.connect(self.kaydet)

        self.populate_dropdown()

    def populate_dropdown(self):
        self.cmb_gonderi.blockSignals(True)
        self.cmb_gonderi.clear()
        b, v = kargo_logic.gonderi_getir_bll()
        if b:
            for row in v: self.cmb_gonderi.addItem(str(row[0]))
        self.cmb_gonderi.blockSignals(False)
        self.ara()

    def goster_form(self):
        for w in [self.txt_id, self.txt_sid, self.txt_durum]: w.clear()
        g_id = self.cmb_gonderi.currentText()
        if not g_id: return QMessageBox.warning(self, "Uyarı", "Lütfen önce bir Kargo seçin!")
        self.txt_gid.setText(g_id)
        self.txt_gid.setEnabled(False)
        self.dialog.exec()

    def ara(self):
        g_id = self.cmb_gonderi.currentText()
        if not g_id: 
            self.tablo.setRowCount(0)
            return
        b, v = kargo_logic.hareket_getir_bll(g_id)
        if b:
            self.tablo.setRowCount(0)
            for i, row in enumerate(v):
                self.tablo.insertRow(i)
                item_no = QTableWidgetItem(str(i + 1))
                item_no.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tablo.setItem(i, 0, item_no)
                for j, val in enumerate(row): 
                    self.tablo.setItem(i, j + 1, QTableWidgetItem(str(val)))
        else: 
            self.tablo.setRowCount(0)

    def kaydet(self):
        b, m = kargo_logic.hareket_kaydet_bll(self.txt_id.text(), self.txt_gid.text(), self.txt_sid.text(), self.txt_durum.text())
        if b: QMessageBox.information(self, "Başarılı", m); self.dialog.accept(); self.ara()
        else: QMessageBox.warning(self, "Hata", m)