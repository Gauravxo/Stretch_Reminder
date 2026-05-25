"""
STRETCH REMINDER - Acrylic Glass UI (Windows)
Optimized Compact Layout
"""

import sys
import json
import random
import datetime
import ctypes
import os
import tkinter as tk
from tkinter import ttk


def enable_blur(hwnd):

    class ACCENTPOLICY(ctypes.Structure):
        _fields_ = [
            ("AccentState", ctypes.c_int),
            ("AccentFlags", ctypes.c_int),
            ("GradientColor", ctypes.c_int),
            ("AnimationId", ctypes.c_int),
        ]

    class WINCOMPATTRDATA(ctypes.Structure):
        _fields_ = [
            ("Attribute", ctypes.c_int),
            ("Data", ctypes.POINTER(ACCENTPOLICY)),
            ("SizeOfData", ctypes.c_size_t),
        ]

    accent = ACCENTPOLICY()
    accent.AccentState = 4
    accent.GradientColor = 0xCC111111

    data = WINCOMPATTRDATA()
    data.Attribute = 19
    data.Data = ctypes.pointer(accent)
    data.SizeOfData = ctypes.sizeof(accent)

    ctypes.windll.user32.SetWindowCompositionAttribute(
        hwnd,
        ctypes.byref(data)
    )



RESOLUTION_DAYS = 60
TRACK_FILE = "resolution_tracker.json"


def load_resolution():

    today = datetime.date.today()

    if not os.path.exists(TRACK_FILE):

        data = {
            "start_date": str(today),
            "completed_days": 0,
            "last_opened": str(today)
        }

        with open(TRACK_FILE, "w") as f:
            json.dump(data, f)

        return data

    with open(TRACK_FILE, "r") as f:
        data = json.load(f)

    last_opened = datetime.date.fromisoformat(
        data["last_opened"]
    )

    days_passed = (today - last_opened).days

    if days_passed > 0:

        data["completed_days"] += days_passed

        data["last_opened"] = str(today)

        with open(TRACK_FILE, "w") as f:
            json.dump(data, f)

    return data


resolution_data = load_resolution()

completed_days = min(
    resolution_data["completed_days"],
    RESOLUTION_DAYS
)

remaining_days = max(
    RESOLUTION_DAYS - completed_days,
    0
)


SNOOZE_MIN = 5

MESSAGES = [
    "🧘 It's Time to Stretch Your Body"
]

QUOTES = [
"💎 Your body is your greatest investment — move it daily!",
"✨ Every stretch brings you closer to a healthier you",
"🔥 Consistency beats intensity every time",
"🌈 Healthy body, clear mind, happier life",
"💪 Motion is medicine — keep going!",
"🌞 Take care of your body — it carries your dreams",
"🚴 Every move counts, no matter how small",
"💖 Self-care begins with self-movement",
"🏆 Progress, not perfection"
]

EXERCISES = [
"💪 Shoulder shrugs - 15 repetitions", 
"🙆 Overhead arm stretch - hold 30 seconds", 
"🤸 Standing side bend - 10 reps each side", 
"🦵 Quad stretch - 20 seconds each leg", 
"👐 Wrist circles - 10 rotations each direction",
"🔄 Torso twists - 15 repetitions each side",
"🚶 Walk in place - 1 minute"
]
root = tk.Tk()
root.title("Stretch Reminder")
# Get screen size
SW = root.winfo_screenwidth()
SH = root.winfo_screenheight()
win_width = int(SW * 0.85)
win_height = int(SH * 0.85)

# Center the window
x_pos = (SW - win_width) // 2
y_pos = (SH - win_height) // 2

root.geometry(f"{win_width}x{win_height}+{x_pos}+{y_pos}")
root.configure(bg="#0a0e1a")
root.attributes("-topmost", True)  

# Optional: make window resizable (users can adjust size)
root.resizable(True, True)

root.update()
hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
#enable_blur(hwnd)  


def done():
    root.destroy()
    sys.exit(0)


def snooze():
    root.destroy()
    sys.exit(1)


container = tk.Frame(
    root,
    bg="#0a0e1a"
)

container.pack(
    expand=True,
    fill="both",
    padx=25,
    pady=15
)

msg = random.choice(MESSAGES)
quote = random.choice(QUOTES)

tk.Label(
    container,
    text=msg,
    font=("Segoe UI", 22, "bold"),
    fg="white",
    bg="#0a0e1a"
).pack(pady=(0, 5))

tk.Label(
    container,
    text=quote,
    font=("Segoe UI", 12, "italic"),
    fg="#90a4ae",
    bg="#0a0e1a"
).pack(pady=(0, 15))


top_section = tk.Frame(
    container,
    bg="#0a0e1a"
)

top_section.pack(fill="x", pady=(0, 12))



timer_outer = tk.Frame(
    top_section,
    bg="#1e88e5",
    padx=1,
    pady=1
)

