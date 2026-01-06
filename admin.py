import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil

# --- DESIGN KONFIGURÁCIÓ (Színek) ---
COLORS = {
    "bg": "#1e1e2e",           # Sötét háttér
    "panel": "#252535",        # Panelek háttere
    "accent": "#00a8ff",       # Sonic Kék gombok
    "accent_hover": "#0097e6", # Gomb hover
    "text": "#f5f6fa",         # Fehér szöveg
    "text_sec": "#7f8fa6",     # Szürke szöveg
    "input_bg": "#353b48",     # Input mező háttér
    "success": "#4cd137",      # Zöld (Siker)
    "danger": "#e84118"        # Piros (Hiba)
}

BASE_IMAGE_FOLDER = "images"

class ModernSonicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SonicOnBox Studio v6.1 - Scroll Edition")
        # Kisebb ablakméret, hogy biztosan elférjen a képernyőn
        self.root.geometry("720x650") 
        self.root.configure(bg=COLORS["bg"])
        
        self.setup_styles()

        # --- GÖRGETHETŐ KERET LÉTREHOZÁSA (Scrollable Frame) ---
        # 1. Konténer
        container = tk.Frame(root, bg=COLORS["bg"])
        container.pack(fill="both", expand=True)

        # 2. Vászon (Canvas) és Görgetősáv (Scrollbar)
        self.canvas = tk.Canvas(container, bg=COLORS["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        
        # 3. Összekötés
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLORS["bg"])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # 4. Elrendezés
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 5. Egérgörgő támogatás
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)

        # --- INNENTŐL MINDEN AZ "scrollable_frame"-BE KERÜL ---
        
        # FŐ KONTÉNER (ami eddig a main_frame volt)
        main_frame = tk.Frame(self.scrollable_frame, bg=COLORS["bg"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 1. FEJLÉC
        header_frame = tk.Frame(main_frame, bg=COLORS["bg"])
        header_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(header_frame, text="SONIC ON BOX", font=("Segoe UI", 24, "bold"), 
                 bg=COLORS["bg"], fg=COLORS["accent"]).pack(side="left")
        tk.Label(header_frame, text="ADMIN TOOL", font=("Segoe UI", 24, "bold"), 
                 bg=COLORS["bg"], fg="white").pack(side="left", padx=10)

        # 2. TÍPUS VÁLASZTÓ
        type_frame = tk.Frame(main_frame, bg=COLORS["panel"], padx=10, pady=10)
        type_frame.pack(fill="x", pady=5)
        
        self.file_type = tk.StringVar(value="downloads.html")
        
        tk.Label(type_frame, text="MIT SZERKESZTÜNK?", font=("Segoe UI", 10, "bold"), 
                 bg=COLORS["panel"], fg=COLORS["text_sec"]).pack(anchor="w", pady=(0, 5))
        
        radio_style = {"bg": COLORS["panel"], "fg": COLORS["text"], "selectcolor": COLORS["bg"], "activebackground": COLORS["panel"], "activeforeground": COLORS["accent"]}
        
        rb1 = tk.Radiobutton(type_frame, text="DOWNLOADS (MODOK)", variable=self.file_type, value="downloads.html", font=("Segoe UI", 11), **radio_style)
        rb1.pack(side="left", padx=20)
        
        rb2 = tk.Radiobutton(type_frame, text="COMMISSIONS (MUNKÁK)", variable=self.file_type, value="commission.html", font=("Segoe UI", 11), **radio_style)
        rb2.pack(side="left", padx=20)

        # 3. ADATOK PANEL
        data_frame = tk.Frame(main_frame, bg=COLORS["panel"], padx=20, pady=20)
        data_frame.pack(fill="both", expand=True, pady=15)

        def create_entry(parent, label_text):
            tk.Label(parent, text=label_text.upper(), font=("Segoe UI", 8, "bold"), bg=COLORS["panel"], fg=COLORS["text_sec"]).pack(anchor="w", pady=(10, 0))
            entry = tk.Entry(parent, font=("Segoe UI", 11), bg=COLORS["input_bg"], fg="white", relief="flat", insertbackground="white")
            entry.pack(fill="x", ipady=8, pady=(5, 0))
            return entry

        # Név
        self.entry_name = create_entry(data_frame, "Név / Cím")
        
        # Játék lista
        tk.Label(data_frame, text="JÁTÉK KATEGÓRIA", font=("Segoe UI", 8, "bold"), bg=COLORS["panel"], fg=COLORS["text_sec"]).pack(anchor="w", pady=(15,0))
        self.combo_game = ttk.Combobox(data_frame, values=[
            "generations", "shadow_gen", "frontiers", "superstars", "unleashed", 
            "colors", "forces", "lost_world", "sadx", "sa2", "06", "mania", "origins", 
            "racing"
        ], font=("Segoe UI", 11))
        self.combo_game.pack(fill="x", ipady=4, pady=5)
        self.combo_game.set("generations")

        # Credits
        self.entry_credits = create_entry(data_frame, "Credits / Készítő (pl: @Sega)")

        # Leírás
        tk.Label(data_frame, text="LEÍRÁS", font=("Segoe UI", 8, "bold"), bg=COLORS["panel"], fg=COLORS["text_sec"]).pack(anchor="w", pady=(15,0))
        self.text_desc = tk.Text(data_frame, height=3, font=("Segoe UI", 11), bg=COLORS["input_bg"], fg="white", relief="flat", insertbackground="white")
        self.text_desc.pack(fill="x", pady=5)

        # ID és Verzió egy sorban
        row_frame_1 = tk.Frame(data_frame, bg=COLORS["panel"])
        row_frame_1.pack(fill="x", pady=5)
        
        col_id = tk.Frame(row_frame_1, bg=COLORS["panel"])
        col_id.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_id = create_entry(col_id, "EGYEDI ID (Fájlnévhez)")
        
        col_ver = tk.Frame(row_frame_1, bg=COLORS["panel"])
        col_ver.pack(side="right", fill="x", expand=True, padx=(10, 0))
        self.entry_ver = create_entry(col_ver, "VERZIÓ (Pl: v1.0)")

        # Link külön sorban
        self.entry_link = create_entry(data_frame, "LETÖLTÉSI LINK")

        # 4. KÉPEK ÉS MAPPA
        media_frame = tk.Frame(main_frame, bg=COLORS["panel"], padx=20, pady=20)
        media_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(media_frame, text="CÉL MAPPA (images/...) - Válassz vagy írj újat:", font=("Segoe UI", 8, "bold"), bg=COLORS["panel"], fg=COLORS["text_sec"]).pack(anchor="w")
        
        self.subfolders = self.scan_subfolders()
        self.combo_folder = ttk.Combobox(media_frame, values=self.subfolders, font=("Segoe UI", 11))
        self.combo_folder.pack(fill="x", ipady=4, pady=5)
        
        self.btn_select_imgs = tk.Button(media_frame, text="KÉPEK KIVÁLASZTÁSA", font=("Segoe UI", 10, "bold"), 
                                         bg="#4b4b4b", fg="white", relief="flat", cursor="hand2", command=self.select_images)
        self.btn_select_imgs.pack(fill="x", pady=10, ipady=5)
        
        self.lbl_img_status = tk.Label(media_frame, text="Nincs kép kiválasztva", font=("Segoe UI", 9), bg=COLORS["panel"], fg=COLORS["text_sec"])
        self.lbl_img_status.pack()

        # 5. MENTÉS GOMB
        self.btn_save = tk.Button(main_frame, text="GENERÁLÁS ÉS MENTÉS", font=("Segoe UI", 12, "bold"), 
                                  bg=COLORS["accent"], fg="white", relief="flat", cursor="hand2", command=self.generate_and_save)
        self.btn_save.pack(fill="x", ipady=10)

        # Alsó üres hely, hogy a gomb alatt is legyen tér görgetéskor
        tk.Label(main_frame, text="", bg=COLORS["bg"]).pack(pady=20)

        # Státusz sor (Külön a root ablak alján, nem görgethető)
        self.status_bar = tk.Label(root, text="Készzen áll.", bg="#15151e", fg="#777", anchor="w", padx=10, font=("Consolas", 9))
        self.status_bar.pack(side="bottom", fill="x")

        self.selected_images = []

    def _on_mousewheel(self, event):
        # Egérgörgő kezelése
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=COLORS["input_bg"], background=COLORS["panel"], foreground="white", arrowcolor="white")

    def scan_subfolders(self):
        folders = [""] 
        if os.path.exists(BASE_IMAGE_FOLDER):
            for item in os.listdir(BASE_IMAGE_FOLDER):
                if os.path.isdir(os.path.join(BASE_IMAGE_FOLDER, item)):
                    folders.append(item)
        return folders

    def select_images(self):
        file_paths = filedialog.askopenfilenames(title="Képek kiválasztása", filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if file_paths:
            self.selected_images = file_paths
            self.lbl_img_status.config(text=f"✓ {len(file_paths)} db kép kiválasztva", fg=COLORS["success"])
            self.btn_select_imgs.config(bg=COLORS["success"], text="KÉPEK KIVÁLASZTVA ✓")
        else:
            self.selected_images = []
            self.lbl_img_status.config(text="Nincs kép kiválasztva", fg=COLORS["text_sec"])
            self.btn_select_imgs.config(bg="#4b4b4b", text="KÉPEK KIVÁLASZTÁSA")

    def log(self, message, error=False):
        color = COLORS["danger"] if error else COLORS["success"]
        self.status_bar.config(text=message, fg=color)
        if error: messagebox.showerror("Hiba", message)
        else: messagebox.showinfo("Siker", message)

    def generate_and_save(self):
        target_file = self.file_type.get()
        name = self.entry_name.get()
        game = self.combo_game.get()
        credits = self.entry_credits.get().strip()
        desc = self.text_desc.get("1.0", tk.END).strip()
        rid = self.entry_id.get()
        link = self.entry_link.get()
        version = self.entry_ver.get().strip() 
        subfolder = self.combo_folder.get().strip()

        if not version: version = "v1.0"

        if not name or not rid or not link:
            self.log("A Név, ID és Link mezők kötelezőek!", True)
            return

        # HTML Kód a Credits részhez
        credits_html = ""
        if credits:
            credits_html = f'<p style="color:#f1c40f; margin-bottom:5px;"><strong>@Credits:</strong> {credits}</p>'

        final_folder_path = os.path.join(BASE_IMAGE_FOLDER, subfolder) if subfolder else BASE_IMAGE_FOLDER
        web_path_prefix = f"images/{subfolder}/" if subfolder else "images/"

        img_html = ""
        if self.selected_images:
            if not os.path.exists(final_folder_path):
                try:
                    os.makedirs(final_folder_path)
                except Exception as e:
                    self.log(f"Mappa hiba: {e}", True)
                    return
            
            for index, img_path in enumerate(self.selected_images):
                ext = os.path.splitext(img_path)[1]
                
                # Fájlnév: ID_szám_soniconbox.png
                new_filename = f"{rid}_{index+1}_soniconbox{ext}" 
                
                dest_path = os.path.join(final_folder_path, new_filename)
                final_web_src = f"{web_path_prefix}{new_filename}"

                try:
                    shutil.copy(img_path, dest_path)
                    img_html += f'<img src="{final_web_src}" onclick="openLightbox(this)" onerror="this.src=\'https://via.placeholder.com/150\'">\n                            '
                except Exception as e:
                    self.log(f"Másolási hiba: {e}", True)
                    return

        # HTML Generálás
        new_block = ""
        if target_file == "commission.html":
            new_block = f"""
            <div class="work-card" data-game="{game}" style="display: flex;">
                <div class="work-header">
                    <span class="work-title">{name}</span>
                    <span class="work-version">{version}</span>
                    <span class="game-tag">{game.upper()}</span>
                </div>
                <div class="work-content">
                    <div class="work-info">
                        {credits_html}
                        <p><strong>Description:</strong></p>
                        <p>{desc}</p>
                        <a href="redirect.html?id={rid}&link={link}" target="_blank" class="download-btn">Download</a>
                    </div>
                    <div class="work-previews">
                        <p><strong>Previews:</strong></p>
                        <div class="preview-grid gallery">
                            {img_html}
                        </div>
                    </div>
                </div>
            </div>"""
        else: # downloads.html
            new_block = f"""
            <div class="mod-card" data-game="{game}">
                <div class="mod-header">
                    <span class="mod-title">{name}</span>
                    <span class="mod-version" style="color:#bdc3c7; font-size:0.8em; margin-left:10px;">{version}</span>
                    <span class="game-tag">{game.upper()}</span>
                </div>
                <div class="mod-content">
                    <div class="mod-info">
                        {credits_html}
                        <p><strong>Description:</strong></p>
                        <p>{desc}</p>
                        <a href="redirect.html?id={rid}&link={link}" target="_blank" class="download-btn">Download</a>
                    </div>
                    <div class="mod-previews"><div class="preview-grid gallery">{img_html}</div></div>
                </div>
            </div>"""

        try:
            with open(target_file, "r", encoding="utf-8") as f:
                content = f.read()

            insert_pos = -1
            if target_file == "commission.html":
                first_dynamic_idx = content.find('class="work-card" data-game=')
                if first_dynamic_idx != -1:
                    insert_pos = content.rfind('<div', 0, first_dynamic_idx)
                else:
                    prices_marker = 'id="prices"'
                    prices_idx = content.find(prices_marker)
                    if prices_idx != -1:
                        pass
                    main_c = content.find('id="mainContent">')
                    if main_c != -1: insert_pos = main_c + len('id="mainContent">')

            else: # downloads
                marker = 'id="modContainer">'
                idx = content.find(marker)
                if idx != -1: insert_pos = idx + len(marker)

            if insert_pos != -1:
                final_content = content[:insert_pos] + "\n" + new_block + content[insert_pos:]
                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(final_content)
                
                # UI Reset
                self.combo_folder['values'] = self.scan_subfolders()
                self.entry_name.delete(0, tk.END)
                self.entry_id.delete(0, tk.END)
                self.entry_link.delete(0, tk.END)
                self.entry_ver.delete(0, tk.END)
                self.entry_credits.delete(0, tk.END)
                self.text_desc.delete("1.0", tk.END)
                self.selected_images = []
                self.lbl_img_status.config(text="Nincs kép kiválasztva", fg=COLORS["text_sec"])
                self.btn_select_imgs.config(bg="#4b4b4b", text="KÉPEK KIVÁLASZTÁSA")
                
                self.log(f"Sikeres mentés: {target_file}")
            else:
                self.log("Nem találtam a beszúrási helyet a HTML-ben.", True)

        except Exception as e:
            self.log(str(e), True)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernSonicApp(root)
    root.mainloop()