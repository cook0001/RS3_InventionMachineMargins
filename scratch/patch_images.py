import os

filepath = r"C:\Users\danie\Documents\invention_machines\alt1\index.html"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update state
content = content.replace("let state = { tab: 'Dashboard', sortBy: 'day', prices: null, masterData: [] };",
                          "let state = { tab: 'Dashboard', sortBy: 'day', prices: null, itemIds: null, masterData: [] };")

# 2. Update getWikiIconUrl
content = content.replace("function getWikiIconUrl(name) { return `https://runescape.wiki/images/${name.split(' -> ').pop().replace(/ /g, '_')}.png`; }",
                          "function getIconUrl(name, id) { if (id) return `https://secure.runescape.com/m=itemdb_rs/obj_sprite.gif?id=${id}`; return `https://runescape.wiki/images/${name.split(' -> ').pop().replace(/ /g, '_')}.png`; }")

# 3. Update fetchPrices
old_fetch = """            let newPrices = {};
            try {
                for (let i = 0; i < uniqueNames.length; i += 40) {
                    const chunk = uniqueNames.slice(i, i + 40);
                    const url = `https://api.weirdgloop.org/exchange/history/rs/latest?name=${encodeURIComponent(chunk.join('|'))}`;
                    const res = await fetch(url);
                    const data = await res.json();
                    for (const [k, v] of Object.entries(data)) { newPrices[k.toLowerCase()] = v.price; }
                }
                state.prices = newPrices;"""

new_fetch = """            let newPrices = {};
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
                state.itemIds = newIds;"""

content = content.replace(old_fetch, new_fetch)

# 4. Update calculateData
content = content.replace("iconName: i.name,", "iconName: i.name, iconId: state.itemIds[i.name.toLowerCase()],")
content = content.replace("iconName: r.plank,", "iconName: r.plank, iconId: state.itemIds[r.plank.toLowerCase()],")
content = content.replace("iconName: r.leather,", "iconName: r.leather, iconId: state.itemIds[r.leather.toLowerCase()],")
content = content.replace("iconName: r.potion,", "iconName: r.potion, iconId: state.itemIds[r.potion.toLowerCase()],")
content = content.replace("iconName: r.output,", "iconName: r.output, iconId: state.itemIds[r.output.toLowerCase()],")
content = content.replace("iconName: r.component,", "iconName: r.component, iconId: null,")

# 5. Update renderData
content = content.replace("getWikiIconUrl(row.iconName)", "getIconUrl(row.iconName, row.iconId)")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
