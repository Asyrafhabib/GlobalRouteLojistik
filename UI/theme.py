def get_stylesheet():
    return """
    /* Global Styling */
    QMainWindow { background-color: #121212; font-family: 'Segoe UI', Arial, sans-serif; }
    QWidget { font-family: 'Segoe UI', Arial, sans-serif; color: #E0E0E0; }

    /* ================= SIDEBAR ================= */
    QFrame#sidebar { background-color: #181818; border-right: 1px solid #2B2B2B; }
    QFrame#sidebar QLabel { background-color: transparent; }
    
    QLabel#logo { color: #007ACC; font-size: 30px; font-weight: 900; margin-top: 20px; letter-spacing: -1px; }
    QLabel#logo_sub { color: #858585; font-size: 11px; font-weight: 700; margin-bottom: 25px; border-bottom: 1px solid #2B2B2B; padding-bottom: 15px; }
    
    QPushButton#nav_button { background-color: transparent; color: #9D9D9D; text-align: left; padding: 12px 15px; font-size: 14px; font-weight: 600; border-radius: 8px; margin: 4px 15px; border: none; }
    QPushButton#nav_button:hover { background-color: #2D2D2D; color: #FFFFFF; }
    QPushButton#nav_button:checked { background-color: #007ACC; color: #FFFFFF; font-weight: 700; }
    QPushButton#nav_button[collapsed="true"] { text-align: center; padding: 12px 0px; margin: 4px 16px; }

    /* ================= HEADER & CARD ================= */
    QLabel#header_title { color: #FFFFFF; font-size: 26px; font-weight: 800; background-color: transparent; }
    QLabel#header_subtitle { color: #858585; font-size: 14px; margin-bottom: 15px; background-color: transparent; }
    QFrame#content_card { background-color: #1E1E1E; border: 1px solid #2B2B2B; border-radius: 10px; }

    /* ================= BUTTONS & INPUT ================= */
    QPushButton { background-color: #252526; color: #E0E0E0; border: 1px solid #3E3E42; border-radius: 6px; padding: 8px 14px; font-weight: 600; font-size: 13px; }
    QPushButton:hover { background-color: #3E3E42; border: 1px solid #555555; }
    QPushButton#btn_sil { background-color: #D32F2F; color: #FFFFFF; border: none; }
    QPushButton#btn_sil:hover { background-color: #B71C1C; }
    QPushButton#btn_kaydet { background-color: #007ACC; color: #FFFFFF; border: none; }
    QPushButton#btn_kaydet:hover { background-color: #005A9E; }
    QPushButton#btn_sorgula { background-color: #007ACC; color: #FFFFFF; border: none; }
    QPushButton#btn_sorgula:hover { background-color: #005A9E; }

    QLineEdit { background-color: #252526; border: 1px solid #3E3E42; border-radius: 6px; padding: 8px 12px; color: #FFFFFF; font-size: 13px; }
    QLineEdit:focus { border: 1px solid #007ACC; background-color: #1E1E1E; }

    /* ================= TABEL PREMIUM ================= */
    QTableWidget { background-color: #1E1E1E; alternate-background-color: #252526; border: 1px solid #2B2B2B; border-radius: 6px; color: #CCCCCC; font-size: 13px; outline: none; }
    QTableWidget::item { padding: 12px; border-bottom: 1px solid #2B2B2B; }
    QTableWidget::item:selected { background-color: #007ACC; color: #FFFFFF; font-weight: bold; }
    QTableWidget::item:hover { background-color: #2D2D2D; }
    
    QHeaderView::section { background-color: #181818; color: #A6A6A6; padding: 12px; font-weight: 700; font-size: 13px; border: none; border-bottom: 2px solid #007ACC; text-align: left; }
    QHeaderView { background-color: #181818; }
    """