import os
from PyQt6.QtGui import QIcon

SVG_ASSETS = {
    # ================= LOGO UTAMA =================
    # Ganti kode <svg>...</svg> di bawah ini dengan kode SVG logo milikmu!
    "logo.svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 220"><g fill="none" stroke="#FFFFFF" stroke-width="12" stroke-linejoin="round" stroke-linecap="round"><polygon points="45,70 90,50 135,70 135,110 90,130 45,110"/><polyline points="45,70 90,90 135,70"/><line x1="90" y1="90" x2="90" y2="130"/></g><path d="M 30,90 C 20,160 120,160 155,85" fill="none" stroke="#FFFFFF" stroke-width="14" stroke-linecap="round"/><path d="M 155,85 Q 135,60 135,45 A 20,20 0 1,1 175,45 Q 175,60 155,85 Z" fill="none" stroke="#FFFFFF" stroke-width="12" stroke-linejoin="round"/><circle cx="155" cy="42" r="6" fill="#FFFFFF"/><text x="96" y="195" font-family="\'Segoe UI\', Arial, sans-serif" font-weight="900" font-size="52" text-anchor="middle" fill="#FFFFFF" letter-spacing="2">GRL</text></svg>',

    # ================= IKON SIDEBAR (Putih) =================
    "person.svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#FFFFFF"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>',
    "shipping.svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#FFFFFF"><path d="M20 8h-3V4H3c-1.1 0-2 .9-2 2v11h2c0 1.66 1.34 3 3 3s3-1.34 3-3h6c0 1.66 1.34 3 3 3s3-1.34 3-3h2v-5l-3-4zM6 18.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm13.5-9l1.96 2.5H17V9.5h2.5zm-1.5 9c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/></svg>',
    "store.svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#FFFFFF"><path d="M20 4H4v2h16V4zm1 10v-2l-1-5H4l-1 5v2h1v6h10v-6h4v6h2v-6h1zm-9 4H6v-4h6v4z"/></svg>',
    "history.svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#FFFFFF"><path d="M13 3c-4.97 0-9 4.03-9 9H1l3.89 3.89.07.14L9 12H6c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42C8.27 19.99 10.51 21 13 21c4.97 0 9-4.03 9-9s-4.03-9-9-9zm-1 5v5l4.28 2.54.72-1.21-3.5-2.08V8H12z"/></svg>',
    "dashboard.svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#FFFFFF"><path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/></svg>',
    
    # ================= IKON TOMBOL HAPUS (Putih) =================
    "delete.svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#FFFFFF"><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/></svg>',
    
    # ================= IKON TOMBOL TOOLBAR (Gelap) =================
    "add.svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#334155"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>',
    "edit.svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#334155"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg>',
    "refresh.svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#334155"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg>',
}

def ensure_icons_exist():
    if not os.path.exists("icons"):
        os.makedirs("icons")
    for filename, svg_content in SVG_ASSETS.items():
        filepath = os.path.join("icons", filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(svg_content)

def get_icon(filename: str) -> QIcon:
    ensure_icons_exist()
    filepath = os.path.join("icons", f"{filename}.svg")
    return QIcon(filepath)