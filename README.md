# Stretch_Reminder
🧘‍♂️ Stretch Reminder App
<div align="center">
Version
Platform
License
Status

💪 Your Personal Health Companion - Never Forget to Stretch Again! 💪

⚡ Quick Start • ✨ Features • 📥 Download • 🎨 Screenshots • ⚙️ Setup

<img src="https://user-images.githubusercontent.com/placeholder/stretch-demo.gif" width="600" alt="Stretch Reminder Demo">
🌟 Stay Healthy • Be Productive • Feel Amazing 🌟
</div>
📖 Table of Contents
🎯 About
✨ Features
🖼️ Screenshots
🚀 Quick Start
💻 Windows Version
🌐 Web Version
📱 Android Setup
⚙️ Configuration
🎨 Customization
🤝 Contributing
📝 License
💖 Credits
🎯 About
"Your body is your most priceless possession. Take care of it." – Jack Lalanne

Stretch Reminder is a beautiful, minimalist desktop & web application that helps you maintain a healthy work routine by reminding you to take stretch breaks. Built with ❤️ to combat the negative effects of prolonged sitting.

🎁 Why Stretch Reminder?
Problem 😓	Solution ✅
Sitting for hours causes back pain	Regular stretch reminders every 40 minutes
Easy to forget to move	Beautiful full-screen notifications you can't miss
Boring health apps	Gorgeous acrylic glass UI with motivational quotes
Complex setup	Works out-of-the-box, no installation needed
Platform-specific	Works on Windows, Web, and Android!
✨ Features
<table> <tr> <td width="50%">
🎨 Beautiful Design
🌈 Stunning acrylic glass effect (Windows)
🎭 Modern gradient UI (Web)
🌙 Dark theme - easy on the eyes
📱 Fully responsive design
🎯 Clean, distraction-free interface
</td> <td width="50%">
🔔 Smart Notifications
⏰ Customizable reminder intervals
🔊 Sound alerts (optional)
📳 Vibration on mobile
🎯 Browser notifications
⏸️ Snooze functionality
</td> </tr> <tr> <td width="50%">
💪 Exercise Library
🧘 8 professionally curated exercises
🎲 Random exercise selection
📝 Clear, step-by-step instructions
🎯 Targets neck, shoulders, back & legs
⏱️ Time-based guidance
</td> <td width="50%">
⚙️ Powerful Settings
🕐 Adjustable interval (1-180 minutes)
⏰ Work hours scheduling
🚫 Exclude time ranges (lunch breaks)
🎵 Sound on/off
📳 Vibration control
</td> </tr> </table>
🌟 Special Features
text

✅ System Tray Integration (Windows)
✅ Auto-start with Windows
✅ Detailed activity logging
✅ Offline-first (works without internet)
✅ Privacy-focused (no data collection)
✅ Lightweight (< 100 KB)
✅ Zero dependencies (Web version)
✅ PWA support (Install as app)
🖼️ Screenshots
<div align="center">
💻 Windows Desktop Version
<img src="https://via.placeholder.com/800x450/0a0e1a/64b5f6?text=Full+Screen+Reminder" alt="Windows Fullscreen" width="800">
Beautiful acrylic glass effect with blur background

🌐 Web/Mobile Version
<table> <tr> <td width="33%"> <img src="https://via.placeholder.com/300x600/1a2332/b3e5fc?text=Mobile+View" alt="Mobile"> <p align="center"><b>📱 Mobile View</b></p> </td> <td width="33%"> <img src="https://via.placeholder.com/300x600/0a0e1a/64b5f6?text=Settings" alt="Settings"> <p align="center"><b>⚙️ Settings Panel</b></p> </td> <td width="33%"> <img src="https://via.placeholder.com/300x600/1a2332/43a047?text=Exercise+List" alt="Exercises"> <p align="center"><b>💪 Exercise Guide</b></p> </td> </tr> </table>
🎨 Features Showcase
Feature	Preview
🏆 Exercise Panel	Exercise
💬 Motivational Quotes	Quotes
⚙️ Smart Scheduling	Schedule
</div>
🚀 Quick Start
⚡ TL;DR - Get Started in 30 Seconds
🌐 Web Version (Fastest - Works Everywhere!)
Bash

# 1. Download the HTML file
# 2. Open in any browser
# 3. Click "Add to Home Screen"
# Done! 🎉
👉 Try Web Demo (Replace with your actual link)

💻 Windows Version (Native Desktop App)
Bash

# 1. Download the ZIP file
# 2. Extract to any folder
# 3. Double-click stretch_reminder.pyw
# Done! 🎉
👉 Download for Windows (Replace with actual release link)

💻 Windows Version
📋 Requirements
✅ Windows 10/11
✅ Python 3.7+ (usually pre-installed)
✅ Optional: pystray, Pillow (for system tray icon)
📥 Installation
<details> <summary><b>🔽 Click to expand installation steps</b></summary>
Option 1: Simple Setup (Recommended)
Bash

