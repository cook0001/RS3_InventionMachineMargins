export const ITEM_DATA = {
  // Runes & Energy
  561: { name: 'Nature rune', type: 'resource' },
  33415: { name: 'Divine charge', type: 'resource' },
  
  // Alchemiser items (ID: { name, alchValue })
  1127: { name: 'Rune platebody', alchValue: 39000, category: 'alchemiser' },
  1123: { name: 'Adamant platebody', alchValue: 9984, category: 'alchemiser' },
  1079: { name: 'Rune platelegs', alchValue: 38400, category: 'alchemiser' },
  1093: { name: 'Rune plateskirt', alchValue: 38400, category: 'alchemiser' },
  1303: { name: 'Rune longsword', alchValue: 19200, category: 'alchemiser' },
  1319: { name: 'Rune 2h sword', alchValue: 38400, category: 'alchemiser' },
  1113: { name: 'Rune chainbody', alchValue: 30000, category: 'alchemiser' },
  1147: { name: 'Rune med helm', alchValue: 11520, category: 'alchemiser' },
  1163: { name: 'Rune full helm', alchValue: 21120, category: 'alchemiser' },
  1201: { name: 'Rune kite shield', alchValue: 32640, category: 'alchemiser' },
  1373: { name: 'Rune battleaxe', alchValue: 24960, category: 'alchemiser' },
  1432: { name: 'Rune mace', alchValue: 8640, category: 'alchemiser' },
  2361: { name: 'Adamantite bar', alchValue: 1080, category: 'alchemiser' },
  2363: { name: 'Runite bar', alchValue: 3000, category: 'alchemiser' },

  // Plank Maker (id: { name, outputs: plankId })
  1511: { name: 'Logs', category: 'plankmaker', outputs: 960 },
  1521: { name: 'Oak logs', category: 'plankmaker', outputs: 8778 },
  6333: { name: 'Teak logs', category: 'plankmaker', outputs: 8780 },
  6332: { name: 'Mahogany logs', category: 'plankmaker', outputs: 8782 },
  
  960: { name: 'Plank', type: 'output' },
  8778: { name: 'Oak plank', type: 'output' },
  8780: { name: 'Teak plank', type: 'output' },
  8782: { name: 'Mahogany plank', type: 'output' },

  // Hide Tanner (id: { name, outputs: leatherId })
  1753: { name: 'Green dragonhide', category: 'tanner', outputs: 1745 },
  1751: { name: 'Blue dragonhide', category: 'tanner', outputs: 2505 },
  1749: { name: 'Red dragonhide', category: 'tanner', outputs: 2507 },
  1747: { name: 'Black dragonhide', category: 'tanner', outputs: 2509 },
  24372: { name: 'Royal dragonhide', category: 'tanner', outputs: 24374 },

  1745: { name: 'Green dragon leather', type: 'output' },
  2505: { name: 'Blue dragon leather', type: 'output' },
  2507: { name: 'Red dragon leather', type: 'output' },
  2509: { name: 'Black dragon leather', type: 'output' },
  24374: { name: 'Royal dragon leather', type: 'output' },
  
  // Disassembler (id: { name, valueOut }) -> valueOut is manual estimate of parts value
  1519: { name: 'Willow logs', category: 'disassembler', expectedValue: 350 },
  1517: { name: 'Maple logs', category: 'disassembler', expectedValue: 480 },
  1515: { name: 'Yew logs', category: 'disassembler', expectedValue: 550 },
  1513: { name: 'Magic logs', category: 'disassembler', expectedValue: 800 },
};

export async function fetchLivePrices() {
  const ids = Object.keys(ITEM_DATA).join('|');
  try {
    const res = await fetch(`https://api.weirdgloop.org/exchange/history/rs/latest?id=${ids}`);
    const data = await res.json();
    return data;
  } catch (err) {
    console.error('Failed to fetch live prices', err);
    return null;
  }
}
