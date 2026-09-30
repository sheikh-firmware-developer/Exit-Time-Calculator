# ⏳ TimeTracker HUD

A minimalist, crystal-clear Windows desktop utility designed using the **MVC (Model-View-Controller)** pattern. It calculates shift exit times, manages policy rules dynamically, and embeds an intelligent bi-directional deficit gap auditor.

## ✨ Key Features
* 🕒 **Live Dynamic Sync:** Compact single-line HUD date and microsecond system clock stream.
* 🌓 **Smart Workspace Themes:** Choose between Light, Dark, or automatic Windows System theme integration.
* 🛡️ **Flexible Boundary Guard:** Toggle strict business compliance schedules or run in open flexible mode.
* 🚪 **Short Leave Automation:** Dynamically shifts calculation target limits whether leaves are clubbed at the Start or End.
* 📊 **Deficit Gap Auditor:** Background calculation engine tracks boundaries to flag shortfalls down to the minute.

## 🚀 How to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com
   cd TimeTracker
   ```
2. Run the application directly using Python:
   ```bash
   python main.py
   ```

## 📦 How to Build the Standalone Executable (.exe)
To compile the multi-file architecture into a single, clean portable executable binary, execute:
```bash
pip install -r requirements.txt
python -m PyInstaller --noconsole --onefile --icon="app_icon.ico" --version-file="file_version_info.txt" main.py
```
The compiled program will be inside the generated `dist/` directory!
