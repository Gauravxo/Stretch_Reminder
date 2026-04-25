<p align="center">
  <img src="https://raw.githubusercontent.com/your-repo/stretch-reminder/main/assets/icon.png" width="120" alt="Stretch Reminder Logo" />
</p>

<h1 align="center">🧘 Stretch Reminder</h1>
<p align="center">
  <b>Silent tray app that reminds you to stand up, stretch, and move – with a gorgeous acrylic‑glass popup</b><br>
  <sub>Timer • Work‑hour awareness • Exercise tips • Motivational quotes</sub>
</p>

<p align="center">
  <a href="https://github.com/your-repo/stretch-reminder/releases"><img src="https://img.shields.io/github/v/release/your-repo/stretch-reminder?style=for-the-badge&color=1e88e5" alt="Release" /></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" alt="License: MIT" /></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+" /></a>
  <a href="#"><img src="https://img.shields.io/badge/Platform-Windows%2010%2F11-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows 10/11" /></a>
  <a href="#"><img src="https://img.shields.io/badge/Works%20offline-✔-green?style=for-the-badge" alt="Offline" /></a>
</p>

---

## 📖 Overview

**Stretch Reminder** is a lightweight Windows application that lives in your system tray and gently nudges you to take regular stretch breaks.  
When the timer fires, a full‑screen (or half‑screen) acrylic‑blur overlay appears – displaying a beautiful stretch message, a motivational quote, and a set of quick exercises.  
It respects your work schedule, can be snoozed, and never interrupts when you're outside your configured hours or during excluded time ranges (like a lunch walk).

---

## ✨ Features

- 🖥️ **Acrylic glass popup** – Modern, translucent overlay with blur effect (Windows only)
- ⏱️ **Configurable timer** – Set any interval between 1 and 180 minutes
- 💤 **Snooze** – Postpone reminders by a custom duration
- 🏢 **Work‑hour awareness** – Only remind on chosen days and during specified hours
- 🚫 **Exclude ranges** – Skip breaks during lunch, meetings, etc.
- 🧘 **Exercise list** – Hand‑picked stretches you can do right at your desk
- 💬 **Motivational quotes** – Fresh encouragement every time
- 🎯 **Auto‑dismiss** – Optionally close the popup after a set number of seconds
- 🖼️ **Tray icon** – Always visible, right‑click menu for instant stretch, settings, log view, and exit
- 📋 **Logging** – All events recorded to a file for debugging
- 🔧 **Persistent settings** – All preferences saved in a JSON config file

---

## 🖼️ Screenshots

| Tray Icon & Menu | Popup (Fullscreen) | Settings Window |
|:---:|:---:|:---:|
| ![Tray](https://raw.githubusercontent.com/your-repo/stretch-reminder/main/screenshots/tray.png) | ![Popup](https://raw.githubusercontent.com/your-repo/stretch-reminder/main/screenshots/popup.png) | ![Settings](https://raw.githubusercontent.com/your-repo/stretch-reminder/main/screenshots/settings.png) |

*(Replace with actual screenshots)*

---

## ⚙️ Installation

> 💡 The app is fully portable – no installation required. Just download and run.

### 1. Requirements
- **Windows 10 / 11** (64‑bit)
- **Python 3.8+** (with Tkinter – included in standard Windows Python installers)
- **pystray** and **Pillow** for the tray icon *(optional – the app still runs without them)*

### 2. Download
Clone the repository or download the source files:
```bash
git clone https://github.com/your-repo/stretch-reminder.git
cd stretch-reminder
