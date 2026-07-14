Still a work in progress
# RS3 Invention Machine Margins ⚙️

An elegant, premium-designed Alt1 Toolkit application for calculating and tracking profitable items for Runescape 3 Invention Machines.

Hosted at: **[invent.armstrader.store](https://invent.armstrader.store)**

## Features ✨

- **Beautiful Dark Mode UI:** A clean, glassmorphic design featuring smooth micro-animations and typography.
- **Top 25 Profitable Items:** Track the best margins for:
  - 🪄 Auto Alchemiser
  - 🔨 Auto Disassembler
  - 🪵 Plank Maker
  - 🐉 Hide Tanner
- **Custom Items:** Easily calculate and add your own custom items to track their specific margins. 
- **Alt1 Integration:** Seamlessly integrates into your Runescape Alt1 Toolkit overlay.

## Installing in Alt1 Toolkit 🛠️

1. Open the **Alt1 Toolkit** application while running Runescape 3.
2. Click the **Browser** button in the Alt1 toolbar.
3. Navigate to `https://invent.armstrader.store`.
4. Click "Add App" on the toolbar prompt to save it to your Alt1 apps list.

## Local Development 💻

This project is built using Vanilla JS, HTML, and CSS with [Vite](https://vitejs.dev/) for an optimized development experience.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/cook0001/RS3_InventionMachineMargins.git
   cd RS3_InventionMachineMargins
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```

4. **Build for production:**
   ```bash
   npm run build
   ```

## Automated Deployment 🚀

This repository uses GitHub Actions for continuous deployment.
Pushing changes to the `main` branch automatically triggers a build that outputs to the `gh-pages` branch, serving it immediately to `invent.armstrader.store`.
