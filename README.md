# Invention Machine Margins ⚙️📈

A comprehensive, automated profit calculator for RuneScape 3 Invention Machines. V3 represents a massive architecture upgrade, moving to a unified glassmorphism UI built on PyWebView for desktop and fully compatible with the Alt1 Toolkit on the web!

## ✨ New in V3 (Mega Update)
- **Best Machine Loadout Optimizer:** Enter your Max Generator Power, and our knapsack algorithm runs through all live GE margins to mathematically prove the absolute most profitable combination of machines you can build!
- **RuneScape Wiki Live Search:** Add custom items with zero friction! Simply type in the new search bar—it auto-completes items directly from the live RS Wiki, scrapes the wikitext, and mathematically calculates the exact High Alch value for you automatically.
- **Historical 90-Day Charts:** Click any item card to instantly render a sleek HTML5 canvas sparkline graph showing the item's GE price trend over the last 90 days.
- **Instant Offline Caching:** The app now locally caches live GE prices and wiki IDs. Upon opening, it instantly loads with offline data while silently fetching live updates in the background.
- **Unified PyWebView Desktop App:** We completely scrapped the old Python Tkinter UI. The desktop `.exe` now uses `pywebview` to natively wrap the gorgeous Alt1 HTML/CSS/JS frontend, ensuring 100% feature parity!
- **Expanded Recipe Database:** Massively expanded the default disassembler logic (yew/magic/elder logs, jewelry) and added a massive list of potion (unf) recipes!

## Core Features
- **Live GE Prices:** Automatically fetches the latest Grand Exchange prices using the Weirdgloop API.
- **5 Machine Types Supported (Mk. I & Mk. II):** Alchemiser, Auto Disassembler, Plank Maker, Hide Tanner, Potion Producer.
- **Advanced Capital & Uptime Analytics:** 
  - Calculates exactly how much daily capital is required to fund each margin.
  - Displays maximum machine uptime (in days) before you need to refill them.
- **Component Valuations:** Calculates the implied value of rare components (e.g., Noxious, Ilujankan) based on current weapon prices.
- **Buy Limit Warnings:** Automatically flags items if their GE buy limit bottlenecks your machine's daily processing capacity.
- **Customization Options:**
  - Config Backup/Restore (Export to clipboard / Import JSON)
  - Customizable refresh rate loop (1m, 5m, 15m, manual)
  - Toggle 2% GE Tax and Junk Reduction Tiers
  - Define custom Divine Charge prices

## 🌐 Alt1 Toolkit Web App
The web app is located in the `alt1/` directory. 
- **Progressive Web App (PWA):** Works beautifully on mobile! You can install the web app to your phone's home screen for offline caching and a native app feel.
- **How to Use in Alt1:** 
  - **Direct Install (Recommended):** [Click here to install directly into Alt1](https://invent.armstrader.store/install.html)
  - **Manual Install:** Open Alt1 Toolkit, click the copy button on the URL below, paste it into the Alt1 address bar, and click the green "Add App" button.
  ```text
  https://invent.armstrader.store/appconfig_v3.json
  ```

## 💻 Python Desktop App

### Requirements
- Python 3.10+
- `pywebview` (for the native desktop wrapper)

### Installation & Running from Source
1. Clone the repository.
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python InventionMachineMargins.py
   ```

## Downloading Compiled Apps (Windows, macOS, Linux)
This repository is configured with **GitHub Actions**. Every time the code is updated, standalone applications are automatically compiled for Windows, macOS, and Linux using PyInstaller.

To download the latest compiled version:
1. Go to the [**Releases**](https://github.com/cook0001/RS3_InventionMachineMargins/releases) tab on the right side of the repository page.
2. Click on the "Latest Automated Build".
3. Under the **Assets** section, download the version for your operating system:
   - `InventionMachineMargins-Windows.exe`
   - `InventionMachineMargins-macOS.zip` (extract to get the Mac `.app` bundle)
   - `InventionMachineMargins-Linux`

## Manual Local Compilation
If you prefer to compile the application locally yourself using PyInstaller:
```bash
pip install pyinstaller
python -m PyInstaller --noconfirm --onefile --windowed --add-data "alt1;alt1" --icon=app_icon.ico --name InventionMachineMargins InventionMachineMargins.py
```
*(Note: Because V3 uses PyWebView, we must use `--add-data "alt1;alt1"` to bundle the web UI inside the executable.)*
The compiled executable will be generated in the `dist/` folder.
