import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil

# --- KONFIGURÁCIÓ ---
BASE_IMAGE_FOLDER = "images"

class SonicAdminApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SonicOnBox Admin Tool v3.0 - Folder Support")
        self.root.geometry("600x850")
        self.root.configure(bg="#2c3e50")

        style = ttk.Style()
        style.theme_use('clam')
        
        # --- UI ELEMEK ---
        self.create_label("1. Melyik oldalt szerkesztjük?", "#f1c40f")
        self.file_type = tk.StringVar(value="downloads.html")
        ttk.Radiobutton(root, text="Downloads (Modok)", variable=self.file_type, value="downloads.html").pack(pady=2)
        ttk.Radiobutton(root, text="Commission (Munkák)", variable=self.file_type, value="commission.html").pack(pady=2)

        self.create_label("2. Adatok megadása", "#ecf0f1")
        
        self.create_input_label("Név / Cím:")
        self.entry_name = ttk.Entry(root, width=50)
        self.entry_name.pack()

        self.create_input_label("Játék Kategória:")
        self.combo_game = ttk.Combobox(root, values=[
            "generations", "shadow_gen", "frontiers", "superstars", "unleashed", 
            "colors", "forces", "lost_world", "sadx", "sa2", "06", "mania", "origins"
        ], width=47)
        self.combo_game.pack()
        self.combo_game.set("generations")

        self.create_input_label("Leírás:")
        self.text_desc = tk.Text(root, height=4, width=50)
        self.text_desc.pack()

        self.create_input_label("Egyedi ID (fájlnevekhez, pl: metal_sonic):")
        self.entry_id = ttk.Entry(root, width=50)
        self.entry_id.pack()

        self.create_input_label("Letöltési Link:")
        self.entry_link = ttk.Entry(root, width=50)
        self.entry_link.pack()

        # --- ÚJ RÉSZ: MAPPA VÁLASZTÓ ---
        self.create_label("3. Képek és Mappa", "#e74c3c")
        
        self.create_input_label("Melyik mappába kerüljenek a képek? (images/...)")
        
        # Mappák beolvasása az images/ alól
        subfolders = self.scan_subfolders()
        self.combo_folder = ttk.Combobox(root, values=subfolders, width=47)
        self.combo_folder.pack()
        self.combo_folder.set("") # Alapértelmezett: gyökér (üres)
        
        tk.Label(root, text="(Válassz a listából, vagy írj be újat a létrehozáshoz!)", bg="#2c3e50", fg="#bdc3c7", font=("Arial", 8)).pack()

        self.btn_select_imgs = tk.Button(root, text="Képek Kiválasztása...", command=self.select_images, bg="#3498db", fg="white", font=("Arial", 10, "bold"))
        self.btn_select_imgs.pack(pady=10)
        
        self.lbl_img_status = tk.Label(root, text="Nincs kép kiválasztva", bg="#2c3e50", fg="#bdc3c7")
        self.lbl_img_status.pack()

        self.selected_images = []
        
        tk.Button(root, text="💾 MENTÉS ÉS GENERÁLÁS", command=self.generate_and_save, bg="#27ae60", fg="white", font=("Arial", 12, "bold"), height=2, width=30).pack(pady=20)

    def scan_subfolders(self):
        """Visszaadja az images mappa almappáit."""
        folders = [""] # Az üres string jelenti az images gyökerét
        if os.path.exists(BASE_IMAGE_FOLDER):
            for item in os.listdir(BASE_IMAGE_FOLDER):
                if os.path.isdir(os.path.join(BASE_IMAGE_FOLDER, item)):
                    folders.append(item)
        return folders

    def create_label(self, text, color):
        tk.Label(self.root, text=text, bg="#2c3e50", fg=color, font=("Arial", 11, "bold")).pack(pady=(15, 5))

    def create_input_label(self, text):
        tk.Label(self.root, text=text, bg="#2c3e50", fg="white", font=("Arial", 9)).pack(pady=(5, 0))

    def select_images(self):
        file_paths = filedialog.askopenfilenames(title="Válassz képeket", filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if file_paths:
            self.selected_images = file_paths
            self.lbl_img_status.config(text=f"{len(file_paths)} kép kiválasztva.")

    def generate_and_save(self):
        # 1. Adatok begyűjtése
        target_file = self.file_type.get()
        name = self.entry_name.get()
        game = self.combo_game.get()
        desc = self.text_desc.get("1.0", tk.END).strip()
        rid = self.entry_id.get()
        link = self.entry_link.get()
        subfolder = self.combo_folder.get().strip()

        if not name or not rid or not link:
            messagebox.showerror("Hiba", "A Név, ID és Link mezők kötelezőek!")
            return

        # 2. Célmappa meghatározása
        # Ha a subfolder üres, akkor 'images/', ha van, akkor 'images/subfolder/'
        final_folder_path = os.path.join(BASE_IMAGE_FOLDER, subfolder) if subfolder else BASE_IMAGE_FOLDER
        
        # HTML src path (amit a weboldal használ): 'images/almappa/' vagy 'images/'
        web_path_prefix = f"images/{subfolder}/" if subfolder else "images/"

        # 3. Képek másolása
        img_html = ""
        if self.selected_images:
            if not os.path.exists(final_folder_path):
                try:
                    os.makedirs(final_folder_path) # Létrehozza a mappát, ha nincs
                except OSError as e:
                    messagebox.showerror("Hiba", f"Nem tudtam létrehozni a mappát: {e}")
                    return
            
            for index, img_path in enumerate(self.selected_images):
                ext = os.path.splitext(img_path)[1]
                # Új név: ID + sorszám + soniconbox + kiterjesztés
                new_filename = f"{rid}_soniconbox{index+1}{ext}"
                dest_path = os.path.join(final_folder_path, new_filename)
                
                # HTML-hez a relatív útvonal kell
                final_web_src = f"{web_path_prefix}{new_filename}"

                try:
                    shutil.copy(img_path, dest_path)
                    img_html += f'<img src="{final_web_src}" onclick="openLightbox(this)" onerror="this.src=\'https://via.placeholder.com/150\'">\n                            '
                except Exception as e:
                    messagebox.showerror("Hiba", f"Nem sikerült a képmásolás: {str(e)}")
                    return

        # 4. HTML Blokk Generálása
        new_block = ""
        
        if target_file == "commission.html":
            new_block = f"""
            <div class="work-card" data-game="{game}" style="display: flex;">
                <div class="work-header">
                    <span class="work-title">{name}</span>
                    <span class="work-version">v1.0</span>
                    <span class="game-tag">{game.upper()}</span>
                </div>
                <div class="work-content">
                    <div class="work-info">
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
                <div class="mod-header"><span class="mod-title">{name}</span><span class="game-tag">{game.upper()}</span></div>
                <div class="mod-content">
                    <div class="mod-info"><p><strong>Description:</strong></p><p>{desc}</p><a href="redirect.html?id={rid}&link={link}" target="_blank" class="download-btn">Link</a></div>
                    <div class="mod-previews"><div class="preview-grid gallery">{img_html}</div></div>
                </div>
            </div>"""

        # 5. Fájlba írás (Beszúrás a lista elejére)
        try:
            with open(target_file, "r", encoding="utf-8") as f:
                content = f.read()

            insert_pos = -1
            
            if target_file == "commission.html":
                # Keresés a dinamikus tartalom elejére
                # Ha van már elem, elé szúrjuk, ha nincs, a mainContent elejére (a statikusok után)
                # Egyszerűsített logika: Próbáljuk a 'prices' után tenni közvetlenül a következő work-card elé.
                
                # Megkeressük az első olyan kártyát, aminek van 'data-game' attribútuma (tehát mod)
                first_dynamic_idx = content.find('class="work-card" data-game=')
                
                if first_dynamic_idx != -1:
                    # Ha találtunk modot, visszakeresünk a nyitó div-jéig
                    insert_pos = content.rfind('<div', 0, first_dynamic_idx)
                else:
                    # Ha még nincs mod, akkor a statikus elemek után (pl. prices)
                    # Ha a prices sincs meg, akkor a mainContent elejére
                    prices_marker = 'id="prices"'
                    prices_idx = content.find(prices_marker)
                    if prices_idx != -1:
                        # Prices div vége
                        close_div = content.find('</div>', prices_idx)
                        # Még egy </div> a tartalma miatt? Nem, a work-card sima div.
                        # Biztonságosabb pont: A mainContent vége előtt? Nem, az aljára tenné.
                        # Tegyük a mainContentbe, de keressük meg a végét és szúrjunk elé? Nem, az a sorrend vége.
                        
                        # Megoldás: Keressük meg a "content-area" div kezdetét, 
                        # és ugorjunk át 3 db work-card-ot (Info, OC, Prices).
                        # Ez bonyolult szövegesen.
                        
                        # Egyszerűbb: Szúrjuk be a 'prices' div ZÁRÓ tagje után.
                        # Ehhez meg kell találni a 'prices' div végét.
                        # Mivel a 'prices' div tartalma változhat, keressük a következő '<div class="work-card"' vagy 'footer'-t.
                        pass # A fenti first_dynamic_idx logika lefedi, ha van már elem.
                    
                    # Ha nincs dinamikus elem, de van prices, akkor a prices után kéne.
                    # Mivel ez bonyolult parser nélkül, egy trükk:
                    # Ha nem talál dinamikus elemet, beszúrja a mainContent végére (a lezáró </div> elé).
                    end_marker = 'id="mainContent">'
                    start_pos = content.find(end_marker)
                    if start_pos != -1:
                        # Keressük meg a content-area lezáró divjét.
                        # Ez kockázatos.
                        # Inkább: Ha nincs dinamikus elem, szúrjuk be az "oc-characters" után?
                        insert_pos = content.rfind('<div id="prices"') 
                        # Ez még mindig csak az eleje.
                        
                        # VÉGSŐ MEGOLDÁS HA ÜRES A LISTA: 
                        # Ha nincs dinamikus elem, beszúrjuk a </body> elé? Nem.
                        # Tegyük fel, hogy van legalább egy statikus elem.
                        # Szúrjuk be a prices után. Mivel nem tudjuk hol a vége,
                        # keressük meg a prices utáni első </div>-et? Nem biztos.
                        
                        # Maradjunk a bevált módszernél: Ha van dinamikus elem, elé.
                        # Ha nincs, akkor a 'prices' szöveg előfordulása utáni részre? 
                        # Tegyük fel, hogy a usernek már van tartalom (mint a példádban).
                        # A te fájlodban ott vannak a "Generations" modok.
                        # Tehát a `first_dynamic_idx` működni fog.
                        pass

            else: # downloads.html
                marker = 'id="modContainer">'
                idx = content.find(marker)
                if idx != -1:
                    insert_pos = idx + len(marker)

            if insert_pos != -1:
                final_content = content[:insert_pos] + "\n" + new_block + content[insert_pos:]
                
                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(final_content)
                
                # Frissítjük a mappa listát (ha újat írt be a user)
                self.combo_folder['values'] = self.scan_subfolders()
                
                messagebox.showinfo("Siker!", f"Hozzáadva a {target_file}-hez!\nKépek mentve ide: {web_path_prefix}")
                
                # Mezők tisztítása
                self.entry_name.delete(0, tk.END)
                self.entry_id.delete(0, tk.END)
                self.entry_link.delete(0, tk.END)
                self.text_desc.delete("1.0", tk.END)
                self.selected_images = []
                self.lbl_img_status.config(text="Nincs kép kiválasztva")
                
            else:
                messagebox.showerror("Hiba", "Nem találtam a beszúrási pontot. (Van már legalább egy mod feltöltve, vagy a 'modContainer'?)")

        except Exception as e:
            messagebox.showerror("Hiba", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SonicAdminApp(root)
    root.mainloop()