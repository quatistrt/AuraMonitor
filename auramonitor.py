import customtkinter as ctk
import psutil
import platform
import threading
import time
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AuraMonitor(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AuraMonitor - Modern System Performance")
        self.geometry("900x600")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.colors = {
            "bg": "#121212",
            "sidebar": "#1E1E1E",
            "accent": "#7C4DFF",
            "text": "#E0E0E0",
            "cpu": "#FF5252",
            "ram": "#448AFF",
            "disk": "#00E676"
        }

        self.setup_ui()
        self.start_monitoring()

    def setup_ui(self):
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=self.colors["sidebar"])
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="AURA\nMONITOR", font=ctk.CTkFont(size=24, weight="bold"), text_color=self.colors["accent"])
        self.logo_label.pack(pady=(30, 50))

        self.status_label = ctk.CTkLabel(self.sidebar, text="Sistem Durumu: Aktif", text_color="#00E676", font=ctk.CTkFont(size=12))
        self.status_label.pack(side="bottom", pady=20)

        self.main_frame = ctk.CTkScrollableFrame(self, fg_color=self.colors["bg"])
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.header = ctk.CTkLabel(self.main_frame, text="Sistem Performans Özeti", font=ctk.CTkFont(size=22, weight="bold"))
        self.header.pack(anchor="w", pady=(0, 20))

        self.cards_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.cards_frame.pack(fill="x", pady=10)

        self.cpu_card = self.create_metric_card(self.cards_frame, "İŞLEMCİ (CPU)", self.colors["cpu"])
        self.cpu_card.pack(fill="x", pady=10)
        self.cpu_progress = self.create_progress(self.cpu_card, self.colors["cpu"])
        self.cpu_info = self.create_info_label(self.cpu_card)

        self.ram_card = self.create_metric_card(self.cards_frame, "BELLEK (RAM)", self.colors["ram"])
        self.ram_card.pack(fill="x", pady=10)
        self.ram_progress = self.create_progress(self.ram_card, self.colors["ram"])
        self.ram_info = self.create_info_label(self.ram_card)

        self.disk_card = self.create_metric_card(self.cards_frame, "DİSK KULLANIMI", self.colors["disk"])
        self.disk_card.pack(fill="x", pady=10)
        self.disk_progress = self.create_progress(self.disk_card, self.colors["disk"])
        self.disk_info = self.create_info_label(self.disk_card)

        self.details_header = ctk.CTkLabel(self.main_frame, text="Donanım Detayları", font=ctk.CTkFont(size=18, weight="bold"))
        self.details_header.pack(anchor="w", pady=(30, 10))

        self.details_frame = ctk.CTkFrame(self.main_frame, fg_color="#1E1E1E")
        self.details_frame.pack(fill="x", pady=10)

        self.hw_info = ctk.CTkLabel(self.details_frame, text=self.get_system_info(), justify="left", font=ctk.CTkFont(family="Consolas", size=12))
        self.hw_info.pack(padx=20, pady=20, anchor="w")

    def create_metric_card(self, parent, title, color):
        card = ctk.CTkFrame(parent, fg_color="#1E1E1E", height=120)
        label = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14, weight="bold"), text_color=color)
        label.pack(anchor="w", padx=20, pady=(15, 5))
        return card

    def create_progress(self, card, color):
        progress = ctk.CTkProgressBar(card, height=12, progress_color=color, fg_color="#333333")
        progress.pack(fill="x", padx=20, pady=5)
        progress.set(0)
        return progress

    def create_info_label(self, card):
        label = ctk.CTkLabel(card, text="Yükleniyor...", font=ctk.CTkFont(size=13))
        label.pack(anchor="w", padx=20, pady=(0, 15))
        return label

    def get_system_info(self):
        info = f"İşletim Sistemi: {platform.system()} {platform.release()}\n"
        info += f"İşlemci: {platform.processor()}\n"
        info += f"Makine: {platform.machine()}\n"
        info += f"CPU Çekirdek Sayısı: {psutil.cpu_count(logical=False)} Gerçek / {psutil.cpu_count(logical=True)} Mantıksal\n"
        
        mem = psutil.virtual_memory()
        info += f"Toplam RAM: {mem.total / (1024**3):.2f} GB"
        return info

    def start_monitoring(self):
        self.update_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.update_thread.start()

    def monitor_loop(self):
        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            self.cpu_progress.set(cpu_usage / 100)
            self.cpu_info.configure(text=f"Kullanım: %{cpu_usage:.1f}")

            mem = psutil.virtual_memory()
            self.ram_progress.set(mem.percent / 100)
            self.ram_info.configure(text=f"Kullanım: %{mem.percent:.1f} ({mem.used / (1024**3):.2f} GB / {mem.total / (1024**3):.2f} GB)")

            disk = psutil.disk_usage('/')
            self.disk_progress.set(disk.percent / 100)
            self.disk_info.configure(text=f"Kullanım: %{disk.percent:.1f} ({disk.used / (1024**3):.2f} GB / {disk.total / (1024**3):.2f} GB)")

            time.sleep(1)

if __name__ == "__main__":
    app = AuraMonitor()
    app.mainloop()
