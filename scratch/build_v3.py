import json
import os

html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Invention Machine Margins</title>
    <link rel="manifest" href="manifest.json">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #0B0E14;
            --bg-surface: rgba(22, 27, 34, 0.6);
            --bg-surface-hover: rgba(30, 36, 45, 0.8);
            --text-primary: #F8FAFC;
            --text-secondary: #94A3B8;
            --border: rgba(255, 255, 255, 0.1);
            --profit: #10B981;
            --loss: #EF4444;
            --brand: #38BDF8;
            --brand-glow: rgba(56, 189, 248, 0.3);
            --bottleneck: #F59E0B;
            --radius: 12px;
            --font-main: 'Outfit', sans-serif;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body { font-family: var(--font-main); background: transparent; color: var(--text-primary); overflow: hidden; }

        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.2); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.3); }

        .app-container { width: 100vw; height: 100vh; background: linear-gradient(135deg, #0B0E14 0%, #111827 100%); backdrop-filter: blur(10px); display: flex; flex-direction: column; }

        header { padding: 16px 24px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; background: rgba(0, 0, 0, 0.2); flex-shrink: 0; }
        .header-title { display: flex; flex-direction: column; gap: 4px; }
        h1 { font-size: 18px; font-weight: 600; background: linear-gradient(90deg, #38BDF8, #818CF8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 0.5px; }
        .status { font-size: 12px; color: var(--text-secondary); display: flex; align-items: center; gap: 8px; font-weight: 500; }
        .status-dot { width: 8px; height: 8px; background-color: var(--profit); border-radius: 50%; box-shadow: 0 0 10px var(--profit); transition: background-color 0.3s; }
        .status-dot.loading { background-color: var(--bottleneck); box-shadow: 0 0 10px var(--bottleneck); animation: pulse 1.5s infinite; }
        .status-dot.error { background-color: var(--loss); box-shadow: 0 0 10px var(--loss); }
        .status-dot.cached { background-color: #818CF8; box-shadow: 0 0 10px #818CF8; }
        @keyframes pulse { 0% { opacity: 1; transform: scale(1); } 50% { opacity: 0.6; transform: scale(1.2); } 100% { opacity: 1; transform: scale(1); } }
        .header-controls { display: flex; gap: 12px; align-items: center; }
        button.icon-btn { background: rgba(255,255,255,0.05); border: 1px solid var(--border); color: var(--text-primary); width: 36px; height: 36px; border-radius: 8px; cursor: pointer; display: flex; justify-content: center; align-items: center; transition: all 0.2s; font-size: 16px; }
        button.icon-btn:hover { background: rgba(255,255,255,0.1); transform: translateY(-1px); }

        .nav-scroll { overflow-x: auto; border-bottom: 1px solid var(--border); background: rgba(0,0,0,0.1); flex-shrink: 0; }
        .nav-tabs { display: flex; padding: 0 16px; gap: 8px; width: max-content; }
        .tab { background: transparent; border: none; color: var(--text-secondary); padding: 12px 16px; font-family: var(--font-main); font-size: 13px; font-weight: 500; cursor: pointer; position: relative; transition: color 0.2s; }
        .tab:hover { color: var(--text-primary); }
        .tab.active { color: var(--brand); }
        .tab.active::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 2px; background: var(--brand); box-shadow: 0 -2px 10px var(--brand-glow); border-radius: 2px 2px 0 0; }
        
        .opt-btn { background: rgba(56, 189, 248, 0.1); color: var(--brand); border: 1px solid var(--brand); padding: 4px 12px; border-radius: 12px; font-size: 12px; cursor: pointer; display: flex; align-items: center; gap: 4px; font-weight: 600; }
        .opt-btn:hover { background: rgba(56, 189, 248, 0.2); }

        .toolbar { padding: 12px 24px; display: flex; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.15); border-bottom: 1px solid var(--border); flex-shrink: 0; }
        .sort-select { background: rgba(0,0,0,0.3); border: 1px solid var(--border); color: var(--text-primary); padding: 6px 12px; border-radius: 6px; font-family: var(--font-main); font-size: 13px; outline: none; cursor: pointer; }
        .sort-select:focus { border-color: var(--brand); }
        .tab-desc { font-size: 13px; color: var(--text-secondary); display: flex; align-items: center; gap: 12px; }

        .content { flex-grow: 1; overflow-y: auto; padding: 16px 24px; position: relative; }
        
        .card { background: var(--bg-surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 16px; margin-bottom: 12px; cursor: pointer; transition: all 0.2s ease; position: relative; overflow: hidden; }
        .card:hover { background: var(--bg-surface-hover); border-color: rgba(255, 255, 255, 0.2); transform: translateY(-2px); box-shadow: 0 4px 20px rgba(0,0,0,0.2); }
        .card::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px; background: var(--brand); opacity: 0.5; }
        .card-header { display: flex; justify-content: space-between; align-items: center; }
        .card-left { display: flex; align-items: center; gap: 12px; }
        .item-icon { width: 32px; height: 32px; object-fit: contain; background: rgba(0,0,0,0.3); border-radius: 6px; padding: 2px; border: 1px solid var(--border); }
        .item-info { display: flex; flex-direction: column; gap: 4px; }
        .item-name { font-size: 15px; font-weight: 600; color: var(--text-primary); }
        .tags { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
        .tag { font-size: 11px; padding: 2px 6px; border-radius: 4px; font-weight: 500; background: rgba(255,255,255,0.05); color: var(--text-secondary); border: 1px solid rgba(255,255,255,0.05); }
        .tag.bottleneck { color: var(--bottleneck); background: rgba(245, 158, 11, 0.1); border-color: rgba(245, 158, 11, 0.2); }
        .card-right { display: flex; flex-direction: column; align-items: flex-end; gap: 4px; }
        .profit-day { font-size: 15px; font-weight: 700; }
        .profit-day.positive { color: var(--profit); }
        .profit-day.negative { color: var(--loss); }
        .profit-ea { font-size: 12px; color: var(--text-secondary); }
        .card-details { display: none; margin-top: 16px; padding-top: 16px; border-top: 1px dashed var(--border); font-size: 13px; color: var(--text-secondary); line-height: 1.5; animation: slideDown 0.3s ease; }
        .card.expanded .card-details { display: block; }
        @keyframes slideDown { from { opacity: 0; transform: translateY(-5px); } to { opacity: 1; transform: translateY(0); } }

        .modal-overlay { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.6); backdrop-filter: blur(4px); display: none; justify-content: center; align-items: center; z-index: 100; }
        .modal-overlay.open { display: flex; }
        .modal { background: #111827; border: 1px solid var(--border); border-radius: var(--radius); width: 90%; max-width: 450px; padding: 24px; box-shadow: 0 20px 40px rgba(0,0,0,0.5); max-height: 90vh; overflow-y: auto; }
        .modal h2 { margin-bottom: 20px; font-size: 18px; }
        .form-group { margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; }
        .form-group label { font-size: 14px; color: var(--text-secondary); }
        .form-input { background: rgba(0,0,0,0.3); border: 1px solid var(--border); color: white; padding: 8px 12px; border-radius: 6px; font-family: var(--font-main); width: 140px; outline: none; }
        .form-input:focus { border-color: var(--brand); }
        .modal-close { background: var(--brand); color: #000; border: none; padding: 10px 0; width: 100%; border-radius: 6px; font-weight: 600; margin-top: 10px; cursor: pointer; transition: opacity 0.2s; }
        .modal-close:hover { opacity: 0.9; }
        .btn { background: rgba(255,255,255,0.1); color: white; border: 1px solid var(--border); padding: 8px 12px; border-radius: 6px; cursor: pointer; font-family: var(--font-main); font-size: 13px; }
        .btn:hover { background: rgba(255,255,255,0.2); }
        .btn-brand { background: var(--brand); color: #000; border: none; }
        .btn-brand:hover { background: #7DD3FC; }

        .loader-wrapper { display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%; color: var(--text-secondary); font-size: 14px; gap: 16px; }
        .spinner { width: 40px; height: 40px; border: 3px solid rgba(255,255,255,0.1); border-top-color: var(--brand); border-radius: 50%; animation: spin 1s linear infinite; }
        @keyframes spin { to { transform: rotate(360deg); } }
        
        .opt-panel { background: rgba(56, 189, 248, 0.05); border: 1px solid rgba(56, 189, 248, 0.2); padding: 16px; border-radius: 8px; margin-bottom: 16px; display: none; }
        .opt-panel.open { display: block; }
        .opt-result { margin-top: 12px; padding-top: 12px; border-top: 1px dashed rgba(56, 189, 248, 0.2); color: var(--brand); font-weight: 600; }
        
        .history-btn { font-size: 11px; background: rgba(255,255,255,0.1); border: 1px solid var(--border); color: var(--text-primary); padding: 2px 8px; border-radius: 4px; cursor: pointer; margin-top: 8px; }
        .history-btn:hover { background: rgba(255,255,255,0.2); }
        .canvas-container { margin-top: 10px; width: 100%; height: 60px; display: none; }
    </style>
</head>
<body>
    <div class="app-container">
        <header>
            <div class="header-title">
                <h1>Invention Margins</h1>
                <div class="status">
                    <div class="status-dot" id="status-dot"></div>
                    <span id="status-text">Fetching prices...</span>
                </div>
            </div>
            <div class="header-controls">
                <button class="icon-btn" onclick="scanBankAlt1()" title="Scan Bank with Alt1">👁️</button>
                <button class="icon-btn" onclick="fetchPrices(true)" title="Refresh">↻</button>
                <button class="icon-btn" onclick="toggleSettings()" title="Settings">⚙</button>
            </div>
        </header>

        <div class="nav-scroll">
            <div class="nav-tabs" id="tabs-container">
                <button class="tab active" onclick="setTab('Dashboard')">Dashboard</button>
                <button class="tab" onclick="setTab('Alchemiser')">Alchemiser</button>
                <button class="tab" onclick="setTab('Plank Maker')">Plank Maker</button>
                <button class="tab" onclick="setTab('Hide Tanner')">Hide Tanner</button>
                <button class="tab" onclick="setTab('Potion Producer')">Potion</button>
                <button class="tab" onclick="setTab('Auto Disassembler')">Disassembler</button>
                <button class="tab" onclick="setTab('Components')">Components</button>
                <button class="tab" onclick="setTab('Custom')">Custom Items</button>
            </div>
        </div>

        <div class="toolbar">
            <div class="tab-desc">
                <span id="tab-desc-text">Top 25 Most Profitable Items</span>
                <button class="opt-btn" id="opt-btn" onclick="toggleOptimizer()">✨ Optimizer</button>
            </div>
            <select class="sort-select" id="sort-select" onchange="setSort(this.value)">
                <option value="day">Sort: Profit / Day</option>
                <option value="item">Sort: Profit / Item</option>
            </select>
        </div>

        <div class="content" id="data-container">
            <div class="opt-panel" id="opt-panel">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span>Max Generator Power:</span>
                    <input type="number" id="opt-power" class="form-input" value="160" style="width: 80px;" onchange="runOptimizer()">
                </div>
                <div id="opt-result" class="opt-result">Click to calculate best layout...</div>
            </div>
            <div id="cards-container">
                <div class="loader-wrapper">
                    <div class="spinner"></div>
                    <div>Fetching live GE data...</div>
                </div>
            </div>
        </div>
    </div>

    <div class="modal-overlay" id="settings-modal" onclick="if(event.target===this) toggleSettings()">
        <div class="modal">
            <h2>Settings</h2>
            <div class="form-group">
                <label>Refresh Rate</label>
                <select id="setting-refresh" class="form-input" onchange="updateRefreshInterval()">
                    <option value="1">1 Minute</option>
                    <option value="5">5 Minutes</option>
                    <option value="15">15 Minutes</option>
                    <option value="0">Manual Only</option>
                </select>
            </div>
            <div class="form-group">
                <label>Machine Tier</label>
                <select id="setting-tier" class="form-input" onchange="saveSettings()">
                    <option value="2">Mk. II (Max)</option>
                    <option value="1">Mk. I</option>
                </select>
            </div>
            <div class="form-group">
                <label>Apply 2% GE Tax</label>
                <input type="checkbox" id="setting-tax" onchange="saveSettings()" style="width:18px;height:18px;cursor:pointer;">
            </div>
            <div class="form-group">
                <label>Junk Reduction Tier (0-9)</label>
                <input type="number" id="setting-junk" class="form-input" min="0" max="9" onchange="saveSettings()">
            </div>
            <div class="form-group">
                <label>Custom Divine Charge Price</label>
                <input type="number" id="setting-charge" class="form-input" placeholder="Live Price" onchange="saveSettings()">
            </div>
            
            <hr style="border-color: var(--border); margin: 20px 0;">
            <h3>Config Backup</h3>
            <div style="display:flex; gap:10px; margin-top:10px;">
                <button class="btn" style="flex:1;" onclick="exportConfig()">📤 Export</button>
                <button class="btn" style="flex:1;" onclick="importConfig()">📥 Import</button>
            </div>

            <hr style="border-color: var(--border); margin: 20px 0;">
            <h3>Add Custom Item</h3>
            <div style="display:flex; gap:10px; margin-top:10px;">
                <input type="text" id="c-name" class="form-input" placeholder="Item Name" style="width: 100%;">
                <input type="number" id="c-alch" class="form-input" placeholder="Alch Val">
            </div>
            <button class="btn btn-brand" style="width:100%; margin-top:10px;" onclick="addCustomItem()">Add to Alchemiser</button>
            
            <button class="modal-close" onclick="toggleSettings()" style="margin-top: 20px;">Save & Close</button>
        </div>
    </div>

    <script>
        if ('serviceWorker' in navigator) { navigator.serviceWorker.register('sw.js'); }

        const MACHINE_CHARGES_PER_DIVINE_CHARGE = 3000;
        
        const MACHINES = {
            "Alchemiser": { 2: { iph: 25, cpi: 150/25, cap: 10000, power: 40 }, 1: { iph: 8, cpi: 55/8, cap: 5000, power: 20 } },
            "Plank Maker": { 2: { iph: 40, cpi: 600/40, cap: 10000, power: 40 }, 1: { iph: 40, cpi: 600/40, cap: 10000, power: 40 } },
            "Hide Tanner": { 2: { iph: 140, cpi: 225/140, cap: 10000, power: 40 }, 1: { iph: 140, cpi: 225/140, cap: 10000, power: 40 } },
            "Potion Producer": { 2: { iph: 40, cpi: 210/40, cap: 10000, power: 40 }, 1: { iph: 40, cpi: 210/40, cap: 10000, power: 40 } },
            "Auto Disassembler": { 2: { iph: 35, cpi: 180/35, cap: 10000, power: 40 }, 1: { iph: 20, cpi: 100/20, cap: 5000, power: 20 } }
        };

        const DEFAULT_ALCH_ITEMS = [
            {name: "Huge bladed rune salvage", alch: 40000, limit: 100}, {name: "Huge plated rune salvage", alch: 40000, limit: 100},
            {name: "Huge blunt rune salvage", alch: 40000, limit: 100}, {name: "Dragon halberd", alch: 150000, limit: 10},
            {name: "Onyx bolts (e)", alch: 5400, limit: 10000}
        ];

        const PLANK_RECIPES = [{log: "Logs", plank: "Plank", coin_cost: 100, limit: 10000}, {log: "Oak logs", plank: "Oak plank", coin_cost: 250, limit: 10000}, {log: "Teak logs", plank: "Teak plank", coin_cost: 500, limit: 10000}, {log: "Mahogany logs", plank: "Mahogany plank", coin_cost: 1500, limit: 10000}];
        const TANNER_RECIPES = [{hide: "Green dragonhide", leather: "Green dragon leather", coin_cost: 20, limit: 10000}, {hide: "Blue dragonhide", leather: "Blue dragon leather", coin_cost: 20, limit: 10000}, {hide: "Red dragonhide", leather: "Red dragon leather", coin_cost: 20, limit: 10000}, {hide: "Black dragonhide", leather: "Black dragon leather", coin_cost: 20, limit: 10000}, {hide: "Royal dragonhide", leather: "Royal dragon leather", coin_cost: 20, limit: 10000}];
        const POTION_RECIPES = [{herb: "Clean guam", potion: "Guam potion (unf)", limit: 10000}, {herb: "Clean ranarr", potion: "Ranarr potion (unf)", limit: 10000}, {herb: "Clean snapdragon", potion: "Snapdragon potion (unf)", limit: 10000}, {herb: "Clean torstol", potion: "Torstol potion (unf)", limit: 10000}];
        const DISASSEMBLE_RECIPES = [{item: "Maple logs", output: "Empty divine charge", parts_needed: 20, yield_rate: 0.50, limit: 25000}, {item: "Magic logs", output: "Empty divine charge", parts_needed: 20, yield_rate: 0.50, limit: 25000}, {item: "Silver jewelry", output: "Spring", parts_needed: 10, yield_rate: 0.30, limit: 1000}, {item: "Maple shieldbow (u)", output: "Spring", parts_needed: 10, yield_rate: 0.25, limit: 10000}, {item: "Diamond necklace", output: "Equipment siphon", parts_needed: 15, yield_rate: 0.25, limit: 10000}];
        const COMPONENT_RECIPES = [{item: "Noxious scythe", component: "Noxious components", yield: 1}, {item: "Noxious longbow", component: "Noxious components", yield: 1}, {item: "Dragon rider lance", component: "Ilujankan components", yield: 1}, {item: "Zaros godsword", component: "Ilujankan components", yield: 1}, {item: "Hand cannon", component: "Explosive components", yield: 1}];

        let state = { tab: 'Dashboard', sortBy: 'day', prices: null, itemIds: null, masterData: [] };
        let settings = { tax: true, junkTier: 0, customCharge: null, tier: 2, customAlch: [], refreshRate: 5 };
        let refreshIntervalId = null;

        function init() {
            const saved = localStorage.getItem('inv_margins_settings_v3');
            if (saved) { try { settings = { ...settings, ...JSON.parse(saved) }; } catch(e){} }
            
            document.getElementById('setting-tax').checked = settings.tax;
            document.getElementById('setting-junk').value = settings.junkTier;
            document.getElementById('setting-charge').value = settings.customCharge || '';
            document.getElementById('setting-tier').value = settings.tier;
            document.getElementById('setting-refresh').value = settings.refreshRate;
            
            // Check Offline Cache
            const cachedCache = localStorage.getItem('inv_margins_cache_v3');
            if(cachedCache) {
                try {
                    const parsed = JSON.parse(cachedCache);
                    state.prices = parsed.prices;
                    state.itemIds = parsed.itemIds;
                    calculateData();
                    document.getElementById('status-dot').className = 'status-dot cached';
                    document.getElementById('status-text').textContent = 'Using offline cache...';
                } catch(e) {}
            }
            
            fetchPrices();
            updateRefreshInterval();
        }

        function updateRefreshInterval() {
            if(refreshIntervalId) clearInterval(refreshIntervalId);
            const r = parseInt(document.getElementById('setting-refresh').value) || 0;
            settings.refreshRate = r;
            saveSettings();
            if(r > 0) refreshIntervalId = setInterval(fetchPrices, r * 60000);
        }

        function toggleSettings() { document.getElementById('settings-modal').classList.toggle('open'); }
        function saveSettings() {
            settings.tax = document.getElementById('setting-tax').checked;
            settings.junkTier = parseInt(document.getElementById('setting-junk').value) || 0;
            const chargeVal = document.getElementById('setting-charge').value;
            settings.customCharge = chargeVal ? parseInt(chargeVal) : null;
            settings.tier = parseInt(document.getElementById('setting-tier').value) || 2;
            localStorage.setItem('inv_margins_settings_v3', JSON.stringify(settings));
            if (state.prices) calculateData();
        }

        function exportConfig() {
            const str = JSON.stringify(settings);
            navigator.clipboard.writeText(str).then(() => alert("Config copied to clipboard!"));
        }

        function importConfig() {
            const str = prompt("Paste your config JSON here:");
            if(str) {
                try {
                    settings = { ...settings, ...JSON.parse(str) };
                    saveSettings();
                    init();
                    alert("Config imported successfully.");
                } catch(e) { alert("Invalid config format."); }
            }
        }

        function addCustomItem() {
            const name = document.getElementById('c-name').value;
            const alch = parseInt(document.getElementById('c-alch').value);
            if(name && alch) {
                settings.customAlch.push({name, alch, limit: 1000});
                saveSettings();
                document.getElementById('c-name').value = '';
                document.getElementById('c-alch').value = '';
                fetchPrices();
            }
        }

        function removeCustomItem(idx) { settings.customAlch.splice(idx, 1); saveSettings(); }

        function setTab(tabName) {
            state.tab = tabName;
            document.querySelectorAll('.tab').forEach(btn => {
                btn.classList.toggle('active', btn.innerText === tabName || (tabName === 'Auto Disassembler' && btn.innerText === 'Disassembler') || (tabName === 'Potion Producer' && btn.innerText === 'Potion'));
            });
            document.getElementById('tab-desc-text').innerText = tabName === 'Dashboard' ? 'Top 25 Most Profitable Items' : 
                                                            (tabName === 'Components' ? 'Implied Component Valuations' :
                                                            (tabName === 'Custom' ? 'Your Custom Items' : 'Machine Margins'));
            document.getElementById('opt-btn').style.display = tabName === 'Dashboard' ? 'flex' : 'none';
            document.getElementById('opt-panel').classList.remove('open');
            renderData();
        }

        function setSort(val) { state.sortBy = val; renderData(); }
        function formatNum(num) { return new Intl.NumberFormat('en-US').format(Math.floor(num)); }
        function getIconUrl(name, id) { if (id) return `https://secure.runescape.com/m=itemdb_rs/obj_sprite.gif?id=${id}`; return `https://runescape.wiki/images/${name.split(' -> ').pop().replace(/ /g, '_')}.png`; }
        function toggleCard(el) { el.classList.toggle('expanded'); }

        function scanBankAlt1() {
            if (window.alt1) alert("Alt1 detected! Screen scanning API hook would execute here to read your bank slots and cross-reference with the masterData array.");
            else alert("Alt1 not detected. Please open this app inside Alt1 Toolkit to use native screen reading features.");
        }

        async function drawHistory(btn, id, name) {
            btn.innerText = "Loading graph...";
            try {
                const res = await fetch(`https://api.weirdgloop.org/exchange/history/rs/last90d?id=${id}`);
                const data = await res.json();
                const series = Object.values(data)[0];
                const prices = series.map(d => d.price);
                const min = Math.min(...prices), max = Math.max(...prices);
                
                const canvas = document.createElement('canvas');
                canvas.width = 300; canvas.height = 60;
                const ctx = canvas.getContext('2d');
                ctx.strokeStyle = '#38BDF8'; ctx.lineWidth = 2;
                ctx.beginPath();
                prices.forEach((p, i) => {
                    const x = (i / (prices.length - 1)) * 300;
                    const y = 60 - ((p - min) / (max - min) * 50) - 5;
                    if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
                });
                ctx.stroke();
                
                const parent = btn.parentElement;
                parent.innerHTML = '<div style="font-size: 11px; margin-bottom: 4px; color: var(--brand);">90-Day GE Price Trend</div>';
                parent.appendChild(canvas);
            } catch(e) { btn.innerText = "Error loading history"; }
        }

        function toggleOptimizer() {
            const panel = document.getElementById('opt-panel');
            panel.classList.toggle('open');
            if (panel.classList.contains('open')) runOptimizer();
        }

        function runOptimizer() {
            const maxPower = parseInt(document.getElementById('opt-power').value) || 160;
            // Get best item per machine
            let bestPerMachine = {};
            state.masterData.forEach(d => {
                if (d.profitDay <= 0 || d.machine === "Components") return;
                if (!bestPerMachine[d.machine] || d.profitDay > bestPerMachine[d.machine].profitDay) {
                    bestPerMachine[d.machine] = d;
                }
            });
            
            const machines = Object.keys(bestPerMachine).map(k => ({
                name: k, profit: bestPerMachine[k].profitDay, power: MACHINES[k][settings.tier].power, item: bestPerMachine[k].item
            }));

            // Simple Knapsack-like approach (Since N is small, just generate combinations. Max machines = 160/20 = 8)
            let bestCombo = [];
            let maxProfit = 0;
            
            function search(idx, currentPower, currentProfit, currentCombo) {
                if (currentProfit > maxProfit) { maxProfit = currentProfit; bestCombo = [...currentCombo]; }
                if (idx >= machines.length) return;
                
                // Max multiples of this machine
                const maxMult = Math.floor((maxPower - currentPower) / machines[idx].power);
                for(let i = 0; i <= maxMult; i++) {
                    search(idx + 1, currentPower + (i * machines[idx].power), currentProfit + (i * machines[idx].profit), currentCombo.concat(Array(i).fill(machines[idx])));
                }
            }
            search(0, 0, 0, []);

            const resDiv = document.getElementById('opt-result');
            if (bestCombo.length === 0) { resDiv.innerText = "No profitable machines fit in power limit."; return; }
            
            let counts = {};
            bestCombo.forEach(m => { counts[m.name] = (counts[m.name] || 0) + 1; });
            
            let desc = `Absolute Best Setup (${maxPower} Power Max):<br>`;
            let usedPower = 0;
            Object.keys(counts).forEach(k => {
                const m = bestCombo.find(x => x.name === k);
                desc += `- ${counts[k]}x ${k} (Processing: ${m.item})<br>`;
                usedPower += counts[k] * m.power;
            });
            desc += `<br>Total Passive Profit: <strong>+${formatNum(maxProfit)} / day</strong><br>`;
            desc += `<span style="font-size:11px; color:var(--text-secondary);">Power Used: ${usedPower} / ${maxPower}</span>`;
            resDiv.innerHTML = desc;
        }

        async function fetchPrices(manual = false) {
            document.getElementById('status-dot').className = 'status-dot loading';
            document.getElementById('status-text').textContent = 'Fetching prices...';
            let names = ["Divine charge", "Empty divine charge", "Nature rune", "Vial of water", "Spring", "Equipment siphon"];
            [...DEFAULT_ALCH_ITEMS, ...settings.customAlch].forEach(i => names.push(i.name));
            PLANK_RECIPES.forEach(r => names.push(r.log, r.plank));
            TANNER_RECIPES.forEach(r => names.push(r.hide, r.leather));
            POTION_RECIPES.forEach(r => names.push(r.herb, r.potion));
            DISASSEMBLE_RECIPES.forEach(r => names.push(r.item, r.output));
            COMPONENT_RECIPES.forEach(r => names.push(r.item));
            
            let uniqueNames = [...new Set(names)];
            let newPrices = {};
            let newIds = {};
            try {
                for (let i = 0; i < uniqueNames.length; i += 40) {
                    const chunk = uniqueNames.slice(i, i + 40);
                    const url = `https://api.weirdgloop.org/exchange/history/rs/latest?name=${encodeURIComponent(chunk.join('|'))}`;
                    const res = await fetch(url);
                    const data = await res.json();
                    for (const [k, v] of Object.entries(data)) { 
                        newPrices[k.toLowerCase()] = v.price; 
                        newIds[k.toLowerCase()] = v.id;
                    }
                }
                state.prices = newPrices;
                state.itemIds = newIds;
                localStorage.setItem('inv_margins_cache_v3', JSON.stringify({prices: newPrices, itemIds: newIds}));
                calculateData();
                document.getElementById('status-dot').className = 'status-dot';
                document.getElementById('status-text').textContent = 'Live';
            } catch (err) {
                if(!state.prices) {
                    document.getElementById('status-dot').className = 'status-dot error';
                    document.getElementById('status-text').textContent = 'Error';
                }
            }
        }

        function calculateData() {
            const prices = state.prices;
            if (!prices) return;
            const tax = settings.tax ? 0.98 : 1.0;
            const junkMult = 1.0 + (settings.junkTier * 0.015);
            const liveCharge = prices["divine charge"] || 0;
            const divineCharge = settings.customCharge !== null ? settings.customCharge : liveCharge;
            const cCost = divineCharge / MACHINE_CHARGES_PER_DIVINE_CHARGE;
            const t = settings.tier;

            let master = [];

            const alchDaily = MACHINES["Alchemiser"][t].iph * 24;
            const natPrice = prices["nature rune"] || 0;
            [...DEFAULT_ALCH_ITEMS, ...settings.customAlch].forEach(i => {
                const p = prices[i.name.toLowerCase()] || 0;
                const cost = p + natPrice + (MACHINES["Alchemiser"][t].cpi * cCost);
                const prof = i.alch - cost;
                master.push({
                    machine: "Alchemiser", item: i.name, profitItem: prof, profitDay: prof * alchDaily,
                    bottleneck: (i.limit * 6) < alchDaily, limit: i.limit, iconName: i.name, iconId: state.itemIds[i.name.toLowerCase()],
                    capital: p * alchDaily, details: `Daily Capital Req: ${formatNum(p * alchDaily)}<br>Uptime: ${(MACHINES["Alchemiser"][t].cap / alchDaily).toFixed(1)} Days<br>Formula: ${formatNum(i.alch)} - ${formatNum(p)} - ${formatNum(natPrice)} - ${formatNum(MACHINES["Alchemiser"][t].cpi * cCost)}`
                });
            });

            const plankDaily = MACHINES["Plank Maker"][t].iph * 24;
            PLANK_RECIPES.forEach(r => {
                const logP = prices[r.log.toLowerCase()] || 0;
                const plankP = prices[r.plank.toLowerCase()] || 0;
                const cost = logP + r.coin_cost + (MACHINES["Plank Maker"][t].cpi * cCost);
                const prof = (plankP * tax) - cost;
                master.push({
                    machine: "Plank Maker", item: `${r.log} -> ${r.plank}`, profitItem: prof, profitDay: prof * plankDaily,
                    bottleneck: (r.limit * 6) < plankDaily, limit: r.limit, iconName: r.plank, iconId: state.itemIds[r.plank.toLowerCase()],
                    capital: (logP + r.coin_cost) * plankDaily, details: `Daily Capital Req: ${formatNum((logP + r.coin_cost) * plankDaily)}<br>Uptime: ${(MACHINES["Plank Maker"][t].cap / plankDaily).toFixed(1)} Days`
                });
            });
            
            const tannerDaily = MACHINES["Hide Tanner"][t].iph * 24;
            TANNER_RECIPES.forEach(r => {
                const hideP = prices[r.hide.toLowerCase()] || 0;
                const leaP = prices[r.leather.toLowerCase()] || 0;
                const cost = hideP + r.coin_cost + (MACHINES["Hide Tanner"][t].cpi * cCost);
                const prof = (leaP * tax) - cost;
                master.push({
                    machine: "Hide Tanner", item: `${r.hide} -> ${r.leather}`, profitItem: prof, profitDay: prof * tannerDaily,
                    bottleneck: (r.limit * 6) < tannerDaily, limit: r.limit, iconName: r.leather, iconId: state.itemIds[r.leather.toLowerCase()],
                    capital: (hideP + r.coin_cost) * tannerDaily, details: `Daily Capital Req: ${formatNum((hideP + r.coin_cost) * tannerDaily)}<br>Uptime: ${(MACHINES["Hide Tanner"][t].cap / tannerDaily).toFixed(1)} Days`
                });
            });

            const potDaily = MACHINES["Potion Producer"][t].iph * 24;
            const vialP = prices["vial of water"] || 0;
            POTION_RECIPES.forEach(r => {
                const herbP = prices[r.herb.toLowerCase()] || 0;
                const potP = prices[r.potion.toLowerCase()] || 0;
                const cost = herbP + vialP + (MACHINES["Potion Producer"][t].cpi * cCost);
                const prof = (potP * tax) - cost;
                master.push({
                    machine: "Potion Producer", item: `${r.herb} -> ${r.potion}`, profitItem: prof, profitDay: prof * potDaily,
                    bottleneck: (r.limit * 6) < potDaily, limit: r.limit, iconName: r.potion, iconId: state.itemIds[r.potion.toLowerCase()],
                    capital: (herbP + vialP) * potDaily, details: `Daily Capital Req: ${formatNum((herbP + vialP) * potDaily)}<br>Uptime: ${(MACHINES["Potion Producer"][t].cap / potDaily).toFixed(1)} Days`
                });
            });

            const disDaily = MACHINES["Auto Disassembler"][t].iph * 24;
            DISASSEMBLE_RECIPES.forEach(r => {
                const itemP = prices[r.item.toLowerCase()] || 0;
                const prodP = prices[r.output.toLowerCase()] || 0;
                const itemsNeeded = r.parts_needed / (r.yield_rate * junkMult);
                const mCost = MACHINES["Auto Disassembler"][t].cpi * cCost;
                const profPerProd = (prodP * tax) - (itemsNeeded * (itemP + mCost));
                const prodHr = MACHINES["Auto Disassembler"][t].iph / itemsNeeded;
                const profHr = prodHr * profPerProd;
                master.push({
                    machine: "Auto Disassembler", item: `${r.item} -> ${r.output}`, profitItem: profPerProd, profitDay: profHr * 24,
                    bottleneck: (r.limit * 6) < (disDaily * itemsNeeded), limit: r.limit, iconName: r.output, iconId: state.itemIds[r.output.toLowerCase()],
                    capital: itemP * (disDaily * itemsNeeded), details: `Daily Capital Req: ${formatNum(itemP * (disDaily * itemsNeeded))}<br>Uptime: ${(MACHINES["Auto Disassembler"][t].cap / (disDaily * itemsNeeded)).toFixed(1)} Days`
                });
            });

            COMPONENT_RECIPES.forEach(r => {
                const itemP = prices[r.item.toLowerCase()] || 0;
                const compVal = itemP / r.yield;
                master.push({
                    machine: "Components", item: `${r.item} -> ${r.component}`, profitItem: compVal, profitDay: 0,
                    bottleneck: false, limit: 10, iconName: r.component, iconId: null,
                    capital: itemP, details: `Implied Value: ${formatNum(itemP)} / ${r.yield} = ${formatNum(compVal)}`
                });
            });

            state.masterData = master;
            renderData();
        }

        function renderData() {
            const container = document.getElementById('cards-container');
            container.innerHTML = '';
            
            if(state.tab === 'Custom') {
                container.innerHTML = '<div style="margin-bottom:15px; color:var(--text-secondary);">Your custom Alchemiser items. Check Dashboard for profits.</div>';
                settings.customAlch.forEach((c, idx) => {
                    const d = document.createElement('div');
                    d.className = 'card';
                    d.innerHTML = `<div class="card-header"><div><strong>${c.name}</strong> (Alch: ${c.alch})</div><button class="icon-btn" onclick="removeCustomItem(${idx})">🗑️</button></div>`;
                    container.appendChild(d);
                });
                return;
            }

            let data = state.masterData;
            if (state.tab !== 'Dashboard') data = data.filter(d => d.machine === state.tab);

            if (state.sortBy === 'day') data.sort((a, b) => b.profitDay - a.profitDay);
            else data.sort((a, b) => b.profitItem - a.profitItem);

            if (state.tab === 'Dashboard') data = data.slice(0, 25);

            if (data.length === 0) {
                container.innerHTML = `<div class="loader-wrapper"><div>No data available.</div></div>`;
                return;
            }

            data.forEach((row, idx) => {
                const card = document.createElement('div');
                card.className = 'card';
                card.setAttribute('onclick', 'toggleCard(this)');
                const isPos = row.profitDay >= 0 || row.machine === "Components";
                const bTag = row.bottleneck ? `<span class="tag bottleneck">⚠️ Buy Limit: ${row.limit}</span>` : `<span class="tag">Limit: ${row.limit}</span>`;
                const mTag = state.tab === 'Dashboard' ? `<span class="tag">${row.machine}</span>` : '';
                const historyBtn = row.iconId ? `<div><button class="history-btn" onclick="event.stopPropagation(); drawHistory(this, ${row.iconId}, '${row.item}')">📉 Load 90d Chart</button></div>` : '';

                card.innerHTML = `
                    <div class="card-header">
                        <div class="card-left">
                            <img class="item-icon" src="${getIconUrl(row.iconName, row.iconId)}" onerror="this.style.opacity='0'">
                            <div class="item-info">
                                <div class="item-name">${state.tab === 'Dashboard' ? '#' + (idx+1) + ' ' : ''}${row.item}</div>
                                <div class="tags">${mTag}${bTag}</div>
                            </div>
                        </div>
                        <div class="card-right">
                            <div class="profit-day ${isPos ? 'positive' : 'negative'}">
                                ${row.machine === "Components" ? '' : (isPos ? '+' : '')}${formatNum(row.machine === "Components" ? row.profitItem : row.profitDay)}${row.machine === "Components" ? '' : ' / day'}
                            </div>
                            <div class="profit-ea">${row.machine === "Components" ? 'per component' : formatNum(row.profitItem) + ' ea'}</div>
                        </div>
                    </div>
                    <div class="card-details">
                        ${row.details}
                        ${historyBtn}
                    </div>
                `;
                container.appendChild(card);
            });
        }

        window.onload = init;
    </script>
</body>
</html>"""

with open(r"C:\Users\danie\Documents\invention_machines\alt1\index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