timer_outer.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 6)
)

timer_box = tk.Frame(
    timer_outer,
    bg="#111827",
    padx=15,
    pady=12
)

timer_box.pack(fill="both", expand=True)



remaining = [5 * 60]

count_lbl = tk.Label(
    timer_box,
    text="05:00",
    font=("Segoe UI", 62, "bold"),
    fg="white",
    bg="#111827"
)

count_lbl.pack(anchor="center", pady=5)


def update_countdown():

    mins, secs = divmod(remaining[0], 60)

    count_lbl.config(
        text=f"{mins:02d}:{secs:02d}"
    )

    if remaining[0] > 0:

        remaining[0] -= 1

        root.after(
            1000,
            update_countdown
        )

    else:
        done()


update_countdown()



progress_outer = tk.Frame(
    top_section,
    bg="#43a047",
    padx=1,
    pady=1
)

progress_outer.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(6, 0)
)

progress_panel = tk.Frame(
    progress_outer,
    bg="#102027",
    padx=15,
    pady=12
)

progress_panel.pack(fill="both", expand=True)

tk.Label(
    progress_panel,
    text="🎯 60 DAY RESOLUTION",
    font=("Segoe UI", 12, "bold"),
    fg="#81c784",
    bg="#102027"
).pack(anchor="w")

tk.Label(
    progress_panel,
    text=f"✅ Completed: {completed_days} Days",
    font=("Segoe UI", 12, "bold"),
    fg="white",
    bg="#102027"
).pack(anchor="w", pady=(8, 2))

tk.Label(
    progress_panel,
    text=f"⏳ Remaining: {remaining_days} Days",
    font=("Segoe UI", 12, "bold"),
    fg="#fef600",
    bg="#102027"
).pack(anchor="w")


progress_percent = (
    completed_days / RESOLUTION_DAYS
) * 100

bar = ttk.Progressbar(
    progress_panel,
    length=220,
    mode="determinate"
)

bar["value"] = progress_percent

bar.pack(fill="x", pady=(10, 2))

# ── Exercise Panel ───────────────────────────────────────────
panel_outer = tk.Frame(
    container,
    bg="#1e88e5",
    padx=1,
    pady=1
)

panel_outer.pack(fill="both", expand=True)

panel = tk.Frame(
    panel_outer,
    bg="#1a2332"
)

panel.pack(fill="both", expand=True)

# Header
tk.Label(
    panel,
    text="💪 STRETCH EXERCISES                                             💧 DON'T FORGET TO DRINK WATER",
    font=("Segoe UI", 12, "bold"),
    fg="#64b5f6",
    bg="#1a2332"
).pack(anchor="w", padx=15, pady=(12, 10))

# Exercise Rows
for idx, ex in enumerate(EXERCISES):

    bg_color = "#1e293b" if idx % 2 == 0 else "#162032"

    row = tk.Frame(
        panel,
        bg=bg_color,
        padx=10,
        pady=8
    )

    row.pack(
        fill="x",
        padx=2,
        pady=1
    )

    badge = tk.Frame(
        row,
        bg="#0411c5",
        width=16,
        height=16
    )

    badge.pack(side="left", padx=(0, 5))
    badge.pack_propagate(False)

    tk.Label(
        badge,
        text=str(idx + 1),
        font=("Segoe UI", 10, "bold"),
        fg="white",
        bg="#1e88e5"
    ).place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    tk.Label(
        row,
        text=ex,
        font=("Segoe UI", 14, "bold"),
        fg="#ffffff",
        bg=bg_color,
        anchor="w"
    ).pack(side="left")

# ── Buttons ──────────────────────────────────────────────────
btn_frame = tk.Frame(
    container,
    bg="#0a0e1a"
)

btn_frame.pack(pady=1)

tk.Button(
    btn_frame,
    text="✓ DONE - I'M STRETCHED!",
    font=("Segoe UI", 12, "bold"),
    bg="#43a047",
    fg="white",
    relief="flat",
    padx=22,
    pady=10,
    borderwidth=0,
    cursor="hand2",
    activebackground="#66bb6a",
    command=done
).grid(row=0, column=1, padx=100)

tk.Button(
    btn_frame,
    text=f"⏱ SNOOZE {SNOOZE_MIN} MIN",
    font=("Segoe UI", 11),
    bg="#1e88e5",
    fg="white",
    relief="flat",
    padx=20,
    pady=10,
    borderwidth=0,
    cursor="hand2",
    activebackground="#42a5f5",
    command=snooze
).grid(row=0, column=10, padx=200)

# ── Footer ───────────────────────────────────────────────────
tk.Label(
    container,
    text="Made with ❤️BY kxo",
    font=("Segoe UI", 11, "bold"),
    fg="#64b5f6",
    bg="#0a0e1a"
).pack(pady=(5, 0))

# ── Run ──────────────────────────────────────────────────────
root.mainloop()
sys.exit(0)