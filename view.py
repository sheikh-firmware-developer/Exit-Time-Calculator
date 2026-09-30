import tkinter as tk
from tkinter import ttk

class TrackerView:
    def __init__(self, root, current_palette, settings):
        self.root = root
        self.root.title("TimeTracker HUD")
        self.root.geometry("300x230") 
        self.root.resizable(False, False)
        
        self.p = current_palette
        self.settings = settings
        
        self.main_container = tk.Frame(self.root, bg=self.p["bg"])
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        self.setup_main_ui()

    def setup_main_ui(self):
        # 1. Seamless Single-Line HUD Component
        self.hud_frame = tk.Frame(self.main_container, bg=self.p["bg"])
        self.hud_frame.pack(fill=tk.X, padx=(45,10), pady=(5, 2))
        
        self.lbl_day_date = tk.Label(self.hud_frame, text="", font=("Segoe UI Semibold", 11), fg=self.p["muted"], bg=self.p["bg"])
        self.lbl_day_date.pack(side=tk.LEFT, padx=(0, 2))
        
        self.lbl_divider = tk.Label(self.hud_frame, text="•", font=("Segoe UI Semibold", 11), fg=self.p["muted"], bg=self.p["bg"])
        self.lbl_divider.pack(side=tk.LEFT, padx=5)
        
        self.lbl_clock = tk.Label(self.hud_frame, text="", font=("Segoe UI", 12, "bold"), fg=self.p["accent"], bg=self.p["bg"])
        self.lbl_clock.pack(side=tk.LEFT, padx=2)
        
        self.btn_settings = tk.Button(self.hud_frame, text="⚙️", font=("Segoe UI", 12), bd=0, bg=self.p["bg"], fg=self.p["accent"], activebackground=self.p["bg"], cursor="hand2")
        self.btn_settings.pack(side=tk.RIGHT)

        # 2. Main Calculation Display Engine Panel
        self.calc_lf = tk.LabelFrame(self.main_container, text=" Business Hours Calculator ", bg=self.p["bg"], fg=self.p["text"], font=("Segoe UI Bold", 9))
        self.calc_lf.pack(fill=tk.BOTH, expand=True, padx=5, pady=5, ipady=2)
        
        self.lbl_punch_prompt = tk.Label(self.calc_lf, text="You Entered Office At:", font=("Segoe UI", 10), bg=self.p["bg"], fg=self.p["muted"])
        self.lbl_punch_prompt.pack(pady=4)
        
        self.input_container = tk.Frame(self.calc_lf, bg=self.p["bg"])
        self.input_container.pack()
        
        self.entry = tk.Entry(self.input_container, font=("Segoe UI", 14, "bold"), width=8, justify="center", bd=1, relief="solid")
        self.entry.pack(side=tk.LEFT, padx=5)
        
        self.btn_ampm = tk.Button(self.input_container, text="AM", font=("Segoe UI", 10, "bold"), relief="flat", width=4)
        self.btn_ampm.pack(side=tk.LEFT, padx=5)
        
        self.lbl_result = tk.Label(self.calc_lf, text="---", font=("Segoe UI", 15, "bold"), bg=self.p["bg"], fg=self.p["muted"])
        self.lbl_result.pack(pady=6)
        
        # FIXED: Added wraplength=280 to prevent long sentences from leaving the window view
        self.lbl_warn = tk.Label(self.calc_lf, text="", font=("Segoe UI Semibold", 9), bg=self.p["bg"], justify="center", wraplength=280)
        self.lbl_warn.pack(pady=2)

        self.apply_theme_to_main()

    def show_config_overlay(self, save_command, cancel_command, strict_toggle_command, sl_toggle_command, theme_command):
        self.overlay_frame = tk.Frame(self.root, bg=self.p["bg"])
        self.overlay_frame.place(x=0, y=0, relwidth=1.0, relheight=1.0)

        config_lf = tk.LabelFrame(self.overlay_frame, text=" Configuration Settings ", bg=self.p["bg"], fg=self.p["text"], font=("Segoe UI Bold", 9))
        config_lf.pack(fill=tk.BOTH, expand=True, padx=5, pady=5, ipady=2)

        tk.Label(config_lf, text="Target Hours:", bg=self.p["bg"], fg=self.p["text"]).grid(row=0, column=0, sticky="w", padx=10, pady=4)
        hours_options = [f"{h/2:.1f}" for h in range(10, 21)]
        self.ent_hours = ttk.Combobox(config_lf, values=hours_options, width=5, font=("Segoe UI", 9), state="readonly", justify="center")
        self.ent_hours.grid(row=0, column=1, padx=1, pady=4)
        self.ent_hours.set(self.settings.get("work_hours", "8.5"))

        self.var_strict = tk.BooleanVar(value=self.settings.get("strict_mode", True))
        self.chk_strict = tk.Checkbutton(config_lf, text="Enforce Rules", variable=self.var_strict, bg=self.p["bg"], fg=self.p["text"], selectcolor=self.p["surface"], activebackground=self.p["bg"], command=strict_toggle_command)
        self.chk_strict.grid(row=0, column=2, columnspan=2, padx=10, pady=4, sticky="e")

        tk.Label(config_lf, text="In-Time Guard:", bg=self.p["bg"], fg=self.p["text"]).grid(row=1, column=0, sticky="w", padx=10, pady=4)
        self.ent_start = tk.Entry(config_lf, width=9, font=("Segoe UI", 9), justify="center", bd=1, relief="solid", bg=self.p["entry_bg"], fg=self.p["text"])
        self.ent_start.grid(row=1, column=1, padx=0, pady=4)
        self.ent_start.insert(0, self.settings.get("intime_start", "08:30 AM"))
        
        tk.Label(config_lf, text="to", bg=self.p["bg"], fg=self.p["text"]).grid(row=1, column=2, padx=0, pady=4)
        self.ent_end = tk.Entry(config_lf, width=9, font=("Segoe UI", 9), justify="center", bd=1, relief="solid", bg=self.p["entry_bg"], fg=self.p["text"])
        self.ent_end.grid(row=1, column=3, padx=0, pady=4)
        self.ent_end.insert(0, self.settings.get("intime_end", "10:00 AM"))

        self.var_sl_enable = tk.BooleanVar(value=self.settings.get("short_leave_enabled", False))
        self.chk_sl = tk.Checkbutton(config_lf, text="Short Leave Option", variable=self.var_sl_enable, bg=self.p["bg"], fg=self.p["text"], selectcolor=self.p["surface"], activebackground=self.p["bg"], command=sl_toggle_command)
        self.chk_sl.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=4)

        sl_durations = ["1.0", "1.5", "2.0", "2.5", "3.0"]
        self.ent_sl_hours = ttk.Combobox(config_lf, values=sl_durations, width=4, font=("Segoe UI", 9), state="readonly", justify="center")
        self.ent_sl_hours.grid(row=2, column=2, padx=2, pady=4, sticky="w")
        self.ent_sl_hours.set(self.settings.get("short_leave_hours", "2.0"))
        tk.Label(config_lf, text="hrs", bg=self.p["bg"], fg=self.p["text"]).grid(row=2, column=3, sticky="w", pady=4)

        tk.Label(config_lf, text="Club Leave At:", bg=self.p["bg"], fg=self.p["text"]).grid(row=3, column=0, sticky="w", padx=10, pady=4)
        self.ent_sl_pos = ttk.Combobox(config_lf, values=["Start", "End"], width=6, font=("Segoe UI", 9), state="readonly", justify="center")
        self.ent_sl_pos.grid(row=3, column=1, padx=2, pady=4, sticky="w")
        self.ent_sl_pos.set(self.settings.get("short_leave_position", "End"))

        btn_container = tk.Frame(config_lf, bg=self.p["bg"])
        btn_container.grid(row=4, column=0, columnspan=4, padx=10, pady=8, sticky="ew")
        
        btn_cancel = tk.Button(
            btn_container, 
            text="Cancel", 
            font=("Segoe UI Semibold", 8), 
            bd=0, 
            relief="solid", 
            highlightthickness=1, 
            highlightbackground=self.p["border"], 
            bg=self.p["surface"], 
            fg=self.p["text"], 
            width=12, 
            command=cancel_command
        )
        btn_cancel.pack(side=tk.LEFT, padx=5)
        
        btn_save = tk.Button(
            btn_container, 
            text="Save Setup", 
            font=("Segoe UI Semibold", 8), 
            bd=0, 
            relief="solid", 
            highlightthickness=1, 
            highlightbackground=self.p["accent"], 
            bg=self.p["accent"], 
            fg=self.p["bg"], 
            width=16, 
            command=save_command
        )
        btn_save.pack(side=tk.RIGHT, padx=5)

        theme_frame = tk.Frame(self.overlay_frame, bg=self.p["bg"])
        theme_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=8, padx=20)
        tk.Label(theme_frame, text="Theme Mode:", font=("Segoe UI", 8), bg=self.p["bg"], fg=self.p["muted"]).pack(side=tk.LEFT, padx=2)
        for t_option in ["Light", "Dark", "System"]:
            btn = tk.Button(theme_frame, text=t_option, font=("Segoe UI Semibold", 8), relief="flat", bg=self.p["surface"], fg=self.p["text"], command=lambda opt=t_option: theme_command(opt))
            btn.pack(side=tk.LEFT, padx=3)

    def hide_config_overlay(self):
        if hasattr(self, 'overlay_frame') and self.overlay_frame.winfo_exists():
            self.overlay_frame.destroy()

    def apply_theme_to_main(self):
        self.root.configure(bg=self.p["bg"])
        self.main_container.config(bg=self.p["bg"])
        self.hud_frame.config(bg=self.p["bg"])
        self.calc_lf.config(bg=self.p["bg"], fg=self.p["text"])
        self.input_container.config(bg=self.p["bg"])
        
        self.lbl_day_date.config(bg=self.p["bg"], fg=self.p["muted"])
        self.lbl_divider.config(bg=self.p["bg"], fg=self.p["muted"])
        self.lbl_clock.config(bg=self.p["bg"], fg=self.p["accent"])
        self.lbl_punch_prompt.config(bg=self.p["bg"], fg=self.p["muted"])
        self.lbl_result.config(bg=self.p["bg"])
        self.lbl_warn.config(bg=self.p["bg"])
        self.btn_settings.config(bg=self.p["bg"], fg=self.p["accent"], activebackground=self.p["bg"])
        self.entry.config(bg=self.p["entry_bg"], fg=self.p["text"], insertbackground=self.p["text"])

    def update_theme(self, new_palette):
        self.p = new_palette
        self.apply_theme_to_main()
        
        if hasattr(self, 'overlay_frame') and self.overlay_frame.winfo_exists():
            if hasattr(self, 'btn_cancel') and self.btn_cancel.winfo_exists():
                self.btn_cancel.config(highlightbackground=self.p["border"])
            if hasattr(self, 'btn_save') and self.btn_save.winfo_exists():
                self.btn_save.config(highlightbackground=self.p["accent"])
                
        self.hide_config_overlay()
