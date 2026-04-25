"""
STRETCH REMINDER - Main Process
Runs silently in tray. Spawns popup.pyw as a child process when timer fires.
Using subprocess is 100% reliable - no threading/tkinter race conditions.
"""

import sys, os, time, json, threading, datetime, subprocess, queue, logging
from pathlib import Path

try:
    import pystray
    from PIL import Image, ImageDraw
    TRAY_OK = True
except ImportError:
    TRAY_OK = False

import tkinter as tk
from tkinter import messagebox

# ── Paths ─────────────────────────────────────────────────────
BASE    = Path(os.path.dirname(os.path.abspath(__file__)))
CFG_F   = BASE / "config.json"
LOG_F   = BASE / "stretch_log.txt"
POPUP_F = BASE / "popup.pyw"

logging.basicConfig(
    filename=str(LOG_F),
    level=logging.DEBUG,
    format="%(asctime)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger()

# ── Default config ─────────────────────────────────────────────
DEFAULT = {
    "interval_minutes": 40,
    "snooze_minutes": 5,
    "display_mode": "fullscreen",
    "auto_dismiss_seconds": 0,
    "work_hours": {
        "enabled": False,          # OFF by default — fires any time
        "start": "09:00",
        "end":   "18:30",
        "days":  [0,1,2,3,4]
    },
    "exclude_ranges": [
        {"start": "13:45", "end": "14:30", "label": "Lunch Walk"}
    ],
    "messages": [
        "Time to Stand Up and Stretch!",
        "Get Up and Move Your Body!",
        "Stand Up - Walk Around a Bit!",
        "Stretch Break! Your body will thank you.",
        "Rise and Stretch!",
        "Break Time! Loosen those muscles.",
        "Your chair misses you - get up!"
    ]
}

# ─────────────────────────────────────────────────────────────
class Config:
    def __init__(self):
        self.data = self._load()

    def _load(self):
        if CFG_F.exists():
            try:
                raw = json.loads(CFG_F.read_text())
                return self._merge(DEFAULT, raw)
            except Exception as e:
                log.error(f"Config load error: {e}")
        return json.loads(json.dumps(DEFAULT))

    def _merge(self, base, over):
        out = json.loads(json.dumps(base))
        for k, v in over.items():
            if k in out and isinstance(out[k], dict) and isinstance(v, dict):
                out[k] = self._merge(out[k], v)
            else:
                out[k] = v
        return out

    def save(self):
        CFG_F.write_text(json.dumps(self.data, indent=2))
        log.info("Config saved")

    def __getitem__(self, k):     return self.data[k]
    def __setitem__(self, k, v):  self.data[k] = v
    def get(self, k, d=None):     return self.data.get(k, d)


# ─────────────────────────────────────────────────────────────
class Timer:
    def __init__(self, cfg: Config, fire_cb):
        self.cfg      = cfg
        self.fire_cb  = fire_cb
        self._lock    = threading.Lock()
        self._next    = time.monotonic() + cfg["interval_minutes"] * 60
        log.info(f"Timer started - interval={cfg['interval_minutes']} min")

    def start(self):
        threading.Thread(target=self._run, daemon=True).start()

    def reset(self, minutes=None):
        m = minutes if minutes is not None else self.cfg["interval_minutes"]
        with self._lock:
            self._next = time.monotonic() + m * 60
        log.info(f"Timer reset to {m} min")

    def get_remaining(self):
        with self._lock:
            secs = max(0.0, self._next - time.monotonic())
        return divmod(int(secs), 60)

    def _run(self):
        while True:
            time.sleep(1)
            with self._lock:
                due = time.monotonic() >= self._next
            if due:
                log.info("Timer fired - checking schedule...")
                self.reset()                        # reset first
                if self._ok_to_fire():
                    log.info("Schedule OK - calling fire_cb")
                    self.fire_cb()
                else:
                    log.info("Skipped (outside work hours or excluded range)")

    def _ok_to_fire(self):
        now = datetime.datetime.now()
        wh  = self.cfg["work_hours"]
        if wh["enabled"]:
            if now.weekday() not in wh["days"]:
                log.debug(f"Skipped: weekday {now.weekday()} not in {wh['days']}")
                return False
            ts = self._t(wh["start"])
            te = self._t(wh["end"])
            if not (ts <= now.time() <= te):
                log.debug(f"Skipped: time {now.time()} outside {ts}-{te}")
                return False
        for ex in self.cfg["exclude_ranges"]:
            ts = self._t(ex["start"])
            te = self._t(ex["end"])
            if ts <= now.time() <= te:
                log.debug(f"Skipped: in exclude range {ex['label']}")
                return False
        return True

    @staticmethod
    def _t(s):
        h, m = map(int, s.split(":"))
        return datetime.time(h, m)


# ─────────────────────────────────────────────────────────────
class App:
    def __init__(self):
        self.cfg    = Config()
        self._q     = queue.Queue()
        self._timer = Timer(self.cfg, lambda: self._q.put("SHOW"))
        self._popup = None      # currently running Popen for popup
        self._tray  = None

        # Hidden root - must NOT be withdrawn (breaks Toplevel on Windows)
        self.root = tk.Tk()
        self.root.geometry("1x1+-32000+-32000")
        self.root.overrideredirect(True)
        self.root.attributes("-alpha", 0.0)

        self._timer.start()
        if TRAY_OK:
            self._setup_tray()
        self._poll()            # start the main-thread event loop

    # ── Poll queue every 1 second ─────────────────────────────
    def _poll(self):
        # Process all queued events
        try:
            while True:
                msg = self._q.get_nowait()
                log.info(f"Queue message: {msg}")
                if msg == "SHOW":
                    self._show_popup()
                elif msg == "QUIT":
                    self.root.destroy()
                    return
                elif msg == "SETTINGS":
                    self._open_settings()
        except queue.Empty:
            pass

        # Update tray countdown
        m, s = self._timer.get_remaining()
        tip = f"Stretch Reminder  |  Next in {m:02d}:{s:02d}"
        if self._tray:
            try:
                self._tray.title = tip
            except Exception:
                pass

        self.root.after(1000, self._poll)

    # ── Show popup as a SEPARATE PROCESS (100% reliable) ──────
    def _show_popup(self):
        # Kill old popup if still open
        if self._popup and self._popup.poll() is None:
            log.info("Popup already open, bringing to front")
            return

        log.info("Launching popup process...")
        try:
            # Pass config as JSON arg so popup knows snooze_minutes etc.
            cfg_json = json.dumps(self.cfg.data)
            self._popup = subprocess.Popen(
                [sys.executable, str(POPUP_F), cfg_json],
                creationflags=subprocess.CREATE_NO_WINDOW
                if sys.platform == "win32" else 0
            )
            # Watch for result in background thread
            threading.Thread(target=self._watch_popup, daemon=True).start()
        except Exception as e:
            log.error(f"Failed to launch popup: {e}")

    def _watch_popup(self):
        """Wait for popup to close, read exit code for snooze/done."""
        code = self._popup.wait()
        log.info(f"Popup closed with code {code}")
        if code == 1:
            # Snooze
            m = self.cfg["snooze_minutes"]
            self._timer.reset(m)
            log.info(f"Snoozed for {m} min")
        else:
            # Done (code 0) or force-closed
            self._timer.reset()
            log.info("Done - timer reset to full interval")

    # ── Tray ──────────────────────────────────────────────────
    def _setup_tray(self):
        def on_now(icon, item):       self._q.put("SHOW")
        def on_settings(icon, item):  self._q.put("SETTINGS")
        def on_log(icon, item):
            if LOG_F.exists():
                os.startfile(str(LOG_F))
        def on_quit(icon, item):
            icon.stop()
            self._q.put("QUIT")

        menu = pystray.Menu(
            pystray.MenuItem("Stretch Reminder", None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Stretch NOW",  on_now),
            pystray.MenuItem("Settings",     on_settings),
            pystray.MenuItem("View Log",     on_log),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit",         on_quit),
        )
        img = Image.new("RGBA", (64,64), (0,0,0,0))
        d   = ImageDraw.Draw(img)
        d.ellipse([2,2,62,62], fill="#1f6feb")
        d.ellipse([24,10,40,26], fill="white")
        d.line([(32,26),(32,44)], fill="white", width=3)
        d.line([(32,34),(18,46)], fill="white", width=3)
        d.line([(32,34),(46,46)], fill="white", width=3)
        d.line([(32,44),(22,58)], fill="white", width=3)
        d.line([(32,44),(42,58)], fill="white", width=3)

        self._tray = pystray.Icon("stretch", img, "Stretch Reminder", menu)
        threading.Thread(target=self._tray.run, daemon=True).start()
        log.info("Tray started")

    # ── Settings ──────────────────────────────────────────────
    def _open_settings(self):
        win = tk.Toplevel(self.root)
        win.title("Stretch Reminder - Settings")
        win.geometry("580x620")
        win.configure(bg="#0d1117")
        win.resizable(False, False)
        win.attributes("-topmost", True)
        win.lift()
        win.focus_force()
        _build_settings(win, self.cfg, lambda: self._timer.reset())

    def run(self):
        log.info("Mainloop starting")
        self.root.mainloop()
        log.info("Mainloop ended")


# ─────────────────────────────────────────────────────────────
# Settings UI builder (shared by main app)
# ─────────────────────────────────────────────────────────────
def _build_settings(win, cfg: Config, on_save_cb):
    BG="#0d1117"; SF="#161b22"; AC="#58a6ff"
    TX="#e6edf3"; SB="#8b949e"; IP="#21262d"

    hdr = tk.Frame(win, bg=SF, pady=12)
    hdr.pack(fill="x")
    tk.Label(hdr, text="Settings-Gauravxo-Github", font=("Segoe UI",18,"bold"), bg=SF, fg=AC).pack()
    tk.Label(hdr, text="Click Save to apply changes", font=("Segoe UI",10), bg=SF, fg=SB).pack()

    body = tk.Frame(win, bg=BG)
    body.pack(fill="both", expand=True, padx=22, pady=10)

    def sec(txt):
        tk.Label(body, text=txt.upper(), font=("Segoe UI",9,"bold"),
                 bg=BG, fg=AC).pack(anchor="w", pady=(10,2))
        tk.Frame(body, bg=AC, height=1).pack(fill="x")

    def spin_row(lbl, var, lo, hi):
        f = tk.Frame(body, bg=SF, pady=4, padx=10); f.pack(fill="x", pady=2)
        tk.Label(f, text=lbl, font=("Segoe UI",11), bg=SF, fg=TX,
                 width=30, anchor="w").pack(side="left")
        tk.Spinbox(f, from_=lo, to=hi, textvariable=var, width=6,
                   font=("Consolas",12), bg=IP, fg=TX,
                   buttonbackground="#30363d").pack(side="right", padx=4)

    def entry_row(lbl, var, w=9):
        f = tk.Frame(body, bg=SF, pady=4, padx=10); f.pack(fill="x", pady=2)
        tk.Label(f, text=lbl, font=("Segoe UI",11), bg=SF, fg=TX,
                 width=30, anchor="w").pack(side="left")
        tk.Entry(f, textvariable=var, width=w,
                 font=("Consolas",12), bg=IP, fg=TX).pack(side="right", padx=4)

    def check_row(lbl, var):
        f = tk.Frame(body, bg=SF, pady=4, padx=10); f.pack(fill="x", pady=2)
        tk.Label(f, text=lbl, font=("Segoe UI",11), bg=SF, fg=TX,
                 width=30, anchor="w").pack(side="left")
        tk.Checkbutton(f, variable=var, bg=SF, fg=TX, selectcolor=IP,
                       activebackground=SF).pack(side="right")

    sec("Timing")
    iv = tk.IntVar(value=cfg["interval_minutes"])
    sv = tk.IntVar(value=cfg["snooze_minutes"])
    av = tk.IntVar(value=cfg["auto_dismiss_seconds"])
    spin_row("Reminder every X minutes",     iv, 1, 180)
    spin_row("Snooze duration (minutes)",    sv, 1,  30)
    spin_row("Auto-dismiss (0 = off)",       av, 0, 300)

    sec("Display")
    mv = tk.StringVar(value=cfg["display_mode"])
    fm = tk.Frame(body, bg=SF, pady=4, padx=10); fm.pack(fill="x", pady=2)
    for val, lbl in [("fullscreen","Full Screen"), ("halfscreen","Half Screen")]:
        tk.Radiobutton(fm, text=lbl, variable=mv, value=val,
                       bg=SF, fg=TX, selectcolor=IP, font=("Segoe UI",11),
                       activebackground=SF).pack(side="left", padx=14)

    sec("Work Hours  (uncheck = remind 24/7)")
    wh = cfg["work_hours"]
    wv = tk.BooleanVar(value=wh["enabled"])
    ws = tk.StringVar(value=wh["start"])
    we = tk.StringVar(value=wh["end"])
    check_row("Only fire during work hours", wv)
    entry_row("Work start (HH:MM)",          ws)
    entry_row("Work end   (HH:MM)",          we)

    sec("Exclude Ranges  (e.g. lunch walk)")
    exc_rows = []
    ef = tk.Frame(body, bg=BG); ef.pack(fill="x")

    def add_exc(s="", e="", lbl=""):
        f = tk.Frame(ef, bg=SF, pady=3, padx=6); f.pack(fill="x", pady=1)
        vs=tk.StringVar(value=s); ve=tk.StringVar(value=e); vl=tk.StringVar(value=lbl)
        for lab, var, w in [("From:",vs,7),("To:",ve,7),("Label:",vl,12)]:
            tk.Label(f, text=lab, font=("Segoe UI",10),
                     bg=SF, fg=TX).pack(side="left", padx=(4,0))
            tk.Entry(f, textvariable=var, width=w,
                     font=("Consolas",11), bg=IP, fg=TX).pack(side="left", padx=2)
        ref=(vs,ve,vl); exc_rows.append(ref)
        tk.Button(f, text="X", bg="#f85149", fg="white", relief="flat",
                  font=("Segoe UI",9), cursor="hand2",
                  command=lambda: (f.destroy(), exc_rows.remove(ref))
                  ).pack(side="right", padx=4)

    for er in cfg["exclude_ranges"]:
        add_exc(er["start"], er["end"], er["label"])
    tk.Button(body, text="+ Add Range", font=("Segoe UI",10), bg=IP, fg=AC,
              relief="flat", pady=3, cursor="hand2",
              command=add_exc).pack(anchor="w", pady=3)

    def save():
        cfg["interval_minutes"]     = iv.get()
        cfg["snooze_minutes"]       = sv.get()
        cfg["auto_dismiss_seconds"] = av.get()
        cfg["display_mode"]         = mv.get()
        cfg["work_hours"]["enabled"]= wv.get()
        cfg["work_hours"]["start"]  = ws.get().strip()
        cfg["work_hours"]["end"]    = we.get().strip()
        cfg["exclude_ranges"] = [
            {"start":vs_.get().strip(),"end":ve_.get().strip(),
             "label":vl_.get().strip() or "Excluded"}
            for vs_,ve_,vl_ in exc_rows
            if vs_.get().strip() and ve_.get().strip()
        ]
        cfg.save()
        messagebox.showinfo("Saved","Settings saved! Timer has been reset.", parent=win)
        win.destroy()
        if on_save_cb: on_save_cb()

    tk.Frame(body, bg=BG, height=4).pack()
    tk.Button(body, text="Save & Apply",
              font=("Segoe UI",13,"bold"),
              bg="#238636", fg="white", relief="flat",
              pady=10, padx=28, cursor="hand2",
              command=save).pack(pady=6)


# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    log.info("="*50)
    log.info("stretch_reminder.pyw starting")

    if not TRAY_OK:
        r = tk.Tk(); r.withdraw()
        messagebox.showwarning("Missing Libraries",
            "pystray / Pillow not found.\nRun install.bat to add tray icon support.\n\n"
            "Reminders will still fire without it.", parent=r)
        r.destroy()

    if not POPUP_F.exists():
        r = tk.Tk(); r.withdraw()
        messagebox.showerror("Missing File",
            f"popup.pyw not found!\nExpected at:\n{POPUP_F}", parent=r)
        r.destroy()
        sys.exit(1)

    App().run()
