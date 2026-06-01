from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                             QPushButton, QStackedWidget, QLabel, QFrame, QSizePolicy)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve
from UI.theme import get_stylesheet
from UI.pages import MusteriPage, GonderiPage, SubePage, HareketPage
from UI.icons import get_icon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Global Route Lojistik - Enterprise Logistics Portal v2.4")
        self.setStyleSheet(get_stylesheet())
        
        # Membuang Title Bar bawaan Windows
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        
        # Menampilkan aplikasi secara penuh
        self.showMaximized()
        self.setMinimumSize(1000, 700) # Mencegah tabel gepeng di layar kecil
        
        self.is_sidebar_expanded = True

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ================= SIDEBAR =================
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(240)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        
        self.logo = QLabel()
        self.logo.setObjectName("logo")
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo.setPixmap(get_icon("logo").pixmap(QSize(55, 55)))
        
        self.logo_sub = QLabel("GLOBAL ROUTE LOJİSTİK")
        self.logo_sub.setObjectName("logo_sub")
        self.logo_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        sp = self.logo_sub.sizePolicy()
        sp.setRetainSizeWhenHidden(True)
        self.logo_sub.setSizePolicy(sp)
        
        sidebar_layout.addWidget(self.logo)
        sidebar_layout.addWidget(self.logo_sub)

        # Tombol Navigasi (Sudah dikoreksi ke bahasa Turki baku)
        self.btn_anamenu = QPushButton(" Ana Menü")
        self.btn_musteri = QPushButton(" Müşteriler")
        self.btn_gonderi = QPushButton(" Kargo Gönderimi")
        self.btn_sube = QPushButton(" Şubeler")
        self.btn_hareket = QPushButton(" Hareketler")

        self.btn_anamenu.original_text = " Ana Menü"
        self.btn_musteri.original_text = " Müşteriler"
        self.btn_gonderi.original_text = " Kargo Gönderimi"
        self.btn_sube.original_text = " Şubeler"
        self.btn_hareket.original_text = " Hareketler"

        self.nav_buttons = [self.btn_anamenu, self.btn_musteri, self.btn_gonderi, self.btn_sube, self.btn_hareket]
        
        self.btn_anamenu.setIcon(get_icon("dashboard"))
        self.btn_musteri.setIcon(get_icon("person"))
        self.btn_gonderi.setIcon(get_icon("shipping"))
        self.btn_sube.setIcon(get_icon("store"))
        self.btn_hareket.setIcon(get_icon("history"))

        for btn in self.nav_buttons:
            btn.setCheckable(True)
            btn.setAutoExclusive(True) 
            btn.setObjectName("nav_button")
            btn.setIconSize(QSize(22, 22))
            btn.setProperty("collapsed", False)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # ================= AREA KONTEN =================
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(30, 20, 30, 30)

        self.header_frame = QFrame()
        self.header_layout = QVBoxLayout(self.header_frame)
        self.header_layout.setContentsMargins(0, 0, 0, 10)
        self.header_layout.setSpacing(0)
        
        # PERBAIKAN: Menghapus emoji bawaan sistem pada judul default
        self.lbl_title = QLabel("Kargo Gönderimi Yönetimi")
        self.lbl_title.setObjectName("header_title")
        self.lbl_subtitle = QLabel("Tüm aktif kargo sevkiyatlarını yönetin")
        self.lbl_subtitle.setObjectName("header_subtitle")
        
        self.header_layout.addWidget(self.lbl_title)
        self.header_layout.addWidget(self.lbl_subtitle)
        content_layout.addWidget(self.header_frame)

        from UI.pages import AnaMenuPage 
        
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(AnaMenuPage()) # Index 0
        self.stacked_widget.addWidget(MusteriPage()) # Index 1
        self.stacked_widget.addWidget(GonderiPage()) # Index 2
        self.stacked_widget.addWidget(SubePage())    # Index 3
        self.stacked_widget.addWidget(HareketPage()) # Index 4
        content_layout.addWidget(self.stacked_widget)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(content_area)

        # PERBAIKAN: Menghapus seluruh emoji dari teks navigasi
        self.btn_anamenu.clicked.connect(lambda: self.handle_nav_click(0, "Ana Menü", "Sistem istatistikleri ve genel bakış", self.btn_anamenu))
        self.btn_musteri.clicked.connect(lambda: self.handle_nav_click(1, "Müşteriler Yönetimi", "Sistemdeki tüm müşteri kayıtlarını yönetin", self.btn_musteri))
        self.btn_gonderi.clicked.connect(lambda: self.handle_nav_click(2, "Kargo Gönderimi Yönetimi", "Tüm aktif kargo sevkiyatlarını yönetin", self.btn_gonderi))
        self.btn_sube.clicked.connect(lambda: self.handle_nav_click(3, "Şubeler Yönetimi", "Şube ağını ve lokasyon bilgilerini yönetin", self.btn_sube))
        self.btn_hareket.clicked.connect(lambda: self.handle_nav_click(4, "Hareketler Yönetimi", "Seçili kargonun taşıma geçmişini listeleyin", self.btn_hareket))

        # Setup Awal
        self.btn_anamenu.setChecked(True)
        self.handle_nav_click(0, "Ana Menü", "Sistem istatistikleri ve genel bakış", self.btn_anamenu, force_init=True)

  
    def handle_nav_click(self, index, title, subtitle, clicked_btn, force_init=False):
        if not force_init and self.stacked_widget.currentIndex() == index:
            self.toggle_sidebar()
        else:
            self.stacked_widget.setCurrentIndex(index)
            self.lbl_title.setText(title)
            self.lbl_subtitle.setText(subtitle)

    def toggle_sidebar(self):
        self.is_sidebar_expanded = not self.is_sidebar_expanded
        
        target_width = 240 if self.is_sidebar_expanded else 76
        
        self.anim1 = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.anim1.setDuration(250)
        self.anim1.setStartValue(self.sidebar.width())
        self.anim1.setEndValue(target_width)
        self.anim1.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        self.anim2 = QPropertyAnimation(self.sidebar, b"maximumWidth")
        self.anim2.setDuration(250)
        self.anim2.setStartValue(self.sidebar.width())
        self.anim2.setEndValue(target_width)
        self.anim2.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        if self.is_sidebar_expanded:
            self.logo_sub.show()
            for btn in self.nav_buttons:
                btn.setText(btn.original_text) 
                btn.setProperty("collapsed", False)
                btn.style().unpolish(btn)
                btn.style().polish(btn)
        else:
            self.logo_sub.hide()
            for btn in self.nav_buttons:
                btn.setText("")
                btn.setProperty("collapsed", True)
                btn.style().unpolish(btn)
                btn.style().polish(btn)
                
        self.anim1.start()
        self.anim2.start()