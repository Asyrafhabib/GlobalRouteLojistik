from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QMessageBox, QHeaderView, QFrame, QDialog, QFormLayout, QLabel, QGridLayout)
from PyQt6.QtCore import Qt, QVariantAnimation, QEasingCurve, QRectF, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath, QBrush, QFont, QLinearGradient
from UI.icons import get_icon
from BLL import kargo_logic

MODAL_STYLE = """
QDialog { background-color: #1E1E1E; border: 1px solid #2B2B2B; border-radius: 8px; }
QLabel { font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; font-weight: 600; color: #E0E0E0; }
QLineEdit { background-color: #252526; border: 1px solid #3E3E42; border-radius: 6px; padding: 10px 14px; color: #FFFFFF; font-size: 13px; }
QLineEdit:focus { border: 1px solid #007ACC; background-color: #1E1E1E; }
QPushButton { font-family: 'Segoe UI', Arial, sans-serif; font-weight: bold; font-size: 13px; border-radius: 6px; padding: 10px 20px; }
QPushButton#btn_iptal { background-color: #333333; color: #E0E0E0; border: 1px solid #3E3E42; }
QPushButton#btn_iptal:hover { background-color: #3E3E42; }
QPushButton#btn_kaydet { background-color: #007ACC; color: #FFFFFF; border: none; }
QPushButton#btn_kaydet:hover { background-color: #005A9E; }
"""

# ==============================================================================
# WIDGET DIAGRAM KUSTOM (LINE CHART & DONUT CHART) - DARK ENTERPRISE THEME
# ==============================================================================

