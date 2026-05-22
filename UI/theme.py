def get_stylesheet():
    return """
    /* Global Styling */
    QMainWindow { background-color: #F8FAFC; font-family: 'Segoe UI', Arial, sans-serif; }
    QWidget { font-family: 'Segoe UI', Arial, sans-serif; }

    /* ================= SIDEBAR ================= */
    QFrame#sidebar {
        background-color: #0F172A;
        border-top-right-radius: 20px;
        border-bottom-right-radius: 20px;
    }
    QFrame#sidebar QLabel { background-color: transparent; }
    
    QLabel#logo {
        color: #3B82F6; font-size: 30px; font-weight: 900;
        margin-top: 20px; letter-spacing: -1px;
    }
    QLabel#logo_sub {
        color: #FFFFFF; font-size: 11px; font-weight: 700;
        margin-bottom: 25px; border-bottom: 1px solid #1E293B; padding-bottom: 15px;
    }
    
    /* Tombol Navigasi Normal (Terbuka) */
    QPushButton#nav_button {
        background-color: transparent; color: #E2E8F0;
        text-align: left; padding: 12px 15px; font-size: 14px; font-weight: 600;
        border-radius: 12px; margin: 4px 15px; border: none;
    }
    QPushButton#nav_button:hover { background-color: #1E293B; color: #FFFFFF; border: none; }
    QPushButton#nav_button:checked { background-color: #2563EB; color: #FFFFFF; border: none; }
    
    /* Tombol Navigasi Saat Sidebar Menyusut (Tengah Sempurna) */
    QPushButton#nav_button[collapsed="true"] {
        text-align: center;
        padding: 12px 0px; /* KUNCI: Samakan padding atas/bawah dengan tombol normal (12px) */
        margin: 4px 16px; 
    }

    /* ================= HEADER & CARD ================= */
    QLabel#header_title { color: #1E293B; font-size: 26px; font-weight: 800; background-color: transparent; }
    QLabel#header_subtitle { color: #475569; font-size: 14px; margin-bottom: 15px; background-color: transparent; }
    
    QFrame#content_card {
        background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px;
    }

    /* ================= BUTTONS (Tombol Umum) ================= */
    QPushButton {
        background-color: #FFFFFF; color: #334155;
        border: 1px solid #E2E8F0; border-radius: 6px;
        padding: 8px 14px; font-weight: 600; font-size: 13px;
    }
    QPushButton:hover { background-color: #F1F5F9; border: 1px solid #CBD5E1; }
    
    QPushButton#btn_sil { background-color: #EF4444; color: #FFFFFF; border: none; }
    QPushButton#btn_sil:hover { background-color: #DC2626; }
    
    QPushButton#btn_kaydet { background-color: #2563EB; color: #FFFFFF; border: none; }
    QPushButton#btn_kaydet:hover { background-color: #1D4ED8; }

    /* ================= INPUT & TABLE ================= */
    QLineEdit {
        background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px;
        padding: 8px 12px; color: #0F172A; font-size: 13px;
    }
    QLineEdit:focus { border: 1px solid #3B82F6; }

    QTableWidget {
        background-color: #FFFFFF; border: none; gridline-color: #F1F5F9;
        color: #334155; font-size: 13px; border-top: 1px solid #E2E8F0;
    }
    QTableWidget::item { padding: 12px; border-bottom: 1px solid #F1F5F9; }
    QHeaderView::section {
        background-color: #F8FAFC; color: #0F172A; padding: 12px;
        font-weight: 700; border: none; border-bottom: 1px solid #E2E8F0; text-align: left;
    }
    
    QGroupBox { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; margin-top: 15px; padding: 15px; }
    QGroupBox::title { subcontrol-origin: margin; left: 10px; background-color: #FFFFFF; color: #2563EB; font-weight: bold; }
    """