import './style.css'
import { ITEM_DATA, fetchLivePrices } from './items.js';

// App State
let settings = JSON.parse(localStorage.getItem('inventionSettings')) || {
  divineChargeCost: 0,
  machineTier: 1 // 1=Base, 2=MK II
};

let customItems = JSON.parse(localStorage.getItem('inventionCustomItems')) || {
  alchemiser: [],
  disassembler: [],
  plankmaker: [],
  tanner: []
};

let livePrices = {};
let searchQuery = "";
let sortMode = "profit";

// DOM Elements
const tabs = document.querySelectorAll('.tab');
const panels = document.querySelectorAll('.machine-panel');
const searchInput = document.getElementById('search-input');
const sortSelect = document.getElementById('sort-select');

// Modals
const customModal = document.getElementById('custom-modal');
const settingsModal = document.getElementById('settings-modal');

// Init
async function init() {
  setupEventListeners();
  
  // Try Alt1 Check
  if (window.alt1) {
    console.log("Alt1 Detected");
  }

  // Fetch prices
  const data = await fetchLivePrices();
  if (data) {
    // Map response to simple ID -> price
    Object.keys(data).forEach(id => {
      livePrices[id] = data[id].price;
    });
  } else {
    alert("Failed to fetch live GE prices. Check console.");
  }
  
  renderAllTables();
}

function getMachineChargeCost(machineId) {
  // Charge drains per hour vs items per hour.
  // Rough estimate per item processed:
  const chargePrice = settings.divineChargeCost > 0 ? settings.divineChargeCost : (livePrices['33415'] || 100000);
  const costPerChargeUnit = chargePrice / 3000; 
  
  // Very simplified charge drain per item
  let baseDrain = 0;
  if (machineId === 'alchemiser') baseDrain = 60; 
  if (machineId === 'disassembler') baseDrain = 60;
  if (machineId === 'plankmaker') baseDrain = 90;
  if (machineId === 'tanner') baseDrain = 60;
  
  // Tier 2 (MK II) is often more efficient or processes more
  const efficiency = settings.machineTier == 2 ? 0.8 : 1.0; 
  
  return Math.floor(costPerChargeUnit * baseDrain * efficiency);
}

function compileData(machineId) {
  let items = [];
  
  // Custom items
  customItems[machineId].forEach(c => {
    items.push({
      name: c.name,
      buyPrice: c.buyPrice,
      valueOut: c.valueOut,
      costs: (machineId === 'alchemiser' || machineId === 'plankmaker') ? (livePrices['561'] || 300) : 0,
      custom: true
    });
  });

  // Database items
  Object.keys(ITEM_DATA).forEach(id => {
    const item = ITEM_DATA[id];
    if (item.category === machineId) {
      const buyPrice = livePrices[id] || 0;
      let valueOut = 0;
      let costs = 0;

      if (machineId === 'alchemiser') {
        valueOut = item.alchValue;
        costs = livePrices['561'] || 0; // Nature rune
      } 
      else if (machineId === 'disassembler') {
        valueOut = item.expectedValue;
      }
      else if (machineId === 'plankmaker') {
        valueOut = livePrices[item.outputs] || 0;
        costs = livePrices['561'] || 0; // Assuming some coins cost but let's use nat price for simple mock
      }
      else if (machineId === 'tanner') {
        valueOut = livePrices[item.outputs] || 0;
      }
      
      items.push({ name: item.name, buyPrice, valueOut, costs, custom: false });
    }
  });

  return items;
}

function formatNumber(num) {
  return new Intl.NumberFormat('en-US').format(num);
}

