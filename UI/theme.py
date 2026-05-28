def get_stylesheet():
    return """
    /* Global Styling */
    QMainWindow { background-color: #0F172A; font-family: 'Segoe UI', Arial, sans-serif; }
    QWidget { font-family: 'Segoe UI', Arial, sans-serif; }

    /* ================= SIDEBAR ================= */
    QFrame#sidebar { background-color: #020617; }
    QFrame#sidebar QLabel { background-color: transparent; }
    
    QLabel#logo {
        color: #3B82F6; font-size: 30px; font-weight: 900;
        margin-top: 20px; letter-spacing: -1px;
    }
    QLabel#logo_sub {
        color: #94A3B8; font-size: 11px; font-weight: 700;
        margin-bottom: 25px; border-bottom: 1px solid #1E293B; padding-bottom: 15px;
    }
    
    QPushButton#nav_button {
        background-color: transparent; color: #94A3B8;
        text-align: left; padding: 12px 15px; font-size: 14px; font-weight: 600;
        border-radius: 12px; margin: 4px 15px; border: none;
    }
    QPushButton#nav_button:hover { background-color: #1E293B; color: #F8FAFC; border: none; }
    QPushButton#nav_button:checked { background-color: #3B82F6; color: #FFFFFF; border: none; }
    QPushButton#nav_button[collapsed="true"] { text-align: center; padding: 12px 0px; margin: 4px 16px; }

    /* ================= HEADER & CARD ================= */
    QLabel#header_title { color: #F8FAFC; font-size: 26px; font-weight: 800; background-color: transparent; }
    QLabel#header_subtitle { color: #94A3B8; font-size: 14px; margin-bottom: 15px; background-color: transparent; }
    QFrame#content_card { background-color: #1E293B; border: 1px solid #334155; border-radius: 12px; }

    /* ================= BUTTONS & INPUT ================= */
    QPushButton {
        background-color: #0F172A; color: #F8FAFC; border: 1px solid #334155;
        border-radius: 6px; padding: 8px 14px; font-weight: 600; font-size: 13px;
    }
    QPushButton:hover { background-color: #334155; border: 1px solid #475569; }
    QPushButton#btn_sil { background-color: #EF4444; color: #FFFFFF; border: none; }
    QPushButton#btn_sil:hover { background-color: #DC2626; }
    QPushButton#btn_kaydet { background-color: #2563EB; color: #FFFFFF; border: none; }
    QPushButton#btn_kaydet:hover { background-color: #1D4ED8; }

    QLineEdit {
        background-color: #0F172A; border: 1px solid #334155; border-radius: 6px;
        padding: 8px 12px; color: #F8FAFC; font-size: 13px;
    }
    QLineEdit:focus { border: 1px solid #3B82F6; }

    /* ================= TABEL PREMIUM (DARK MODE) ================= */
    QTableWidget {
        background-color: #1E293B; 
        alternate-background-color: #0F172A; /* Efek selang-seling */
        border: 1px solid #334155; 
        border-radius: 8px;
        color: #E2E8F0; 
        font-size: 13px;
        outline: none;
    }
    QTableWidget::item { 
        padding: 12px; 
        border-bottom: 1px solid #334155; 
    }
    QTableWidget::item:selected { 
        background-color: #3B82F6; 
        color: #FFFFFF; 
        font-weight: bold;
    }
    QTableWidget::item:hover {
        background-color: #334155; /* Efek highlight saat mouse lewat */
    }
    
    QHeaderView::section {
        background-color: #020617; 
        color: #94A3B8; 
        padding: 15px 12px;
        font-weight: 800; 
        font-size: 13px;
        border: none; 
        border-bottom: 3px solid #3B82F6; /* Aksen garis biru */
        text-align: left;
    }
    QHeaderView {
        background-color: #020617;
    }
    """