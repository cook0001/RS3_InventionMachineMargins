# Invention Machine Margins ⚙️📈

A comprehensive, automated profit calculator for RuneScape 3 Invention Machines.

## Features
- **Live GE Prices:** Automatically fetches the latest Grand Exchange prices using the Weirdgloop API.
- **5 Machine Types Supported:**
  - Alchemiser Mk. II
  - Auto Disassembler Mk. II
  - Plank Maker
  - Hide Tanner
  - Potion Producer DX
- **Global Dashboard:** A master leaderboard showing the absolute best machine+item combinations across all categories.
- **Custom Items:** Add and save custom item recipes directly from the UI for the Alchemiser and Disassembler.
- **Junk Reduction Scaling:** Built-in yield multipliers for precise Auto Disassembler calculations based on your account's Junk Reduction Tier.

## Requirements
- Python 3.10+
- `sv_ttk` (for the dark theme UI)

## Installation & Running from Source
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