# 1. Clone or download this repository
git clone https://github.com/your-username/stretch-reminder.git
cd stretch-reminder

# 2. Install dependencies (optional - for tray icon)
pip install pystray Pillow

# 3. Run the app
python stretch_reminder.pyw
Option 2: Portable Version
Download stretch-reminder-windows.zip from Releases
Extract to C:\StretchReminder\
Double-click stretch_reminder.pyw
(Optional) Right-click → Send to → Desktop (create shortcut)
Option 3: Auto-start with Windows
Bash

# Press Win+R, type: shell:startup
# Copy the shortcut to this folder
# The app will now start automatically!
</details>
⚙️ Windows Configuration
Edit config.json:

JSON

{
  "interval_minutes": 40,          // ⏰ Remind every X minutes
  "snooze_minutes": 5,             // ⏸️ Snooze duration
  "display_mode": "fullscreen",    // 🖥️ fullscreen or halfscreen
  "auto_dismiss_seconds": 0,       // ⏱️ Auto-close (0 = disabled)
  "work_hours": {
    "enabled": true,               // 🕐 Schedule reminders
    "start": "09:00",              // 🌅 Work start time
    "end": "18:30",                // 🌆 Work end time
    "days": [0,1,2,3,4]            // 📅 Mon-Fri (0=Monday)
  }
}
<details> <summary><b>🎨 See full configuration options</b></summary>
JSON

{
  "interval_minutes": 40,
  "snooze_minutes": 5,
  "display_mode": "fullscreen",
  "auto_dismiss_seconds": 0,
  "work_hours": {
    "enabled": true,
    "start": "09:00",
    "end": "18:30",
    "days": [0, 1, 2, 3, 4]
  },
  "exclude_ranges": [
    {
      "start": "12:00",
      "end": "13:00",
      "label": "Lunch Break"
    }
  ],
  "messages": [
    "Time to Stand Up and Stretch!",
    "Get Up and Move Your Body!",
    "Custom motivational message here..."
  ],
  "exercises": [
    "🧘 Neck rolls - 10 rotations each direction",
    "💪 Your custom exercise here..."
  ]
}
</details>
🌐 Web Version
🌟 Perfect for:
📱 Android & iPhone users
💻 Chromebook users
🌍 Any device with a browser
🚀 No installation needed
🎯 How to Use
Method 1: Direct Use
Download stretch-reminder.html
Open in Chrome/Firefox/Safari
Bookmark it (Ctrl+D)
Done! ✨
Method 2: Install as PWA (Progressive Web App)
On Android:

text

1. Open the HTML file in Chrome
2. Tap ⋮ menu → "Add to Home Screen"
3. Now it works like a native app! 📱
On Desktop:

text

1. Open in Chrome/Edge
2. Click install icon (⊕) in address bar
3. Now available as desktop app! 💻
Method 3: Host Online (Free)
<details> <summary><b>🌍 Click to see hosting options</b></summary>
GitHub Pages (Recommended)

Bash

1. Create GitHub account
2. Create new repository "stretch-reminder"
3. Upload stretch-reminder.html
4. Settings → Pages → Enable
5. Access at: https://yourusername.github.io/stretch-reminder/
Other Free Hosting:

🔷 Netlify - Drag & drop
🔶 Vercel - One-click deploy
🟢 Surge.sh - Command-line deploy
🔴 Firebase Hosting - Google's platform
</details>
📱 Web Features
JavaScript

✅ Browser Notifications
✅ Sound Alerts
✅ Vibration (mobile)
✅ Offline Support
✅ Settings Persistence (localStorage)
✅ Responsive Design
✅ Works on Any Device
📱 Android Setup
🎯 Best Methods for Android
Option 1: Web App (Easiest) ⭐
Open stretch-reminder.html in Chrome
Tap ⋮ → Add to Home Screen
Choose app name → Add
Access from home screen like any app!
Features:

✅ Notifications
✅ Vibration
✅ Sound alerts
✅ Full offline support
✅ No app store needed
Option 2: Automation Apps
<details> <summary><b>📲 Using MacroDroid (Free)</b></summary>
text

1. Install MacroDroid from Play Store
2. Create new macro:
   Trigger: Time-based (every 40 minutes)
   Action: Show notification "Time to Stretch!"
   Action: Vibrate device
   Action: Open stretch exercises (web link)
3. Enable macro
</details><details> <summary><b>📲 Using Tasker ($3.49)</b></summary>
text

1. Install Tasker from Play Store
2. Create Profile:
   Time: Every 40 minutes
3. Add Task:
   Alert → Notify → "Stretch Time!"
   Alert → Vibrate
   App → Browse URL → stretch-reminder.html
</details>
⚙️ Configuration
🎨 Customization Guide
Change Colors
Edit popup.pyw (Windows) or stretch-reminder.html (Web):

Python

# Line 132 - Time color
fg="#64b5f6"  # Change to any hex color

