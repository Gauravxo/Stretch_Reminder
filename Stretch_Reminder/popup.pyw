"""
STRETCH REMINDER - Acrylic Glass UI (Windows)
Optimized for 15-inch laptop - Everything fits in one screen
"""

import sys, json, random, datetime, ctypes
import tkinter as tk
from ctypes import wintypes

# ── Windows Acrylic Blur ─────────────────────────────────────
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

    ctypes.windll.user32.SetWindowCompositionAttribute(hwnd, ctypes.byref(data))


# ── Load config ──────────────────────────────────────────────
try:
    cfg = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
except:
    cfg = {}

SNOOZE_MIN  = cfg.get("snooze_minutes", 5)
DISPLAY     = cfg.get("display_mode", "fullscreen")
AUTO_DIS    = cfg.get("auto_dismiss_seconds", 0)
MESSAGES    = cfg.get("messages", ["its Time to Stretch Your Body"])
EXERCISES   = cfg.get("exercises", [
    "🧘 Neck rolls - 10 rotations each direction",
    "💪 Shoulder shrugs - 15 repetitions",
    "🙆 Overhead arm stretch - hold 30 seconds",
    "🤸 Standing side bend - 10 reps each side",
    "🦵 Quad stretch - 20 seconds each leg",
    "👐 Wrist circles - 10 rotations each direction",
    "🔄 Torso twists - 15 repetitions each side",
    "🚶 Walk in place - 1 minute"
])

QUOTES = [
    "💎 Your body is your temple. Keep it moving!",
    "✨ Every stretch is a step toward wellness",
    "🌟 Small breaks, big impact",
    "🎯 Health is wealth - invest 2 minutes now",
    "🔥 Keep the blood flowing, keep the energy growing",
    "🌈 Stretch your body, refresh your mind",
    "⚡ Motion is lotion for your joints",
    "🌺 Take care of your body, it's the only place you have to live",
    "💪 Strong body, strong mind",
    "🧘 Breathe deep, stretch far"
]

# ── Window ───────────────────────────────────────────────────
root = tk.Tk()
root.title("Stretch Reminder")
root.overrideredirect(False)
root.attributes("-topmost", True)

SW = root.winfo_screenwidth()
SH = root.winfo_screenheight()

if DISPLAY == "fullscreen":
    root.attributes("-fullscreen", True)