function renderTable(machineId) {
  const tbody = document.querySelector(`#${machineId}-table tbody`);
  if (!tbody) return;
  tbody.innerHTML = '';
  
  const chargeCost = getMachineChargeCost(machineId);
  let items = compileData(machineId);

  // Filter
  if (searchQuery) {
    items = items.filter(i => i.name.toLowerCase().includes(searchQuery.toLowerCase()));
  }

  // Sort
  items.sort((a, b) => {
    const profitA = a.valueOut - a.buyPrice - a.costs - chargeCost;
    const profitB = b.valueOut - b.buyPrice - b.costs - chargeCost;
    
    if (sortMode === 'profit') {
      return profitB - profitA;
    } else {
      // ROI
      const roiA = a.buyPrice > 0 ? (profitA / a.buyPrice) : 0;
      const roiB = b.buyPrice > 0 ? (profitB / b.buyPrice) : 0;
      return roiB - roiA;
    }
  });

  items.slice(0, 50).forEach(item => {
    const totalCosts = item.costs + chargeCost;
    const profit = item.valueOut - item.buyPrice - totalCosts;
    const profitClass = profit >= 0 ? 'profit-positive' : 'profit-negative';
    const roi = item.buyPrice > 0 ? ((profit / item.buyPrice) * 100).toFixed(1) : 0;
    
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>
        <div class="item-name">
          <div class="item-icon">${item.custom ? '⭐' : '📦'}</div>
          ${item.name}
        </div>
      </td>
      <td>${formatNumber(item.buyPrice)}</td>
      <td>${formatNumber(item.valueOut)}</td>
      <td>${formatNumber(totalCosts)}</td>
      <td class="${profitClass}">${profit > 0 ? '+' : ''}${formatNumber(profit)}</td>
      <td class="${profitClass}">${roi}%</td>
    `;
    tbody.appendChild(tr);
  });
}

function renderAllTables() {
  renderTable('alchemiser');
  renderTable('disassembler');
  renderTable('plankmaker');
  renderTable('tanner');
}

function setupEventListeners() {
  // Tabs
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      panels.forEach(p => p.classList.remove('active'));
      tab.classList.add('active');
      document.getElementById(tab.dataset.target).classList.add('active');
    });
  });

  // Search & Sort
  searchInput.addEventListener('input', (e) => {
    searchQuery = e.target.value;
    renderAllTables();
  });
  sortSelect.addEventListener('change', (e) => {
    sortMode = e.target.value;
    renderAllTables();
  });

  // Modals Open/Close
  document.getElementById('add-custom-btn').addEventListener('click', () => customModal.classList.remove('hidden'));
  document.getElementById('close-custom').addEventListener('click', () => customModal.classList.add('hidden'));
  document.getElementById('settings-btn').addEventListener('click', () => {
    document.getElementById('divine-charge-cost').value = settings.divineChargeCost;
    document.getElementById('machine-tier').value = settings.machineTier;
    settingsModal.classList.remove('hidden');
  });
  document.getElementById('close-settings').addEventListener('click', () => settingsModal.classList.add('hidden'));

  // Form Submits
  document.getElementById('custom-item-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const machine = document.getElementById('machine-select').value;
    customItems[machine].push({
      name: document.getElementById('item-name').value,
      buyPrice: parseInt(document.getElementById('buy-price').value, 10),
      valueOut: parseInt(document.getElementById('value-out').value, 10),
    });
    localStorage.setItem('inventionCustomItems', JSON.stringify(customItems));
    e.target.reset();
    customModal.classList.add('hidden');
    renderAllTables();
  });

  document.getElementById('settings-form').addEventListener('submit', (e) => {
    e.preventDefault();
    settings.divineChargeCost = parseInt(document.getElementById('divine-charge-cost').value, 10) || 0;
    settings.machineTier = parseInt(document.getElementById('machine-tier').value, 10) || 1;
    localStorage.setItem('inventionSettings', JSON.stringify(settings));
    settingsModal.classList.add('hidden');
    renderAllTables();
  });

  // Export / Import
  document.getElementById('export-btn').addEventListener('click', () => {
    const data = btoa(JSON.stringify({ customItems, settings }));
    navigator.clipboard.writeText(data).then(() => alert("Data exported to clipboard!"));
  });
  document.getElementById('import-btn').addEventListener('click', () => {
    const data = prompt("Paste your exported string here:");
    if (data) {
      try {
        const parsed = JSON.parse(atob(data));
        if (parsed.customItems) customItems = parsed.customItems;
        if (parsed.settings) settings = parsed.settings;
        localStorage.setItem('inventionCustomItems', JSON.stringify(customItems));
        localStorage.setItem('inventionSettings', JSON.stringify(settings));
        renderAllTables();
        alert("Import successful!");
      } catch (err) {
        alert("Invalid import data.");
      }
    }
  });

  // Alt1 Scan Bank Placeholder
  document.getElementById('alt1-btn').addEventListener('click', () => {
    if (window.alt1) {
      alt1.overLaySetGroup('inventionMargins');
      alt1.overLayTextEx('Scan feature coming soon! Bank reading requires image sprite mapping.', 
        alt1.rsWidth/2, alt1.rsHeight/2, 20, 0xFFFFFF, 3000);
    } else {
      alert("Alt1 not detected. Open this app inside the Alt1 Toolkit browser.");
    }
  });
}

init();
