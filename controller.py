import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

class TrackerController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.bind_main_events()
        self.refresh_ampm_button_color()
        self.calculate_exit_metrics()

    def bind_main_events(self):
        self.view.btn_settings.config(command=self.handle_open_settings)
        self.view.btn_ampm.config(command=self.toggle_ampm_switch)
        self.view.entry.bind("<KeyRelease>", self.auto_format_colon)
        self.view.entry.bind("<Return>", self.calculate_exit_metrics)
        self.view.entry.bind("<FocusOut>", self.calculate_exit_metrics)

    def handle_open_settings(self):
        self.view.show_config_overlay(
            save_command=self.commit_settings,
            cancel_command=self.handle_close_settings,
            strict_toggle_command=self.toggle_config_ui_states,
            sl_toggle_command=self.toggle_config_ui_states,
            theme_command=self.switch_theme
        )
        self.toggle_config_ui_states()

    def handle_close_settings(self):
        self.view.hide_config_overlay()
        self.view.entry.focus()

    def update_clock_loop(self):
        now = datetime.now()
        self.view.lbl_day_date.config(text=now.strftime("%a, %b %d"))
        self.view.lbl_clock.config(text=now.strftime("%I:%M:%S %p"))
        
        if self.model.settings.get("theme") == "System":
            refreshed_palette = self.model.get_active_palette()
            if refreshed_palette != self.view.p:
                self.view.update_theme(refreshed_palette)
                self.calculate_exit_metrics()
                
        self.view.root.after(1000, self.update_clock_loop)

    def toggle_config_ui_states(self):
        if not hasattr(self.view, 'overlay_frame') or not self.view.overlay_frame.winfo_exists(): return
        strict_state = tk.NORMAL if self.view.var_strict.get() else tk.DISABLED
        self.view.ent_start.config(state=strict_state)
        self.view.ent_end.config(state=strict_state)
        
        sl_state = tk.NORMAL if self.view.var_sl_enable.get() else tk.DISABLED
        self.view.ent_sl_hours.config(state=sl_state)
        self.view.ent_sl_pos.config(state=sl_state)

    def toggle_ampm_switch(self):
        if self.view.btn_ampm.cget("text") == "AM":
            self.view.btn_ampm.config(text="PM")
        else:
            self.view.btn_ampm.config(text="AM")
        self.refresh_ampm_button_color()
        self.calculate_exit_metrics()

    def refresh_ampm_button_color(self):
        p = self.view.p
        if self.view.btn_ampm.cget("text") == "AM":
            self.view.btn_ampm.config(bg=p["green"], fg=p["bg"])
        else:
            self.view.btn_ampm.config(bg=p["red"], fg=p["bg"])

    def auto_format_colon(self, event):
        if event.keysym in ("Backspace", "Delete", "Left", "Right", "Return", "Tab"): 
            # Re-evaluate calculations if editing existing entries
            self.calculate_exit_metrics()
            return
            
        val = self.view.entry.get().replace(":", "")
        if not val.isdigit(): return
        
        # Cleaned explicit indexing ensures colon formatting does not cycle loop strings
        if len(val) == 3:
            self.view.entry.delete(0, tk.END)
            self.view.entry.insert(0, f"{val[0]}:{val[1:]}")
        elif len(val) == 4:
            self.view.entry.delete(0, tk.END)
            self.view.entry.insert(0, f"{val[:2]}:{val[2:]}")
            
        self.calculate_exit_metrics()

    def switch_theme(self, target_theme):
        settings = self.model.settings
        settings["theme"] = target_theme
        self.model.save_settings(settings)
        p = self.model.get_active_palette()
        self.view.update_theme(p)
        self.refresh_ampm_button_color()

    def commit_settings(self):
        work_hours_raw = self.view.ent_hours.get()
        start_str = self.view.ent_start.get().strip()
        end_str = self.view.ent_end.get().strip()
        strict = self.view.var_strict.get()
        sl_enabled = self.view.var_sl_enable.get()
        sl_hours_raw = self.view.ent_sl_hours.get()
        sl_pos = self.view.ent_sl_pos.get()

        if strict:
            try:
                datetime.strptime(start_str, "%I:%M %p")
                datetime.strptime(end_str, "%I:%M %p")
            except ValueError:
                messagebox.showerror("Validation Error", "Ensure all fields match time string rules (e.g. '08:30 AM').")
                return

        new_settings = {
            "work_hours": work_hours_raw,
            "intime_start": start_str,
            "intime_end": end_str,
            "strict_mode": strict,
            "short_leave_enabled": sl_enabled,
            "short_leave_hours": sl_hours_raw,
            "short_leave_position": sl_pos,
            "theme": self.model.settings.get("theme", "System")
        }
        
        if self.model.save_settings(new_settings):
            messagebox.showinfo("Success", "Configuration metrics permanently saved!")
            self.view.settings = new_settings
            self.view.hide_config_overlay()
            self.calculate_exit_metrics()

    def calculate_exit_metrics(self, event=None):
        p = self.view.p
        raw_in = self.view.entry.get().strip()
        ampm = self.view.btn_ampm.cget("text")
        
        self.refresh_ampm_button_color()
        
        # Safe length checks block half-complete entry values
        if not raw_in or ":" not in raw_in or len(raw_in.replace(":", "")) < 3:
            self.view.lbl_result.config(text="---", fg=p["muted"])
            self.view.lbl_warn.config(text="")
            return
        
        try:
            parsed_in = datetime.strptime(f"{raw_in} {ampm}", "%I:%M %p")
        except ValueError:
            self.view.lbl_result.config(text="Format Err", fg=p["red"])
            self.view.lbl_warn.config(text="")
            return

        try:
            base_target_hours = float(self.model.settings.get("work_hours", "8.5"))
        except ValueError:
            base_target_hours = 8.5
            
        strict = self.model.settings.get("strict_mode", True)
        sl_enabled = self.model.settings.get("short_leave_enabled", False)
        
        try:
            sl_hours = float(self.model.settings.get("short_leave_hours", "2.0"))
        except ValueError:
            sl_hours = 2.0
            
        sl_pos = self.model.settings.get("short_leave_position", "End")

        try:
            policy_start = datetime.strptime(self.model.settings.get("intime_start", "08:30 AM"), "%I:%M %p")
            policy_end = datetime.strptime(self.model.settings.get("intime_end", "10:00 AM"), "%I:%M %p")
        except ValueError:
            self.view.lbl_warn.config(text="⚠️ Configuration time formatting issue!", fg=p["red"])
            return

        net_working_hours = base_target_hours - sl_hours if sl_enabled else base_target_hours
        calculated_exit = parsed_in + timedelta(hours=net_working_hours)
        exit_str = calculated_exit.strftime("%I:%M %p")

        absolute_exit_floor = policy_start + timedelta(hours=net_working_hours)
        latest_allowed_exit = policy_end + timedelta(hours=base_target_hours)

        deficit_warning = None
        if strict:
            if sl_enabled and sl_pos == "End":
                if parsed_in.time() > policy_end.time():
                    max_possible_presence = (latest_allowed_exit - parsed_in).total_seconds() / 3600.0
                    recognized_hours_logged = max_possible_presence - sl_hours
                    if recognized_hours_logged < net_working_hours:
                        gap_deficit = net_working_hours - recognized_hours_logged
                        deficit_warning = f"⚠️ Deficit Gap Alert!\nCutoff rules leave a {gap_deficit:.1f} hr gap."
            
            elif sl_enabled and sl_pos == "Start":
                extended_arrival_limit = policy_end + timedelta(hours=sl_hours)
                if parsed_in.time() > extended_arrival_limit.time():
                    available_time_window = (latest_allowed_exit - parsed_in).total_seconds() / 3600.0
                    if available_time_window < net_working_hours:
                        gap_deficit = net_working_hours - available_time_window
                        deficit_warning = f"⚠️ Deficit Gap Alert!\nExtended arrival limit breached.\nCutoff rules leave a {gap_deficit:.1f} hr gap."
            else:
                if parsed_in.time() > policy_end.time():
                    available_time_window = (latest_allowed_exit - parsed_in).total_seconds() / 3600.0
                    if available_time_window < base_target_hours:
                        gap_deficit = base_target_hours - available_time_window
                        deficit_warning = f"⚠️ Deficit Gap Alert!\nSystem leaves a {gap_deficit:.1f} hr shift gap."

        if strict:
            extended_limit = (policy_end + timedelta(hours=sl_hours)) if (sl_enabled and sl_pos == "Start") else policy_end
            text_color = p["red"] if (calculated_exit.time() > latest_allowed_exit.time() or parsed_in.time() > extended_limit.time()) else p["green"]
            self.view.lbl_result.config(text=f"Exit Time: {exit_str}", fg=text_color)
            
            is_early_floor_breach = calculated_exit.time() < absolute_exit_floor.time()
            is_late_ceiling_breach = calculated_exit.time() > latest_allowed_exit.time()

            if deficit_warning:
                self.view.lbl_warn.config(text=deficit_warning, fg=p["red"])
            elif is_early_floor_breach:
                self.view.lbl_warn.config(text=f"⚠️ Floor Breach Warning!\nExit time cannot drop below the policy minimum frame ({absolute_exit_floor.strftime('%I:%M %p')}).", fg=p["red"])
            elif is_late_ceiling_breach:
                self.view.lbl_warn.config(text=f"⚠️ Upper Limit Warning!\nLatest recognized office shift hour cutoff is {latest_allowed_exit.strftime('%I:%M %p')}.", fg=p["red"])
            else:
                self.view.lbl_warn.config(text="✅ Shift validation target compliant.", fg=p["green"])
        else:
            self.view.lbl_result.config(text=f"Exit Time: {exit_str}", fg=p["accent"])
            self.view.lbl_warn.config(text="ℹ️ Running in open flexible mode.", fg=p["muted"])
