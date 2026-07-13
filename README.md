# Invention Machine Margins ⚙️📈

A comprehensive, automated profit calculator for RuneScape 3 Invention Machines. Available as both a standalone desktop application and a sleek, fully-featured Alt1 Toolkit web app.

## Features

- **Live GE Prices:** Automatically fetches the latest Grand Exchange prices using the Weirdgloop API.
- **5 Machine Types Supported (Mk. I & Mk. II):**
  - Alchemiser
  - Auto Disassembler
  - Plank Maker
  - Hide Tanner
  - Potion Producer
- **Advanced Capital & Uptime Analytics:** 
  - Calculates exactly how much daily capital is required to fund each margin.
  - Displays maximum machine uptime (in days) before you need to refill them.
- **Component Valuations:** Calculates the implied value of rare components (e.g., Noxious, Ilujankan) based on current weapon prices.
- **Buy Limit Warnings:** Automatically flags items if their GE buy limit bottlenecks your machine's daily processing capacity.
- **Customization Options:**
  - Toggle 2% GE Tax
  - Set your Junk Reduction Tier for accurate Disassembler yields
  - Define custom Divine Charge prices (useful if you gather your own energy)
  - Add and save custom item recipes directly from the UI

## 🌐 Alt1 Toolkit Web App (New!)
The web app is located in the `alt1/` directory. It features a premium, glassmorphism UI with RuneScape Wiki icon integration, dynamic sorting, and persistent `localStorage` settings. 

### Web App Features:
- **Alt1 Integration:** Ready for native Alt1 screen reading hooks.
- **Progressive Web App (PWA):** Works beautifully on mobile! You can install the web app to your phone's home screen for offline caching and native app feel.
- **How to Use in Alt1:** Simply point your Alt1 browser to the hosted URL or load the `alt1/index.html` file locally.

## 💻 Python Desktop App

### Requirements
- Python 3.10+
- `sv_ttk` (for the dark theme UI)

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
This repository is configured with **GitHub Actions**. Every time the code is updated, standalone applications are automatically compiled for Windows, macOS, and Linux. You don't need Python installed to run these!

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
python -m PyInstaller --noconfirm --onefile --windowed --icon=app_icon.ico --name InventionMachineMargins InventionMachineMargins.py
```
The compiled executable will be generated in the `dist/` folder.
