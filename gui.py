"""
gui.py - Modern Desktop Graphical User Interface for Swapi Water Tanker
Built with Python's standard Tkinter & ttk libraries.
Features live animated tank graphics, water flow visualization, preset buttons,
and non-blocking background dispensing.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import math
from tanker_core import WaterTanker, VALID_DENOMINATIONS


class WaterTankerGUI:
    def __init__(self, root: tk.Tk, tanker: WaterTanker = None):
        self.root = root
        self.root.title("Swapi Water Tanker - Smart Dispenser")
        self.root.geometry("640x720")
        self.root.minsize(580, 680)
        self.root.configure(bg="#f1f5f9")

        self.tanker = tanker if tanker is not None else WaterTanker()

        # State flags
        self.is_dispensing = False
        self.stop_requested = False
        self.anim_step = 0

        # Build UI
        self._setup_styles()
        self._build_header()
        self._build_tank_visualizer()
        self._build_controls()
        self._build_progress_section()
        self._build_status_log()

        # Initial render
        self.update_tank_display()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Custom ttk progressbar
        style.configure(
            "Water.Horizontal.TProgressbar",
            troughcolor="#e2e8f0",
            background="#0284c7",
            lightcolor="#38bdf8",
            darkcolor="#0369a1",
            thickness=18
        )

    def _build_header(self):
        header_frame = tk.Frame(self.root, bg="#0284c7", pady=14, padx=16)
        header_frame.pack(fill="x")

        title_lbl = tk.Label(
            header_frame,
            text="💧 Swapi Water Tanker",
            font=("Segoe UI", 18, "bold"),
            fg="#ffffff",
            bg="#0284c7"
        )
        title_lbl.pack()

        subtitle_lbl = tk.Label(
            header_frame,
            text="Automated Pure Water Dispensing Station",
            font=("Segoe UI", 10),
            fg="#e0f2fe",
            bg="#0284c7"
        )
        subtitle_lbl.pack()

    def _build_tank_visualizer(self):
        container = tk.Frame(self.root, bg="#ffffff", bd=1, relief="solid")
        container.pack(fill="x", padx=20, pady=(12, 6))

        # Canvas for animated tank & nozzle
        self.canvas = tk.Canvas(container, height=180, bg="#ffffff", highlightthickness=0)
        self.canvas.pack(fill="x", padx=10, pady=8)

        # Draw static elements on canvas
        self.canvas.bind("<Configure>", lambda e: self.update_tank_display())

    def update_tank_display(self):
        """Draws the tank level, pipes, and active water droplets."""
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        if width <= 1:
            width = 600

        # Tank Dimensions
        tank_x1 = 50
        tank_y1 = 20
        tank_x2 = 220
        tank_y2 = 160

        # Tank outline
        self.canvas.create_rectangle(
            tank_x1, tank_y1, tank_x2, tank_y2,
            outline="#475569", width=3, fill="#f8fafc"
        )

        # Water Level fill inside tank
        water_ratio = max(0.0, min(1.0, self.tanker.current_water / self.tanker.capacity))
        water_height = (tank_y2 - tank_y1 - 6) * water_ratio
        water_top_y = (tank_y2 - 3) - water_height

        if water_ratio > 0:
            self.canvas.create_rectangle(
                tank_x1 + 3, water_top_y, tank_x2 - 3, tank_y2 - 3,
                outline="", fill="#38bdf8"
            )
            # Animated wave surface
            if self.is_dispensing:
                wave_offset = math.sin(self.anim_step * 0.5) * 3
                self.canvas.create_line(
                    tank_x1 + 3, water_top_y + wave_offset,
                    tank_x2 - 3, water_top_y - wave_offset,
                    fill="#0284c7", width=2
                )

        # Tank capacity label
        self.canvas.create_text(
            (tank_x1 + tank_x2) / 2, tank_y2 - 20,
            text=f"{self.tanker.current_water} / {self.tanker.capacity} L",
            font=("Segoe UI", 11, "bold"),
            fill="#0f172a"
        )
        self.canvas.create_text(
            (tank_x1 + tank_x2) / 2, tank_y1 + 18,
            text="STORAGE TANK",
            font=("Segoe UI", 8, "bold"),
            fill="#64748b"
        )

        # Dispensing Pipe & Tap
        pipe_y = tank_y2 - 35
        self.canvas.create_line(tank_x2, pipe_y, 340, pipe_y, fill="#64748b", width=10)
        self.canvas.create_line(340, pipe_y - 5, 340, pipe_y + 25, fill="#64748b", width=12)

        # Nozzle
        self.canvas.create_polygon(
            332, pipe_y + 25, 348, pipe_y + 25, 344, pipe_y + 35, 336, pipe_y + 35,
            fill="#334155"
        )

        # Dispenser Station / Container
        bucket_x = 340
        bucket_y = tank_y2 - 5
        self.canvas.create_polygon(
            bucket_x - 22, bucket_y + 15,
            bucket_x + 22, bucket_y + 15,
            bucket_x + 16, bucket_y - 25,
            bucket_x - 16, bucket_y - 25,
            fill="#e2e8f0", outline="#94a3b8", width=2
        )

        # If dispensing, draw animated water flow
        if self.is_dispensing:
            flow_y1 = pipe_y + 35
            flow_y2 = bucket_y + 5
            # Animated stream
            self.canvas.create_line(
                340, flow_y1, 340, flow_y2,
                fill="#0284c7", width=5, dash=(6, 4)
            )
            # Water splash ripples in bucket
            ripple_w = 10 + (self.anim_step % 6) * 2
            self.canvas.create_oval(
                340 - ripple_w, bucket_y - 2, 340 + ripple_w, bucket_y + 4,
                outline="#38bdf8", width=2
            )

        # Info Box on right side of visualizer
        info_x = 420
        self.canvas.create_text(
            info_x, 40,
            text=f"Total Dispensed: {self.tanker.total_dispensed} L",
            font=("Segoe UI", 10, "bold"), anchor="w", fill="#0369a1"
        )
        status_text = "READY TO DISPENSE" if not self.is_dispensing else "DISPENSING IN PROGRESS..."
        status_color = "#059669" if not self.is_dispensing else "#d97706"
        self.canvas.create_text(
            info_x, 70,
            text=f"Status: {status_text}",
            font=("Segoe UI", 9, "bold"), anchor="w", fill=status_color
        )
        self.canvas.create_text(
            info_x, 100,
            text=f"Price: ₹1 per Litre",
            font=("Segoe UI", 9), anchor="w", fill="#475569"
        )

    def _build_controls(self):
        ctrl_card = tk.LabelFrame(
            self.root, text=" 🪙 Select Coin Amount (Litres) ",
            font=("Segoe UI", 10, "bold"), bg="#ffffff", padx=14, pady=10
        )
        ctrl_card.pack(fill="x", padx=20, pady=6)

        # Preset denomination buttons
        presets_frame = tk.Frame(ctrl_card, bg="#ffffff")
        presets_frame.pack(fill="x", pady=4)

        self.amount_var = tk.StringVar(value="5")

        for denom in VALID_DENOMINATIONS:
            btn = tk.Button(
                presets_frame,
                text=f"₹{denom}\n({denom}L)",
                font=("Segoe UI", 9, "bold"),
                bg="#f0f9ff",
                fg="#0369a1",
                activebackground="#bae6fd",
                activeforeground="#0369a1",
                relief="groove",
                bd=1,
                padx=8,
                pady=4,
                cursor="hand2",
                command=lambda d=denom: self.select_preset(d)
            )
            btn.pack(side="left", expand=True, fill="x", padx=3)

        # Custom input row
        custom_frame = tk.Frame(ctrl_card, bg="#ffffff")
        custom_frame.pack(fill="x", pady=(8, 2))

        custom_lbl = tk.Label(
            custom_frame, text="Or Custom Litres:",
            font=("Segoe UI", 9), bg="#ffffff", fg="#334155"
        )
        custom_lbl.pack(side="left", padx=(0, 8))

        self.custom_entry = tk.Entry(
            custom_frame, textvariable=self.amount_var,
            font=("Segoe UI", 10, "bold"), width=10, justify="center"
        )
        self.custom_entry.pack(side="left", padx=4)

        refill_btn = tk.Button(
            custom_frame, text="Refill Tank",
            font=("Segoe UI", 9), bg="#e2e8f0", fg="#334155",
            relief="groove", bd=1, cursor="hand2", command=self.on_refill
        )
        refill_btn.pack(side="right", padx=4)

    def _build_progress_section(self):
        progress_card = tk.Frame(self.root, bg="#ffffff", padx=14, pady=10, bd=1, relief="solid")
        progress_card.pack(fill="x", padx=20, pady=6)

        # Action Buttons
        btn_frame = tk.Frame(progress_card, bg="#ffffff")
        btn_frame.pack(fill="x", pady=(0, 8))

        self.dispense_btn = tk.Button(
            btn_frame,
            text="▶ START DISPENSING",
            font=("Segoe UI", 11, "bold"),
            bg="#0284c7",
            fg="#ffffff",
            activebackground="#0369a1",
            activeforeground="#ffffff",
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2",
            command=self.start_dispense_thread
        )
        self.dispense_btn.pack(side="left", expand=True, fill="x", padx=(0, 6))

        self.stop_btn = tk.Button(
            btn_frame,
            text="⏹ STOP",
            font=("Segoe UI", 11, "bold"),
            bg="#ef4444",
            fg="#ffffff",
            activebackground="#dc2626",
            activeforeground="#ffffff",
            relief="flat",
            padx=16,
            pady=8,
            state="disabled",
            cursor="hand2",
            command=self.request_stop
        )
        self.stop_btn.pack(side="right", padx=(6, 0))

        # Progress bar
        self.progress_bar = ttk.Progressbar(
            progress_card,
            style="Water.Horizontal.TProgressbar",
            orient="horizontal",
            mode="determinate"
        )
        self.progress_bar.pack(fill="x", pady=6)

        self.status_lbl = tk.Label(
            progress_card,
            text="Ready. Select amount and press Start Dispensing.",
            font=("Segoe UI", 9, "bold"),
            bg="#ffffff",
            fg="#64748b"
        )
        self.status_lbl.pack()

    def _build_status_log(self):
        log_card = tk.LabelFrame(
            self.root, text=" Transaction History & Logs ",
            font=("Segoe UI", 9, "bold"), bg="#ffffff", padx=10, pady=6
        )
        log_card.pack(fill="both", expand=True, padx=20, pady=(6, 12))

        self.log_text = tk.Text(
            log_card, height=6, font=("Consolas", 9),
            bg="#f8fafc", fg="#334155", state="disabled", wrap="word"
        )
        self.log_text.pack(fill="both", expand=True)

        self._log_message("System initialized. Swapi Water Tanker Ready.")

    def select_preset(self, amount: int):
        self.amount_var.set(str(amount))
        self.custom_entry.focus()

    def _log_message(self, message: str):
        self.log_text.config(state="normal")
        timestamp = time.strftime("[%H:%M:%S] ")
        self.log_text.insert("end", timestamp + message + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def on_refill(self):
        if self.is_dispensing:
            messagebox.showwarning("Busy", "Cannot refill while dispensing.")
            return

        added = self.tanker.refill()
        self.update_tank_display()
        self._log_message(f"Tank refilled with {added} Litres. Current level: {self.tanker.capacity}L.")
        messagebox.showinfo("Tanker Refilled", f"Tank refilled to 100% capacity ({self.tanker.capacity} Litres).")

    def request_stop(self):
        if self.is_dispensing:
            self.stop_requested = True
            self.status_lbl.config(text="Stopping dispensing...", fg="#dc2626")

    def start_dispense_thread(self):
        if self.is_dispensing:
            return

        raw_input = self.amount_var.get()
        # Allow custom numbers in GUI as an enhancement, but validate
        is_valid, amount, err_msg = self.tanker.validate_amount(raw_input, allow_custom=True)
        if not is_valid:
            messagebox.showerror("Invalid Input", err_msg)
            return

        self.is_dispensing = True
        self.stop_requested = False
        self.dispense_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = amount

        self._log_message(f"Starting dispense order: {amount} Litres (₹{amount}).")

        # Launch background worker
        worker = threading.Thread(target=self._dispense_worker, args=(amount,), daemon=True)
        worker.start()

        # Start animation ticker
        self._animate_water()

    def _animate_water(self):
        if self.is_dispensing:
            self.anim_step += 1
            self.update_tank_display()
            self.root.after(80, self._animate_water)

    def _dispense_worker(self, amount: int):
        try:
            dispensed_count = 0
            # Realistic dispense delay for GUI (0.2 seconds per litre)
            step_delay = 0.2

            for current_litre, total_litres, percent in self.tanker.dispense_stream(amount, step_delay=step_delay):
                if self.stop_requested:
                    self._log_message(f"Dispensing stopped prematurely after {dispensed_count} Litres.")
                    break

                dispensed_count = current_litre
                self.root.after(0, self._update_progress_ui, current_litre, total_litres, percent)

            # Finished
            self.root.after(0, self._on_dispense_complete, dispensed_count, amount)

        except Exception as e:
            self.root.after(0, self._on_dispense_error, str(e))

    def _update_progress_ui(self, current: int, total: int, percent: float):
        self.progress_bar["value"] = current
        self.status_lbl.config(
            text=f"Dispensing: {current} / {total} Litres ({percent:.0f}%)",
            fg="#0284c7"
        )
        self.update_tank_display()

    def _on_dispense_complete(self, dispensed: int, requested: int):
        self.is_dispensing = False
        self.stop_requested = False
        self.dispense_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.update_tank_display()

        if dispensed == requested:
            self.status_lbl.config(
                text=f"✔ Complete! Dispensed {dispensed} Litres. Thank you!",
                fg="#059669"
            )
            self._log_message(f"Transaction completed successfully: {dispensed} Litres dispensed.")
            messagebox.showinfo(
                "Dispense Complete",
                f"Successfully dispensed {dispensed} Litres!\nTotal Amount: ₹{dispensed}\nTank Remaining: {self.tanker.current_water}L\n\nThanks for visiting Swapi Water Tanker!"
            )
        else:
            self.status_lbl.config(
                text=f"Dispense stopped. Total dispensed: {dispensed} Litres.",
                fg="#dc2626"
            )

    def _on_dispense_error(self, err: str):
        self.is_dispensing = False
        self.dispense_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.update_tank_display()
        self.status_lbl.config(text=f"Error: {err}", fg="#dc2626")
        self._log_message(f"Error encountered: {err}")
        messagebox.showerror("Dispensing Error", err)


def launch_gui(tanker: WaterTanker = None):
    """Launches the Tkinter GUI application."""
    root = tk.Tk()
    app = WaterTankerGUI(root, tanker=tanker)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
