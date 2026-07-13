import os

filepath = r"C:\Users\danie\Documents\invention_machines\alt1\index.html"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Modal UI
old_modal = """            <h3>Add Custom Item</h3>
            <div style="display:flex; gap:10px; margin-top:10px;">
                <input type="text" id="c-name" class="form-input" placeholder="Item Name" style="width: 100%;">
                <input type="number" id="c-alch" class="form-input" placeholder="Alch Val">
            </div>"""

new_modal = """            <h3>Add Custom Item</h3>
            <div style="position:relative;">
                <input type="text" id="wiki-search" class="form-input" placeholder="🔍 Search RS Wiki for item..." style="width: 100%; margin-top:10px;" oninput="searchWiki(this.value)">
                <div id="wiki-dropdown" style="position:absolute; top:100%; left:0; right:0; background:#1E293B; border:1px solid var(--border); border-radius:6px; max-height:150px; overflow-y:auto; display:none; z-index:1000;"></div>
            </div>
            <div style="font-size:12px; color:var(--text-secondary); margin-top:8px; text-align:center;">OR enter manually below:</div>
            <div style="display:flex; gap:10px; margin-top:10px;">
                <input type="text" id="c-name" class="form-input" placeholder="Item Name" style="width: 100%;">
                <input type="number" id="c-alch" class="form-input" placeholder="Alch Val">
            </div>"""

content = content.replace(old_modal, new_modal)

# 2. Add Javascript Logic
js_to_add = """        let wikiSearchTimeout = null;
        async function searchWiki(query) {
            const dropdown = document.getElementById('wiki-dropdown');
            if(query.length < 3) { dropdown.style.display = 'none'; return; }
            if(wikiSearchTimeout) clearTimeout(wikiSearchTimeout);
            wikiSearchTimeout = setTimeout(async () => {
                try {
                    const res = await fetch(`https://runescape.wiki/api.php?action=opensearch&search=${encodeURIComponent(query)}&format=json&origin=*`);
                    const data = await res.json();
                    const items = data[1];
                    if(items.length > 0) {
                        dropdown.innerHTML = items.map(item => `<div style="padding:8px 12px; cursor:pointer; border-bottom:1px solid var(--border);" onmouseover="this.style.background='rgba(56,189,248,0.1)'" onmouseout="this.style.background='transparent'" onclick="selectWikiItem('${item.replace(/'/g, "\\\\'")}')">${item}</div>`).join('');
                        dropdown.style.display = 'block';
                    } else {
                        dropdown.style.display = 'none';
                    }
                } catch(e) {}
            }, 300);
        }

        async function selectWikiItem(name) {
            document.getElementById('wiki-dropdown').style.display = 'none';
            document.getElementById('wiki-search').value = name;
            document.getElementById('c-name').value = name;
            document.getElementById('c-alch').placeholder = 'Fetching...';
            try {
                const res = await fetch(`https://runescape.wiki/api.php?action=parse&page=${encodeURIComponent(name)}&prop=wikitext&format=json&origin=*`);
                const data = await res.json();
                const wikitext = data.parse.wikitext['*'];
                const match = wikitext.match(/\\|\\s*value\\s*=\\s*(\\d+)/i);
                if(match && match[1]) {
                    const val = parseInt(match[1]);
                    document.getElementById('c-alch').value = Math.floor(val * 0.6);
                    document.getElementById('c-alch').placeholder = 'Alch Val';
                } else {
                    document.getElementById('c-alch').placeholder = 'Alch Val';
                    alert("Could not find High Alch value for this item. Please enter it manually.");
                }
            } catch(e) {
                document.getElementById('c-alch').placeholder = 'Alch Val';
            }
        }

        function addCustomItem() {"""

content = content.replace("        function addCustomItem() {", js_to_add)

# 3. Add clearing search input when adding custom item
old_add = """                document.getElementById('c-name').value = '';
                document.getElementById('c-alch').value = '';"""

new_add = """                document.getElementById('c-name').value = '';
                document.getElementById('c-alch').value = '';
                document.getElementById('wiki-search').value = '';"""

content = content.replace(old_add, new_add)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