elif DISPLAY == "halfscreen":
    w = int(SW * 0.5)
    h = int(SH * 0.75)
    x = (SW - w) // 2
    y = (SH - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")
else:
    root.geometry(f"{int(SW*0.6)}x{int(SH*0.7)}")

root.configure(bg="#0a0e1a")
root.update()
hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
enable_blur(hwnd)

root.bind("<Alt-F4>", lambda e: "break")
root.bind("<Escape>", lambda e: "break")
root.protocol("WM_DELETE_WINDOW", lambda: None)

# ── Actions ──────────────────────────────────────────────────
def done():
    root.destroy()
    sys.exit(0)

def snooze():
    root.destroy()
    sys.exit(1)

# ── Content ──────────────────────────────────────────────────
msg = random.choice(MESSAGES)
quote = random.choice(QUOTES)
now = datetime.datetime.now().strftime("%I:%M %p")

# ── Main Container ───────────────────────────────────────────
container = tk.Frame(root, bg="#0a0e1a")
container.place(relx=0.5, rely=0.5, anchor="center")

# ── Time ─────────────────────────────────────────────────────
tk.Label(container,
         text="⏰  " + now,
         font=("Segoe UI", 14, "bold"),
         fg="#64b5f6",
         bg="#0a0e1a").pack(pady=(8,3))

# ── Message ──────────────────────────────────────────────────
tk.Label(container,
         text=msg,
         font=("Segoe UI", 32, "bold"),
         fg="#ffffff",
         bg="#0a0e1a",
         wraplength=750,
         justify="center").pack(pady=(3,3))

# ── Quote ────────────────────────────────────────────────────
tk.Label(container,
         text=quote,
         font=("Segoe UI", 22, "bold"),
         fg="#90a4ae",
         bg="#0a0e1a",
         wraplength=700).pack(pady=(9,20))

# ── Exercise Panel ───────────────────────────────────────────
panel_outer = tk.Frame(container, bg="#1e88e5", padx=1, pady=1)
panel_outer.pack(pady=3, padx=40)

panel = tk.Frame(panel_outer, bg="#1a2332")
panel.pack(ipadx=300, ipady=15)

# Header
tk.Label(panel,
         text="💪  STRETCH EXERCISES",
         font=("Segoe UI", 18, "bold"),
         fg="#64b5f6",
         bg="#1a2332").pack(anchor="w", pady=(0,12))

# Exercises - ALL shown in compact layout
exercises_container = tk.Frame(panel, bg="#1a2332")
exercises_container.pack(fill="x")

for idx, ex in enumerate(EXERCISES):
    # Alternating row colors for better readability
    bg_color = "#1e293b" if idx % 2 == 0 else "#162032"
    
    ex_frame = tk.Frame(exercises_container, bg=bg_color, padx=15, pady=8)
    ex_frame.pack(fill="x", pady=2)
    
    # Number badge
    badge = tk.Frame(ex_frame, bg="#1e88e5", width=28, height=28)
    badge.pack(side="left", padx=(0,12))
    badge.pack_propagate(False)
    
    tk.Label(badge,
             text=str(idx + 1),
             font=("Segoe UI", 18, "bold"),
             fg="#ffffff",
             bg="#1e88e5").place(relx=0.5, rely=0.5, anchor="center")
    
    # Exercise text
    tk.Label(ex_frame,
             text=ex,
             font=("Segoe UI", 18, "bold"),
             fg="#b3e5fc",  # Light cyan - beautiful on dark bg
             bg=bg_color,
             anchor="w",
             justify="left",
             wraplength=650).pack(side="left", fill="x", expand=True)

# ── Buttons ──────────────────────────────────────────────────
btn_frame = tk.Frame(container, bg="#0a0e1a")
btn_frame.pack(pady=18)

tk.Button(btn_frame,
          text="✓  DONE - I'M STRETCHED!",
          font=("Segoe UI", 13, "bold"),
          bg="#43a047",
          fg="white",
          relief="flat",
          padx=30,
          pady=10,
          borderwidth=0,
          cursor="hand2",
          activebackground="#66bb6a",
          activeforeground="white",
          command=done).grid(row=0, column=0, padx=10)

tk.Button(btn_frame,
          text=f"⏱  SNOOZE {SNOOZE_MIN} MIN",
          font=("Segoe UI", 12),
          bg="#1e88e5",
          fg="white",
          relief="flat",
          padx=25,
          pady=10,
          borderwidth=0,
          cursor="hand2",
          activebackground="#42a5f5",
          activeforeground="white",
          command=snooze).grid(row=0, column=1, padx=10)

# ── Auto-dismiss ─────────────────────────────────────────────
if AUTO_DIS > 0:
    timer = [AUTO_DIS]
    lbl = tk.Label(container, fg="#78909c", bg="#0a0e1a",
                   font=("Segoe UI", 9))
    lbl.pack(pady=(8,5))

    def tick():
        if timer[0] > 0:
            timer[0] -= 1
            lbl.config(text=f"Closing in {timer[0]}s")
            root.after(1000, tick)
        else:
            done()
    tick()

# ── Your Name ────────────────────────────────────────────────
tk.Label(container,
         text="Made with❤️BY kxo-Gauravxo-Github",
         font=("Segoe UI", 14, "italic"),
         fg="#64b5f6",
         bg="#0a0e1a").pack(pady=(12,5))

# ─────────────────────────────────────────────────────────────
root.mainloop()
sys.exit(0)