# Line 159 - Panel border
bg="#58a6ff"  # Blue glow effect

# Line 193 - Exercise text
fg="#b3e5fc"  # Light cyan text
Add Your Own Exercises
Edit config.json:

JSON

"exercises": [
  "🧘 Your custom exercise here",
  "💪 Another exercise with emoji",
  "🤸 Make it fun and descriptive!"
]
Change Font Sizes
Python

# popup.pyw - Line 145
font=("Segoe UI", 32, "bold")  # Message size (32pt)

# Line 193
font=("Segoe UI", 12)  # Exercise size (12pt)
📊 Activity Logging
View your stretch history in stretch_log.txt:

text

2024-01-15 14:30:00  Timer fired - checking schedule...
2024-01-15 14:30:00  Schedule OK - calling fire_cb
2024-01-15 14:32:15  Done - timer reset to full interval
🎨 Customization
🌈 Color Schemes
<details> <summary><b>🎨 Click to see pre-made themes</b></summary>
Ocean Blue (Default)
CSS

--bg: #0a0e1a
--panel: #1a2332
--accent: #1e88e5
--text: #b3e5fc
Forest Green
CSS

--bg: #0a1a0a
--panel: #1a3320
--accent: #43a047
--text: #c8e6c9
Sunset Orange
CSS

--bg: #1a0f0a
--panel: #332218
--accent: #ff6f00
--text: #ffe0b2
Purple Dream
CSS

--bg: #120a1a
--panel: #221833
--accent: #7c4dff
--text: #e1bee7
</details>
💬 Custom Messages
Add your own motivational messages in config.json:

JSON

"messages": [
  "🌟 You're doing great! Time to stretch!",
  "💪 Strong body, strong mind - let's move!",
  "🎯 Quick 2-minute break = Better focus!",
  "Your custom message here..."
]
🎵 Custom Sounds
<details> <summary><b>🔊 Add your own notification sound</b></summary>
Edit stretch-reminder.html around line 350:

JavaScript

function playSound() {
    const audio = new Audio('your-sound.mp3');
    audio.play();
}
</details>
🤝 Contributing
We ❤️ contributions! Here's how you can help:

🌟 Ways to Contribute
🐛 Report Bugs - Found an issue? Open an issue
💡 Suggest Features - Have an idea? Share it!
🎨 Improve Design - Submit UI/UX improvements
📝 Fix Typos - Even small fixes matter
🌍 Translations - Help translate to other languages
💪 Add Exercises - Share your favorite stretches
🔧 Development Setup
Bash

# Fork the repository
git clone https://github.com/your-username/stretch-reminder.git
cd stretch-reminder

# Create a branch
git checkout -b feature/amazing-feature

# Make your changes
# Test thoroughly

# Commit
git commit -m "Add amazing feature"

# Push
git push origin feature/amazing-feature

# Open a Pull Request
📜 Contribution Guidelines
✅ Follow existing code style
✅ Test on Windows & Web before submitting
✅ Update documentation if needed
✅ Add comments for complex code
✅ Be respectful and constructive
📝 License
text

MIT License

Copyright (c) 2024 kxo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
Full license: LICENSE

💖 Credits
<div align="center">
👨‍💻 Created with ❤️ by kxo
Special thanks to:

Contribution	Credit
🎨 UI Inspiration	Windows Acrylic Design
💪 Exercise Guidance	Physical Therapy Experts
🎵 Sound Effects	Web Audio API
📱 PWA Support	Google Developers
🐍 Python Framework	Tkinter Community
🌟 Star History
Star History Chart

📊 Stats
GitHub stars
GitHub forks
GitHub watchers

GitHub issues
GitHub pull requests
GitHub last commit

💬 Get in Touch
Have questions or suggestions?

GitHub
Email
Twitter

🎯 Project Roadmap
 ✅ Windows desktop version
 ✅ Web/PWA version
 ✅ Android support
 🔄 macOS native app
 🔄 iOS app
 🔄 Linux version
 🔄 Exercise video tutorials
 🔄 Multi-language support
 🔄 Streak tracking
 🔄 Health statistics dashboard
🏆 Support This Project
If this app helped you stay healthy, consider:

⭐ Star this repository
🐛 Report bugs
💡 Suggest features
🤝 Contribute code
☕ Buy me a coffee
<img src="https://via.placeholder.com/800x2/1e88e5/1e88e5" alt="divider">
"Take care of your body. It's the only place you have to live." – Jim Rohn
Stay healthy. Stay active. Stretch regularly. 💪

<img src="https://via.placeholder.com/800x2/43a047/43a047" alt="divider">
Made with 💙 by kxo • 2024

Your body deserves it. ✨

</div>
🔗 Quick Links
📖 Full Documentation
🐛 Report Bug
💡 Request Feature
📝 Changelog
🤝 Contributing Guide
❓ FAQ
<div align="center">
If you found this helpful, give it a ⭐!

Happy Stretching! 🧘‍♂️💪🎉

</div>
