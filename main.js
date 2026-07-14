import './style.css'

// Mock Data for the demonstration of the premium UI and functionality.
// In a real application, this would fetch from a database or Runescape GE API.
const initialData = {
  alchemiser: Array.from({ length: 25 }, (_, i) => ({
    id: `alch-${i}`,
    name: `Rune item ${i + 1}`,
    buyPrice: 35000 - i * 100,
    valueOut: 38400 - i * 100,
    costItem: 300 // nature rune
  })),
  disassembler: Array.from({ length: 25 }, (_, i) => ({
    id: `dis-${i}`,
    name: `Maple logs ${i + 1}`,
    buyPrice: 150 + i * 5,
    valueOut: 450 - i * 5,
    costItem: 0
  })),
  plankmaker: Array.from({ length: 25 }, (_, i) => ({
    id: `plank-${i}`,
    name: `Mahogany logs ${i + 1}`,
    buyPrice: 1500 - i * 10,
    valueOut: 2200 - i * 10,
    costItem: 0
  })),
  tanner: Array.from({ length: 25 }, (_, i) => ({
    id: `tan-${i}`,
    name: `Royal dragonhide ${i + 1}`,
    buyPrice: 2800 - i * 20,
    valueOut: 3500 - i * 20,
    costItem: 0
  }))
};

// State
let appData = JSON.parse(localStorage.getItem('inventionMargins')) || initialData;

// DOM Elements
const tabs = document.querySelectorAll('.tab');
const panels = document.querySelectorAll('.machine-panel');
const modal = document.getElementById('custom-modal');
const addBtn = document.getElementById('add-custom-btn');
const closeBtn = document.getElementById('close-modal');
const form = document.getElementById('custom-item-form');

// Initialization
function init() {
  renderAllTables();
  setupEventListeners();
}

function saveState() {
  localStorage.setItem('inventionMargins', JSON.stringify(appData));
  renderAllTables();
}

function formatNumber(num) {
  return new Intl.NumberFormat('en-US').format(num);
}

function renderTable(machineId) {
  const tbody = document.querySelector(`#${machineId}-table tbody`);
  if (!tbody) return;
  
  tbody.innerHTML = '';
  
  // Sort by profit descending
  const items = [...appData[machineId]].sort((a, b) => {
    const profitA = a.valueOut - a.buyPrice - (a.costItem || 0);
    const profitB = b.valueOut - b.buyPrice - (b.costItem || 0);
    return profitB - profitA;
  }).slice(0, 25); // Top 25

  items.forEach(item => {
    const profit = item.valueOut - item.buyPrice - (item.costItem || 0);
    const profitClass = profit >= 0 ? 'profit-positive' : 'profit-negative';
    
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>
        <div class="item-name">
          <div class="item-icon">📦</div>
          ${item.name}
        </div>
      </td>
      <td>${formatNumber(item.buyPrice)}</td>
      <td>${formatNumber(item.valueOut)}</td>
      ${item.costItem !== undefined && machineId === 'alchemiser' ? `<td>${formatNumber(item.costItem)}</td>` : ''}
      <td class="${profitClass}">${profit > 0 ? '+' : ''}${formatNumber(profit)}</td>
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
      const target = document.getElementById(tab.dataset.target);
      if(target) target.classList.add('active');
    });
  });

  // Modal
  addBtn.addEventListener('click', () => {
    modal.classList.remove('hidden');
  });

  closeBtn.addEventListener('click', () => {
    modal.classList.add('hidden');
  });

  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.classList.add('hidden');
    }
  });

  // Form Submit
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const machine = document.getElementById('machine-select').value;
    const name = document.getElementById('item-name').value;
    const buyPrice = parseInt(document.getElementById('buy-price').value, 10);
    const valueOut = parseInt(document.getElementById('value-out').value, 10);
    
    const newItem = {
      id: `custom-${Date.now()}`,
      name,
      buyPrice,
      valueOut,
      costItem: machine === 'alchemiser' ? 300 : 0 // Simplified mock nature rune price
    };

    appData[machine].push(newItem);
    saveState();
    
    form.reset();
    modal.classList.add('hidden');
  });
}

// Boot
init();