class LineChartWidget(QWidget):
    """Diagram Garis (Line Chart) dengan Sumbu Y yang Diperjelas"""
    def __init__(self, data, labels):
        super().__init__()
        self.data = data
        self.labels = labels
        self.progress = 0.0
        self.setMinimumHeight(240)
        
        self.anim = QVariantAnimation(self)
        self.anim.setDuration(1500)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anim.valueChanged.connect(self.update_progress)

    def update_progress(self, val):
        self.progress = val
        self.update()

    def start_animation(self):
        self.anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w, h = self.width(), self.height()
        margin_left = 50 # Diperlebar untuk angka Sumbu Y
        margin_right = 30
        margin_y = 30
        
        draw_w = w - margin_left - margin_right
        draw_h = h - (margin_y * 2)
        
        max_val = max(self.data) if self.data else 10
        max_val = int(max_val + (max_val * 0.2)) # Tambah ruang 20% di atas
        if max_val == 0: max_val = 10
        
        # Gambar Garis Latar (Grid) dan Angka Sumbu Y
        painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        for i in range(4):
            y = margin_y + (draw_h / 3) * i
            val_y = int(max_val - (max_val / 3) * i)
            
            # Teks Sumbu Y
            painter.setPen(QColor(133, 133, 133))
            painter.drawText(10, int(y + 5), f"{val_y}")
            
            # Garis Putus-putus
            painter.setPen(QPen(QColor(62, 62, 66), 1, Qt.PenStyle.DashLine))
            painter.drawLine(margin_left, int(y), w - margin_right, int(y))
            
        # Hitung Titik Koordinat
        points = []
        step_x = draw_w / (len(self.data) - 1) if len(self.data) > 1 else draw_w
        for i, val in enumerate(self.data):
            x = margin_left + (i * step_x)
            y = margin_y + draw_h - ((val / max_val) * draw_h)
            points.append(QPointF(x, y))
            
        # Efek Animasi
        clip_rect = QRectF(0, 0, w * self.progress, h)
        painter.setClipRect(clip_rect)

        # Gambar Area Bawah Gradient
        if len(points) > 1:
            path = QPainterPath()
            path.moveTo(points[0].x(), margin_y + draw_h)
            for p in points: path.lineTo(p)
            path.lineTo(points[-1].x(), margin_y + draw_h)
            path.closeSubpath()
            
            grad = QLinearGradient(0, margin_y, 0, margin_y + draw_h)
            grad.setColorAt(0.0, QColor(0, 122, 204, 120)) # Biru korporat transparan
            grad.setColorAt(1.0, QColor(0, 122, 204, 0))
            painter.fillPath(path, QBrush(grad))
            
            # Gambar Garis Utama
            line_path = QPainterPath()
            line_path.moveTo(points[0])
            for p in points[1:]: line_path.lineTo(p)
            
            painter.setPen(QPen(QColor(0, 122, 204), 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            painter.drawPath(line_path)

        # Gambar Titik dan Sumbu X
        painter.setClipRect(QRectF(0, 0, w, h)) 
        for i, p in enumerate(points):
            if p.x() <= w * self.progress: 
                # Lingkaran Titik (Lebih Besar & Jelas)
                painter.setPen(QPen(QColor(0, 122, 204), 2))
                painter.setBrush(QBrush(QColor(30, 30, 30)))
                painter.drawEllipse(p, 6, 6)
                
                # Angka di atas titik
                painter.setPen(QColor(255, 255, 255))
                painter.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
                painter.drawText(int(p.x() - 8), int(p.y() - 15), str(self.data[i]))
            
            # Label Hari (Sumbu X)
            painter.setPen(QColor(166, 166, 166))
            painter.setFont(QFont("Segoe UI", 10))
            painter.drawText(int(p.x() - 10), int(margin_y + draw_h + 22), self.labels[i])


class DonutChartWidget(QWidget):
    """Diagram Donat Kategori Umum Sesuai Tema (Blue/Grey)"""
    def __init__(self, data_dict):
        super().__init__()
        self.data = data_dict
        self.progress = 0.0
        self.setMinimumHeight(240)
        
        # Palet Warna Sesuai UI (Biru Terang, Biru Gelap, Abu-abu UI)
        self.color_map = {
            "Teslim Edildi": QColor(0, 122, 204),   # Accent Blue
            "Yolda": QColor(0, 90, 158),            # Dark Blue
            "Beklemede": QColor(62, 62, 66),        # Dark Grey
            "Veri Yok": QColor(43, 43, 43)
        }
        
        self.anim = QVariantAnimation(self)
        self.anim.setDuration(1500)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.valueChanged.connect(self.update_progress)

    def update_progress(self, val):
        self.progress = val
        self.update()

    def start_animation(self):
        self.anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w, h = self.width(), self.height()
        size = min(w, h) - 40
        rect = QRectF(20, (h - size) / 2, size, size)
        
        total = sum(self.data.values()) if self.data else 1
        start_angle = 90 * 16 
        
        for label, val in self.data.items():
            span_angle = int((-val / total) * 360 * 16 * self.progress)
            color = self.color_map.get(label, QColor(0, 122, 204))
            
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPie(rect, start_angle, span_angle)
            start_angle += span_angle
            
        # Lubang Tengah
        hole_size = size * 0.65
        hole_rect = QRectF(20 + (size - hole_size)/2, (h - hole_size)/2, hole_size, hole_size)
        painter.setBrush(QBrush(QColor(24, 24, 24))) 
        painter.drawEllipse(hole_rect)
        
        # Teks Total
        if self.progress > 0.5:
            painter.setPen(QColor(255, 255, 255))
            painter.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
            painter.drawText(hole_rect, Qt.AlignmentFlag.AlignCenter, f"{int(total * self.progress)}\nKargo")

        # Legenda yang Diperjelas
        legend_x = 20 + size + 40
        legend_y = (h - (len(self.data) * 35)) / 2
        painter.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        
        for i, (label, val) in enumerate(self.data.items()):
            color = self.color_map.get(label, QColor(0, 122, 204))
            y_pos = int(legend_y + (i * 35))
            
            painter.setBrush(QBrush(color))
            painter.drawRect(int(legend_x), y_pos, 14, 14)
            
            painter.setPen(QColor(224, 224, 224))
            pct = int((val/total)*100) if total > 0 else 0
            painter.drawText(int(legend_x + 25), y_pos + 12, f"{label} (%{pct})")

# ==============================================================================
# HALAMAN-HALAMAN (PAGES)
# ==============================================================================

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

# --- 0. ANA MENÜ (DASHBOARD) PAGE ---
class AnaMenuPage(BasePage):
    def __init__(self):
        super().__init__()
        lbl_title = QLabel("Sistem Gösterge Paneli")
        lbl_title.setStyleSheet("font-size: 24px; font-weight: 800; color: #FFFFFF; margin-bottom: 10px; background-color: transparent;")
        self.card_layout.addWidget(lbl_title)
        
        grid = QGridLayout()
        grid.setSpacing(15)

        self.card_musteri, self.lbl_val_musteri = self.create_stat_card("Toplam Müşteri", "0")
        self.card_kargo, self.lbl_val_kargo = self.create_stat_card("Aktif Gönderiler", "0")
        self.card_sube, self.lbl_val_sube = self.create_stat_card("Kayıtlı Şubeler", "0")
        self.card_status, self.lbl_val_status = self.create_stat_card("Sistem Durumu", "Çevrimiçi")

        grid.addWidget(self.card_musteri, 0, 0); grid.addWidget(self.card_kargo, 0, 1)
        grid.addWidget(self.card_sube, 0, 2); grid.addWidget(self.card_status, 0, 3)
        self.card_layout.addLayout(grid)
        
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(20)
        charts_layout.setContentsMargins(0, 20, 0, 0)

        # 1. Bingkai Diagram Garis
        frame_line = QFrame()
        frame_line.setStyleSheet("QFrame { background-color: #181818; border: 1px solid #2B2B2B; border-radius: 10px; }")
        lay_line = QVBoxLayout(frame_line)
        lbl_line = QLabel("Son 5 Günlük Kargo Hacmi"); lbl_line.setStyleSheet("color: #E0E0E0; font-size: 15px; font-weight: bold; padding: 10px 5px 0px 10px;")
        self.chart_line = LineChartWidget(data=[12, 28, 15, 35, 22], labels=["Pzt", "Sal", "Çar", "Per", "Cum"])
        lay_line.addWidget(lbl_line); lay_line.addWidget(self.chart_line)
        charts_layout.addWidget(frame_line, stretch=3) 

        # 2. Bingkai Diagram Donat
        status_data = self.get_kargo_status_distribution()
        frame_donut = QFrame()
        frame_donut.setStyleSheet("QFrame { background-color: #181818; border: 1px solid #2B2B2B; border-radius: 10px; }")
        lay_donut = QVBoxLayout(frame_donut)
        lbl_donut = QLabel("Kargo Durum Dağılımı"); lbl_donut.setStyleSheet("color: #E0E0E0; font-size: 15px; font-weight: bold; padding: 10px 5px 0px 10px;")
        self.chart_donut = DonutChartWidget(data_dict=status_data)
        lay_donut.addWidget(lbl_donut); lay_donut.addWidget(self.chart_donut)
        charts_layout.addWidget(frame_donut, stretch=2) 

        self.card_layout.addLayout(charts_layout)
        self.card_layout.addStretch()
        self.load_analytics_data()

    def get_kargo_status_distribution(self):
        """Mengkategorikan status secara pintar menjadi 3 grup besar"""
        b, v = kargo_logic.gonderi_getir_bll()
        dist = {"Teslim Edildi": 0, "Yolda": 0, "Beklemede": 0}
        
        if b:
            for row in v:
                status = str(row[6]).strip().lower()
                # Kategorisasi Logika
                if "teslim edildi" in status:
                    dist["Teslim Edildi"] += 1
                elif "beklemede" in status or "bekliyor" in status:
                    dist["Beklemede"] += 1
                else:
                    dist["Yolda"] += 1
                    
        # Hapus kategori yang nilainya 0 agar diagram bersih
        clean_dist = {k: v for k, v in dist.items() if v > 0}
        return clean_dist if clean_dist else {"Veri Yok": 1}

    def create_stat_card(self, title, value):
        # Aksen warna diseragamkan dengan warna biru UI (Bukan warna-warni lagi)
        card = QFrame()
        card.setStyleSheet("QFrame { background-color: #181818; border: 1px solid #2B2B2B; border-radius: 10px; border-bottom: 4px solid #007ACC; }")
        lay = QVBoxLayout(card)
        lay.setContentsMargins(20, 20, 20, 20)
        lbl_t = QLabel(title); lbl_t.setStyleSheet("color: #858585; font-size: 14px; font-weight: 700; border: none;")
        lbl_v = QLabel(value); lbl_v.setStyleSheet("color: #FFFFFF; font-size: 32px; font-weight: 900; border: none; margin-top: 10px;")
        lay.addWidget(lbl_t); lay.addWidget(lbl_v)
        return card, lbl_v

    def load_analytics_data(self):
        b1, v1 = kargo_logic.musteri_getir_bll()
        if b1: self.lbl_val_musteri.setText(str(len(v1)))
        b2, v2 = kargo_logic.gonderi_getir_bll()
        if b2: self.lbl_val_kargo.setText(str(len(v2)))
        b3, v3 = kargo_logic.sube_getir_bll()
        if b3: self.lbl_val_sube.setText(str(len(v3)))

    def showEvent(self, event):
        super().showEvent(event)
        self.chart_line.start_animation()
        self.chart_donut.start_animation()

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
        self.dialog.setWindowTitle("Müşteri İşlemleri"); self.dialog.setModal(True)
        self.dialog.setFixedSize(450, 460); self.dialog.setStyleSheet(MODAL_STYLE)
        dialog_layout = QVBoxLayout(self.dialog); dialog_layout.setContentsMargins(30, 30, 30, 30); dialog_layout.setSpacing(15)

        title_label = QLabel("Müşteri Detayları"); title_label.setStyleSheet("font-size: 20px; font-weight: 800; color: #FFFFFF; margin-bottom: 10px;")
        dialog_layout.addWidget(title_label)

        self.txt_id = QLineEdit(); self.txt_ad = QLineEdit(); self.txt_soyad = QLineEdit()
        self.txt_tel = QLineEdit(); self.txt_mail = QLineEdit(); self.txt_ulke = QLineEdit()

        form_layout = QFormLayout(); form_layout.setSpacing(12)
        form_layout.addRow("Müşteri ID:", self.txt_id); form_layout.addRow("Ad:", self.txt_ad)
        form_layout.addRow("Soyad:", self.txt_soyad); form_layout.addRow("Telefon:", self.txt_tel)
        form_layout.addRow("Mail:", self.txt_mail); form_layout.addRow("Ülke:", self.txt_ulke)
        dialog_layout.addLayout(form_layout)

        btn_layout = QHBoxLayout(); self.btn_iptal = QPushButton("İptal"); self.btn_iptal.setObjectName("btn_iptal")
        self.btn_kaydet = QPushButton("Kaydet"); self.btn_kaydet.setObjectName("btn_kaydet")
        btn_layout.addStretch(); btn_layout.addWidget(self.btn_iptal); btn_layout.addWidget(self.btn_kaydet)
        dialog_layout.addLayout(btn_layout)

        self.tablo = QTableWidget(); self.tablo.setColumnCount(7) 
        self.tablo.setHorizontalHeaderLabels(["No.", "ID", "Müşteri Adı", "Soyad", "Telefon", "Mail", "Ülke"])
        
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tablo.horizontalHeader().setStretchLastSection(True)
        
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
        if mod == "EKLE": [w.clear() for w in [self.txt_id, self.txt_ad, self.txt_soyad, self.txt_tel, self.txt_mail, self.txt_ulke]]
        else:
            s = self.tablo.currentRow()
            if s < 0: return QMessageBox.warning(self, "Uyarı", "Lütfen bir kayıt seçin!")
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
                item_no = QTableWidgetItem(str(i + 1)); item_no.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tablo.setItem(i, 0, item_no)
                for j, val in enumerate(row): self.tablo.setItem(i, j + 1, QTableWidgetItem(str(val)))

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
        self.dialog.setWindowTitle("Kargo İşlemleri"); self.dialog.setModal(True)
        self.dialog.setFixedSize(450, 480); self.dialog.setStyleSheet(MODAL_STYLE)
        dialog_layout = QVBoxLayout(self.dialog); dialog_layout.setContentsMargins(30, 30, 30, 30); dialog_layout.setSpacing(15)

        title_label = QLabel("Kargo Formu"); title_label.setStyleSheet("font-size: 20px; font-weight: 800; color: #FFFFFF; margin-bottom: 10px;")
        dialog_layout.addWidget(title_label)

        self.txt_id = QLineEdit(); self.txt_mid = QLineEdit()
        self.txt_cikis = QLineEdit(); self.txt_varis = QLineEdit()
        self.txt_kg = QLineEdit(); self.txt_durum = QLineEdit()

        form_layout = QFormLayout(); form_layout.setSpacing(12)
        form_layout.addRow("Kargo ID:", self.txt_id); form_layout.addRow("Müşteri ID:", self.txt_mid)
        form_layout.addRow("Çıkış Şubesi:", self.txt_cikis); form_layout.addRow("Varış Adresi:", self.txt_varis)
        form_layout.addRow("Ağırlık (kg):", self.txt_kg); form_layout.addRow("Durum:", self.txt_durum)
        dialog_layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.btn_iptal = QPushButton("İptal"); self.btn_iptal.setObjectName("btn_iptal")
        self.btn_kaydet = QPushButton("Kaydet"); self.btn_kaydet.setObjectName("btn_kaydet")
        btn_layout.addStretch(); btn_layout.addWidget(self.btn_iptal); btn_layout.addWidget(self.btn_kaydet)
        dialog_layout.addLayout(btn_layout)

        self.tablo = QTableWidget(); self.tablo.setColumnCount(9) 
        self.tablo.setHorizontalHeaderLabels(["No.", "Kargo ID", "Müşteri", "Çıkış Şubesi", "Varış Adresi", "Ağırlık (kg)", "Ücret (₺)", "Durum", "Tarih"])
        
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tablo.horizontalHeader().setStretchLastSection(True)
        
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
                item_no = QTableWidgetItem(str(i + 1)); item_no.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tablo.setItem(i, 0, item_no)
                for j, val in enumerate(row): self.tablo.setItem(i, j + 1, QTableWidgetItem(str(val)))

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
        self.dialog.setWindowTitle("Şube İşlemleri"); self.dialog.setModal(True)
        self.dialog.setFixedSize(450, 360); self.dialog.setStyleSheet(MODAL_STYLE)
        dialog_layout = QVBoxLayout(self.dialog); dialog_layout.setContentsMargins(30, 30, 30, 30); dialog_layout.setSpacing(15)

        title_label = QLabel("Şube Detayları"); title_label.setStyleSheet("font-size: 20px; font-weight: 800; color: #FFFFFF; margin-bottom: 10px;")
        dialog_layout.addWidget(title_label)

        self.txt_id = QLineEdit(); self.txt_ad = QLineEdit()
        self.txt_ulke = QLineEdit(); self.txt_sehir = QLineEdit()

        form_layout = QFormLayout(); form_layout.setSpacing(12)
        form_layout.addRow("Şube ID:", self.txt_id); form_layout.addRow("Şube Adı:", self.txt_ad)
        form_layout.addRow("Ülke:", self.txt_ulke); form_layout.addRow("Şehir:", self.txt_sehir)
        dialog_layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.btn_iptal = QPushButton("İptal"); self.btn_iptal.setObjectName("btn_iptal")
        self.btn_kaydet = QPushButton("Kaydet"); self.btn_kaydet.setObjectName("btn_kaydet")
        btn_layout.addStretch(); btn_layout.addWidget(self.btn_iptal); btn_layout.addWidget(self.btn_kaydet)
        dialog_layout.addLayout(btn_layout)

        self.tablo = QTableWidget(); self.tablo.setColumnCount(5) 
        self.tablo.setHorizontalHeaderLabels(["No.", "Şube ID", "Şube Adı", "Ülke", "Şehir"])
        
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tablo.horizontalHeader().setStretchLastSection(True)
        
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
                item_no = QTableWidgetItem(str(i + 1)); item_no.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tablo.setItem(i, 0, item_no)
                for j, val in enumerate(row): self.tablo.setItem(i, j + 1, QTableWidgetItem(str(val)))


# --- 4. HAREKET PAGE ---
class HareketPage(BasePage):
    def __init__(self):
        super().__init__()
        toolbar = QHBoxLayout()
        
        self.txt_gid_sorgu = QLineEdit()
        self.txt_gid_sorgu.setPlaceholderText("Gönderi ID Girin (Örn: TRK-001)")
        self.txt_gid_sorgu.setFixedWidth(250)
        toolbar.addWidget(self.txt_gid_sorgu)
        
        self.btn_sorgula = QPushButton(" Sorgula")
        self.btn_sorgula.setObjectName("btn_sorgula")
        self.btn_sorgula.setIcon(get_icon("search"))
        toolbar.addWidget(self.btn_sorgula)
        
        self.btn_yeni = QPushButton(" Yeni Ekle"); self.btn_yeni.setIcon(get_icon("add"))
        
        # TOMBOL SIL DITAMBAHKAN KEMBALI
        self.btn_sil = QPushButton(" Sil"); self.btn_sil.setIcon(get_icon("delete")); self.btn_sil.setObjectName("btn_sil")
        
        toolbar.addWidget(self.btn_yeni)
        toolbar.addWidget(self.btn_sil)
        toolbar.addStretch()
        self.card_layout.addLayout(toolbar)

        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Hareket Kaydı Ekle"); self.dialog.setModal(True)
        self.dialog.setFixedSize(450, 360); self.dialog.setStyleSheet(MODAL_STYLE)
        dialog_layout = QVBoxLayout(self.dialog); dialog_layout.setContentsMargins(30, 30, 30, 30); dialog_layout.setSpacing(15)

        title_label = QLabel("Yeni Hareket Ekle")
        title_label.setStyleSheet("font-size: 20px; font-weight: 800; color: #FFFFFF; margin-bottom: 10px;")
        dialog_layout.addWidget(title_label)

        self.txt_id = QLineEdit(); self.txt_id.setPlaceholderText("Örn: HK-101")
        self.txt_gid = QLineEdit() 
        self.txt_sid = QLineEdit(); self.txt_sid.setPlaceholderText("Örn: TR-34A")
        self.txt_durum = QLineEdit(); self.txt_durum.setPlaceholderText("Örn: Transfer aracına yüklendi")

        form_layout = QFormLayout(); form_layout.setSpacing(12)
        form_layout.addRow("Hareket ID:", self.txt_id); form_layout.addRow("Gönderi ID:", self.txt_gid)
        form_layout.addRow("Şube ID:", self.txt_sid); form_layout.addRow("Durum:", self.txt_durum)
        dialog_layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.btn_iptal = QPushButton("İptal"); self.btn_iptal.setObjectName("btn_iptal")
        self.btn_kaydet = QPushButton("Kaydet"); self.btn_kaydet.setObjectName("btn_kaydet")
        btn_layout.addStretch(); btn_layout.addWidget(self.btn_iptal); btn_layout.addWidget(self.btn_kaydet)
        dialog_layout.addLayout(btn_layout)

        # TABEL DIUBAH MENJADI 5 KOLOM
        self.tablo = QTableWidget(); self.tablo.setColumnCount(5)
        self.tablo.setHorizontalHeaderLabels(["No.", "Hareket ID", "İşlem Tarihi", "Şube Adı", "Durum"])
        
        # MENYEMBUNYIKAN KOLOM "Hareket ID" AGAR DESAIN TETAP RAPI
        self.tablo.setColumnHidden(1, True)
        
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tablo.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        
        self.tablo.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.setAlternatingRowColors(True)
        self.card_layout.addWidget(self.tablo)

        self.btn_sorgula.clicked.connect(self.ara)
        self.txt_gid_sorgu.returnPressed.connect(self.ara) 
        self.btn_yeni.clicked.connect(self.goster_form)
        self.btn_sil.clicked.connect(self.sil) # EVENT SIL
        self.btn_iptal.clicked.connect(self.dialog.reject)
        self.btn_kaydet.clicked.connect(self.kaydet)

    def goster_form(self):
        for w in [self.txt_id, self.txt_sid, self.txt_durum]: w.clear()
        g_id = self.txt_gid_sorgu.text().strip()
        if not g_id: return QMessageBox.warning(self, "Uyarı", "Lütfen önce arama kutusuna bir Gönderi ID yazın!")
        self.txt_gid.setText(g_id)
        self.txt_gid.setEnabled(False) 
        self.dialog.exec()

    def ara(self):
        g_id = self.txt_gid_sorgu.text().strip()
        if not g_id: 
            self.tablo.setRowCount(0)
            return QMessageBox.warning(self, "Uyarı", "Lütfen bir Gönderi ID girin!")
            
        b, v = kargo_logic.hareket_getir_bll(g_id)
        if b:
            self.tablo.setRowCount(0)
            if len(v) == 0:
                QMessageBox.information(self, "Bilgi", "Bu Gönderi ID'sine ait bir hareket bulunamadı.")
                return
                
            for i, row in enumerate(v):
                self.tablo.insertRow(i)
                item_no = QTableWidgetItem(str(i + 1)); item_no.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tablo.setItem(i, 0, item_no)
                
                # Memasukkan data dari DB ke kolom 1 (Hareket ID), 2 (Tarih), 3 (Sube), 4 (Durum)
                for j, val in enumerate(row): 
                    self.tablo.setItem(i, j + 1, QTableWidgetItem(str(val)))
        else: 
            self.tablo.setRowCount(0)

    def kaydet(self):
        b, m = kargo_logic.hareket_kaydet_bll(self.txt_id.text(), self.txt_gid.text(), self.txt_sid.text(), self.txt_durum.text())
        if b: QMessageBox.information(self, "Başarılı", m); self.dialog.accept(); self.ara()
        else: QMessageBox.warning(self, "Hata", m)

    def sil(self):
        # 1. Cek apakah ada baris yang dipilih (Diklik)
        s = self.tablo.currentRow()
        if s < 0: 
            return QMessageBox.warning(self, "Uyarı", "Lütfen silmek istediğiniz kargo hareketini tablodan seçin!")
        
        # 2. Ambil ID dari kolom index ke-1 yang disembunyikan
        hareket_id = self.tablo.item(s, 1).text()
        
        # 3. Detektor Error (Jika Python belum di-restart dan tidak sengaja menangkap Tanggal)
        if "-" in hareket_id and ":" in hareket_id and len(hareket_id) > 10:
            return QMessageBox.critical(self, "Hata", "Sistem Hareket ID'yi bulamadı (Tarih verisi yakalandı)!\nLütfen Python uygulamasını tamamen kapatıp yeniden çalıştırın.")
        
        # 4. Konfirmasi Penghapusan dengan menyebutkan ID-nya
        cevap = QMessageBox.question(self, "Onay", f"Seçili kargo hareketini ({hareket_id}) silmek istediğinize emin misiniz?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if cevap == QMessageBox.StandardButton.Yes:
            # Memanggil fungsi Hapus di BLL
            basarili, mesaj = kargo_logic.hareket_sil_bll(hareket_id)
            if basarili:
                QMessageBox.information(self, "Başarılı", "Kargo hareketi başarıyla silindi!")
                self.ara() # Segarkan tabel setelah dihapus
            else:
                QMessageBox.warning(self, "Hata", f"Silinirken bir hata oluştu:\n{mesaj}")

    def goster_form(self):
        for w in [self.txt_id, self.txt_sid, self.txt_durum]: w.clear()
        g_id = self.txt_gid_sorgu.text().strip()
        if not g_id: return QMessageBox.warning(self, "Uyarı", "Lütfen önce arama kutusuna bir Gönderi ID yazın!")
        self.txt_gid.setText(g_id)
        self.txt_gid.setEnabled(False) 
        self.dialog.exec()

    def ara(self):
        g_id = self.txt_gid_sorgu.text().strip()
        if not g_id: 
            self.tablo.setRowCount(0)
            return QMessageBox.warning(self, "Uyarı", "Lütfen bir Gönderi ID girin!")
            
        b, v = kargo_logic.hareket_getir_bll(g_id)
        if b:
            self.tablo.setRowCount(0)
            if len(v) == 0:
                QMessageBox.information(self, "Bilgi", "Bu Gönderi ID'sine ait bir hareket bulunamadı.")
                return
                
            for i, row in enumerate(v):
                self.tablo.insertRow(i)
                item_no = QTableWidgetItem(str(i + 1)); item_no.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tablo.setItem(i, 0, item_no)
                for j, val in enumerate(row): 
                    self.tablo.setItem(i, j + 1, QTableWidgetItem(str(val)))
        else: 
            self.tablo.setRowCount(0)

    def kaydet(self):
        b, m = kargo_logic.hareket_kaydet_bll(self.txt_id.text(), self.txt_gid.text(), self.txt_sid.text(), self.txt_durum.text())
        if b: QMessageBox.information(self, "Başarılı", m); self.dialog.accept(); self.ara()
        else: QMessageBox.warning(self, "Hata", m)