import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import urllib.parse
import json
import threading
import os
import time
import ctypes

try:
    myappid = 'rs3.invention.profit.calc.premium'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

try:
    import sv_ttk
    HAS_SV_TTK = True
except ImportError:
    HAS_SV_TTK = False

MACHINE_CHARGES_PER_DIVINE_CHARGE = 3000
ALCHEMISER_ITEMS_PER_HOUR = 25
ALCHEMISER_MACHINE_CHARGES_PER_HOUR = 150
ALCH_CHARGES_PER_ITEM = ALCHEMISER_MACHINE_CHARGES_PER_HOUR / ALCHEMISER_ITEMS_PER_HOUR

PLANK_MAKER_ITEMS_PER_HOUR = 40
PLANK_MAKER_MACHINE_CHARGES_PER_HOUR = 600
PLANK_CHARGES_PER_ITEM = PLANK_MAKER_MACHINE_CHARGES_PER_HOUR / PLANK_MAKER_ITEMS_PER_HOUR

DISASSEMBLER_ITEMS_PER_HOUR = 35
DISASSEMBLER_MACHINE_CHARGES_PER_HOUR = 180
DISASSEMBLER_CHARGES_PER_ITEM = DISASSEMBLER_MACHINE_CHARGES_PER_HOUR / DISASSEMBLER_ITEMS_PER_HOUR

TANNER_ITEMS_PER_HOUR = 140
TANNER_MACHINE_CHARGES_PER_HOUR = 225
TANNER_CHARGES_PER_ITEM = TANNER_MACHINE_CHARGES_PER_HOUR / TANNER_ITEMS_PER_HOUR

POTION_ITEMS_PER_HOUR = 40
POTION_MACHINE_CHARGES_PER_HOUR = 210
POTION_CHARGES_PER_ITEM = POTION_MACHINE_CHARGES_PER_HOUR / POTION_ITEMS_PER_HOUR

DEFAULT_ALCH_ITEMS = [
    {"name": "Huge bladed rune salvage", "alch": 40000, "limit": 100},
    {"name": "Huge plated rune salvage", "alch": 40000, "limit": 100},
    {"name": "Huge blunt rune salvage", "alch": 40000, "limit": 100},
    {"name": "Huge bladed orikalkum salvage", "alch": 60000, "limit": 100},
    {"name": "Huge plated orikalkum salvage", "alch": 60000, "limit": 100},
    {"name": "Huge blunt orikalkum salvage", "alch": 60000, "limit": 100},
    {"name": "Huge bladed necronium salvage", "alch": 80000, "limit": 100},
    {"name": "Huge plated necronium salvage", "alch": 80000, "limit": 100},
    {"name": "Huge blunt necronium salvage", "alch": 80000, "limit": 100},
    {"name": "Large bladed rune salvage", "alch": 16000, "limit": 1000},
    {"name": "Large plated rune salvage", "alch": 16000, "limit": 1000},
    {"name": "Large blunt rune salvage", "alch": 16000, "limit": 1000},
    {"name": "Dragon halberd", "alch": 150000, "limit": 10},
    {"name": "Dragon 2h sword", "alch": 78000, "limit": 10},
    {"name": "Dragon battleaxe", "alch": 120000, "limit": 10},
    {"name": "Onyx bolts (e)", "alch": 5400, "limit": 10000},
    {"name": "Hydrix bolts (e)", "alch": 6000, "limit": 10000},
    {"name": "Ascendri bolts (e)", "alch": 6000, "limit": 10000},
    {"name": "Rune 2h sword", "alch": 38400, "limit": 100},
    {"name": "Rune platebody", "alch": 39000, "limit": 100},
    {"name": "Fire battlestaff", "alch": 9300, "limit": 100},
    {"name": "Water battlestaff", "alch": 9300, "limit": 100},
    {"name": "Mystic air staff", "alch": 25500, "limit": 100},
    {"name": "Mystic water staff", "alch": 25500, "limit": 100},
    {"name": "Grifolic wand", "alch": 5000, "limit": 5000},
]

PLANK_RECIPES = [
    {"log": "Logs", "plank": "Plank", "coin_cost": 100, "limit": 10000},
    {"log": "Oak logs", "plank": "Oak plank", "coin_cost": 250, "limit": 10000},
    {"log": "Teak logs", "plank": "Teak plank", "coin_cost": 500, "limit": 10000},
    {"log": "Mahogany logs", "plank": "Mahogany plank", "coin_cost": 1500, "limit": 10000},
]

TANNER_RECIPES = [
    {"hide": "Green dragonhide", "leather": "Green dragon leather", "coin_cost": 20, "limit": 10000},
    {"hide": "Blue dragonhide", "leather": "Blue dragon leather", "coin_cost": 20, "limit": 10000},
    {"hide": "Red dragonhide", "leather": "Red dragon leather", "coin_cost": 20, "limit": 10000},
    {"hide": "Black dragonhide", "leather": "Black dragon leather", "coin_cost": 20, "limit": 10000},
    {"hide": "Royal dragonhide", "leather": "Royal dragon leather", "coin_cost": 20, "limit": 10000},
    {"hide": "Dinosaurhide", "leather": "Dinosaur leather", "coin_cost": 20, "limit": 10000},
]

POTION_RECIPES = [
    {"herb": "Clean guam", "potion": "Guam potion (unf)", "limit": 10000},
    {"herb": "Clean tarromin", "potion": "Tarromin potion (unf)", "limit": 10000},
    {"herb": "Clean marrentill", "potion": "Marrentill potion (unf)", "limit": 10000},
    {"herb": "Clean harralander", "potion": "Harralander potion (unf)", "limit": 10000},
    {"herb": "Clean ranarr", "potion": "Ranarr potion (unf)", "limit": 10000},
    {"herb": "Clean toadflax", "potion": "Toadflax potion (unf)", "limit": 10000},
    {"herb": "Clean irit", "potion": "Irit potion (unf)", "limit": 10000},
    {"herb": "Clean avantoe", "potion": "Avantoe potion (unf)", "limit": 10000},
    {"herb": "Clean kwuarm", "potion": "Kwuarm potion (unf)", "limit": 10000},
    {"herb": "Clean snapdragon", "potion": "Snapdragon potion (unf)", "limit": 10000},
    {"herb": "Clean cadantine", "potion": "Cadantine potion (unf)", "limit": 10000},
    {"herb": "Clean lantadyme", "potion": "Lantadyme potion (unf)", "limit": 10000},
    {"herb": "Clean dwarf weed", "potion": "Dwarf weed potion (unf)", "limit": 10000},
    {"herb": "Clean torstol", "potion": "Torstol potion (unf)", "limit": 10000},
    {"herb": "Clean bloodweed", "potion": "Bloodweed potion (unf)", "limit": 10000},
    {"herb": "Clean arbuck", "potion": "Arbuck potion (unf)", "limit": 10000},
    {"herb": "Clean fellstalk", "potion": "Fellstalk potion (unf)", "limit": 10000},
]

DISASSEMBLE_RECIPES = [
    {"item": "Maple logs", "output": "Empty divine charge", "parts_needed": 20, "yield_rate": 0.50, "limit": 25000},
    {"item": "Acadia logs", "output": "Empty divine charge", "parts_needed": 20, "yield_rate": 0.50, "limit": 10000},
    {"item": "Yew logs", "output": "Empty divine charge", "parts_needed": 20, "yield_rate": 0.50, "limit": 25000},
    {"item": "Magic logs", "output": "Empty divine charge", "parts_needed": 20, "yield_rate": 0.50, "limit": 25000},
    {"item": "Elder logs", "output": "Empty divine charge", "parts_needed": 20, "yield_rate": 0.50, "limit": 25000},
    {"item": "Gold bar", "output": "Empty divine charge", "parts_needed": 20, "yield_rate": 0.90, "limit": 10000},
    {"item": "Harralander tar", "output": "Empty divine charge", "parts_needed": 20, "yield_rate": 0.80, "limit": 10000},
    {"item": "Silver jewelry", "output": "Spring", "parts_needed": 10, "yield_rate": 0.30, "limit": 1000}, 
    {"item": "Maple shortbow (u)", "output": "Spring", "parts_needed": 10, "yield_rate": 0.25, "limit": 10000},
    {"item": "Yew shortbow (u)", "output": "Spring", "parts_needed": 10, "yield_rate": 0.25, "limit": 10000},
    {"item": "Magic shortbow (u)", "output": "Spring", "parts_needed": 10, "yield_rate": 0.25, "limit": 10000},
    {"item": "Maple shieldbow (u)", "output": "Spring", "parts_needed": 10, "yield_rate": 0.25, "limit": 10000},
    {"item": "Yew shieldbow (u)", "output": "Spring", "parts_needed": 10, "yield_rate": 0.25, "limit": 10000},
    {"item": "Magic shieldbow (u)", "output": "Spring", "parts_needed": 10, "yield_rate": 0.25, "limit": 10000},
    {"item": "Maple shortbow", "output": "Spring", "parts_needed": 10, "yield_rate": 0.30, "limit": 10000},
    {"item": "Yew shortbow", "output": "Spring", "parts_needed": 10, "yield_rate": 0.30, "limit": 10000},
    {"item": "Magic shortbow", "output": "Spring", "parts_needed": 10, "yield_rate": 0.30, "limit": 10000},
    {"item": "Maple shieldbow", "output": "Spring", "parts_needed": 10, "yield_rate": 0.30, "limit": 10000},
    {"item": "Yew shieldbow", "output": "Spring", "parts_needed": 10, "yield_rate": 0.30, "limit": 10000},
    {"item": "Magic shieldbow", "output": "Spring", "parts_needed": 10, "yield_rate": 0.30, "limit": 10000},
    {"item": "Gold ring", "output": "Equipment siphon", "parts_needed": 15, "yield_rate": 0.25, "limit": 10000},
    {"item": "Ruby amulet", "output": "Equipment siphon", "parts_needed": 15, "yield_rate": 0.25, "limit": 10000},
    {"item": "Diamond necklace", "output": "Equipment siphon", "parts_needed": 15, "yield_rate": 0.25, "limit": 10000},
    {"item": "Dragonstone bracelet", "output": "Equipment siphon", "parts_needed": 15, "yield_rate": 0.25, "limit": 10000},
]

CONFIG_FILE = "config.json"

class InventionProfitApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Invention Machine Margins")
        self.geometry("1100x750")
        try: self.iconbitmap('app_icon.ico')
        except Exception: pass
        if HAS_SV_TTK: sv_ttk.set_theme("dark")
            
        self.alch_items = []
        self.dis_items = []
        self.prices = {}
        self.apply_tax = tk.BooleanVar(value=True)
        self.next_refresh_time = 0
        self.sort_state = {}
        
        self.load_config()
        self.create_widgets()
        self.fetch_prices_async()
        self.update_timer()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    self.alch_items = data.get("alch_items", DEFAULT_ALCH_ITEMS.copy())
                    self.dis_items = data.get("dis_items", DISASSEMBLE_RECIPES.copy())
            except Exception:
                self.alch_items = DEFAULT_ALCH_ITEMS.copy()
                self.dis_items = DISASSEMBLE_RECIPES.copy()
        else: 
            self.alch_items = DEFAULT_ALCH_ITEMS.copy()
            self.dis_items = DISASSEMBLE_RECIPES.copy()
            
    def save_config(self):
        with open(CONFIG_FILE, 'w') as f: json.dump({"alch_items": self.alch_items, "dis_items": self.dis_items}, f)

    def create_widgets(self):
        self.top_frame = ttk.Frame(self, padding="10")
        self.top_frame.pack(fill=tk.X)
        self.status_var = tk.StringVar(value="Ready to fetch prices.")
        ttk.Label(self.top_frame, textvariable=self.status_var, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)
        self.timer_var = tk.StringVar(value="")
        ttk.Label(self.top_frame, textvariable=self.timer_var, font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=20)
        self.refresh_btn = ttk.Button(self.top_frame, text="Refresh Prices", command=self.fetch_prices_async)
        self.refresh_btn.pack(side=tk.RIGHT)
        ttk.Checkbutton(self.top_frame, text="Apply 2% GE Tax (Sells)", variable=self.apply_tax, command=self.recalculate_all).pack(side=tk.RIGHT, padx=20)
        
        ttk.Label(self.top_frame, text="Junk Reduction Tier:").pack(side=tk.LEFT, padx=10)
        self.junk_tier = tk.StringVar(value="0")
        ttk.Combobox(self.top_frame, textvariable=self.junk_tier, values=[str(i) for i in range(10)], width=3, state="readonly").pack(side=tk.LEFT)
        self.junk_tier.trace_add("write", lambda *args: self.recalculate_all())
        
        # Legend
        legend_frame = ttk.Frame(self, padding="0 5 10 5")
        legend_frame.pack(fill=tk.X)
        ttk.Label(legend_frame, text="Legend:", font=("Segoe UI", 9, "bold")).pack(side=tk.RIGHT)
        tk.Label(legend_frame, text="Red = Buy limit bottlenecks daily machine production", fg="#ff4444", bg=self.cget('bg')).pack(side=tk.RIGHT, padx=10)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.setup_dash_tab()
        self.setup_alch_tab()
        self.setup_plank_tab()
        self.setup_tanner_tab()
        self.setup_potion_tab()
        self.setup_dis_tab()
        
    def setup_dash_tab(self):
        self.dash_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dash_tab, text="Dashboard Leaders")
        ttk.Label(self.dash_tab, text="Top Most Profitable Items Across All Machines (Ignores Buy Limits)", padding=5).pack(anchor=tk.W)
        self.dash_tree = self.create_treeview(self.dash_tab, ("Rank", "Machine", "Item", "Profit/Item", "Profit/Day"), "dash")

    def treeview_sort_column(self, tv, col, reverse, update_state=True):
        if update_state: self.sort_state[tv] = (col, reverse)
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        try:
            l.sort(key=lambda t: float(t[0].replace(',', '').replace('+', '').replace('-', '')), reverse=reverse)
        except ValueError:
            l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))

    def on_right_click(self, event, tree, tree_type):
        item_id = tree.identify_row(event.y)
        if not item_id: return
        tree.selection_set(item_id)
        values = tree.item(item_id, "values")
        if not values: return
        
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Copy Item Info", command=lambda: self.clipboard_clear() or self.clipboard_append(f"{values[0]} | {values[-1]}"))
        
        if tree_type in ["alch", "dis"]:
            menu.add_separator()
            menu.add_command(label="Delete Custom Item", command=lambda: self.delete_custom_item(tree_type, values))
            
        menu.post(event.x_root, event.y_root)

    def delete_custom_item(self, tree_type, values):
        if tree_type == "alch":
            self.alch_items = [i for i in self.alch_items if i["name"] != values[0]]
            self.save_config()
            self.recalculate_all()
        elif tree_type == "dis":
            self.dis_items = [i for i in self.dis_items if not (i["item"] == values[0] and i["output"] == values[1])]
            self.save_config()
            self.recalculate_all()

    def create_treeview(self, parent, columns, tree_type=""):
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        tree.tag_configure("bottleneck", foreground="#ff4444")
        for col in columns:
            tree.heading(col, text=col, command=lambda c=col: self.treeview_sort_column(tree, c, False))
            tree.column(col, width=110, anchor=tk.E)
        tree.column(columns[0], width=180, anchor=tk.W)
        if len(columns) > 1 and "Price" not in columns[1] and "Value" not in columns[1]:
            tree.column(columns[1], width=140, anchor=tk.W)
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        tree.bind("<Button-3>", lambda e: self.on_right_click(e, tree, tree_type))
        return tree

    def setup_alch_tab(self):
        self.alch_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.alch_tab, text="Alchemiser Mk. II")
        ttk.Label(self.alch_tab, text="Processes 25 items/hr (600/day). High Alch avoids GE tax.", padding=5).pack(anchor=tk.W)
        self.alch_tree = self.create_treeview(self.alch_tab, ("Item", "GE Price", "High Alch", "Buy Limit", "Profit/Item", "Profit/Hr", "Profit/Day"), "alch")
        add_frame = ttk.LabelFrame(self.alch_tab, text="Add Custom Item", padding="10")
        add_frame.pack(fill=tk.X, padx=5, pady=10)
        ttk.Label(add_frame, text="Item Name:").pack(side=tk.LEFT, padx=5)
        self.c_name = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.c_name, width=25).pack(side=tk.LEFT, padx=5)
        ttk.Label(add_frame, text="High Alch:").pack(side=tk.LEFT, padx=5)
        self.c_alch = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.c_alch, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Label(add_frame, text="Buy Limit (4hr):").pack(side=tk.LEFT, padx=5)
        self.c_limit = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.c_limit, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(add_frame, text="Add Item", command=self.add_custom_alch_item).pack(side=tk.LEFT, padx=10)
        
    def setup_plank_tab(self):
        self.plank_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.plank_tab, text="Plank Maker")
        ttk.Label(self.plank_tab, text="Processes 40 items/hr (960/day).", padding=5).pack(anchor=tk.W)
        self.plank_tree = self.create_treeview(self.plank_tab, ("Log", "Plank", "Log Price", "Plank Price", "Buy Limit", "Profit/Item", "Profit/Hr", "Profit/Day"), "plank")
        
    def setup_tanner_tab(self):
        self.tanner_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.tanner_tab, text="Hide Tanner")
        ttk.Label(self.tanner_tab, text="Processes 140 hides/hr (3,360/day).", padding=5).pack(anchor=tk.W)
        self.tanner_tree = self.create_treeview(self.tanner_tab, ("Hide", "Leather", "Hide Price", "Leather Price", "Buy Limit", "Profit/Item", "Profit/Hr", "Profit/Day"), "tanner")
        
    def setup_potion_tab(self):
        self.potion_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.potion_tab, text="Potion Producer DX")
        ttk.Label(self.potion_tab, text="Processes 40 items/hr (960/day).", padding=5).pack(anchor=tk.W)
        self.potion_tree = self.create_treeview(self.potion_tab, ("Herb", "Potion (unf)", "Herb Price", "Potion Price", "Buy Limit", "Profit/Item", "Profit/Hr", "Profit/Day"), "potion")
        
    def setup_dis_tab(self):
        self.dis_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dis_tab, text="Auto Disassembler Mk. II")
        ttk.Label(self.dis_tab, text="Processes 35 items/hr (840/day). Expands to Springs and Siphons.", padding=5).pack(anchor=tk.W)
        self.dis_tree = self.create_treeview(self.dis_tab, ("Item", "Produces", "Item Price", "Prod Price", "Buy Limit", "Profit/Hr", "Profit/Day"), "dis")
        add_frame = ttk.LabelFrame(self.dis_tab, text="Add Custom Item", padding="10")
        add_frame.pack(fill=tk.X, padx=5, pady=10)
        ttk.Label(add_frame, text="Item Name:").pack(side=tk.LEFT, padx=5)
        self.d_name = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.d_name, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Label(add_frame, text="Produces:").pack(side=tk.LEFT, padx=5)
        self.d_out = ttk.Combobox(add_frame, values=[
            "Empty divine charge", "Spring", "Equipment siphon", "Augmentor",
            "Mechanised chinchompa", "Gizmo dissolver", "Augmentation dissolver",
            "Classic component crate (small)", "Classic component crate (large)",
            "Historic component crate (small)", "Historic component crate (large)"
        ], width=30, state="readonly")
        self.d_out.set("Empty divine charge")
        self.d_out.pack(side=tk.LEFT, padx=5)
        ttk.Label(add_frame, text="Parts Needed:").pack(side=tk.LEFT, padx=5)
        self.d_parts = tk.StringVar(value="20")
        ttk.Entry(add_frame, textvariable=self.d_parts, width=5).pack(side=tk.LEFT, padx=5)
        ttk.Label(add_frame, text="Yield Rate:").pack(side=tk.LEFT, padx=5)
        self.d_yield = tk.StringVar(value="0.5")
        ttk.Entry(add_frame, textvariable=self.d_yield, width=5).pack(side=tk.LEFT, padx=5)
        ttk.Label(add_frame, text="Limit:").pack(side=tk.LEFT, padx=5)
        self.d_limit = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.d_limit, width=8).pack(side=tk.LEFT, padx=5)
        ttk.Button(add_frame, text="Add Item", command=self.add_custom_dis_item).pack(side=tk.LEFT, padx=10)
        
    def add_custom_alch_item(self):
        name = self.c_name.get().strip()
        try: 
            alch_val = int(self.c_alch.get().strip())
            limit_val = int(self.c_limit.get().strip() or "0")
        except ValueError: return
        if not name: return
        for item in self.alch_items:
            if item["name"].lower() == name.lower(): return
        self.alch_items.append({"name": name, "alch": alch_val, "limit": limit_val})
        self.save_config()
        self.c_name.set(""); self.c_alch.set(""); self.c_limit.set("")
        self.fetch_prices_async()
        
    def add_custom_dis_item(self):
        name = self.d_name.get().strip()
        out = self.d_out.get().strip()
        try: 
            parts_val = float(self.d_parts.get().strip())
            yield_val = float(self.d_yield.get().strip())
            limit_val = int(self.d_limit.get().strip() or "0")
        except ValueError: return
        if not name or not out: return
        for item in self.dis_items:
            if item["item"].lower() == name.lower() and item["output"].lower() == out.lower(): return
        self.dis_items.append({"item": name, "output": out, "parts_needed": parts_val, "yield_rate": yield_val, "limit": limit_val})
        self.save_config()
        self.d_name.set(""); self.d_limit.set("")
        self.fetch_prices_async()
        
    def update_timer(self):
        if self.next_refresh_time > 0:
            remaining = int(self.next_refresh_time - time.time())
            if remaining <= 0: self.fetch_prices_async()
            else:
                mins, secs = divmod(remaining, 60)
                self.timer_var.set(f"Next refresh in: {mins:02d}:{secs:02d}")
        self.after(1000, self.update_timer)
        
    def fetch_prices_async(self):
        self.status_var.set("Fetching prices...")
        self.refresh_btn.config(state=tk.DISABLED)
        self.next_refresh_time = time.time() + 300
        threading.Thread(target=self.fetch_prices_worker, daemon=True).start()
        
    def fetch_prices_worker(self):
        names = ["Divine charge", "Empty divine charge", "Nature rune", "Vial of water", "Spring", "Equipment siphon"]
        for i in self.alch_items: names.append(i["name"])
        for r in PLANK_RECIPES: names.extend([r["log"], r["plank"]])
        for r in TANNER_RECIPES: names.extend([r["hide"], r["leather"]])
        for r in POTION_RECIPES: names.extend([r["herb"], r["potion"]])
        for r in self.dis_items: names.extend([r["item"], r["output"]])
        
        unique_names = list(set(names))
        
        try:
            self.prices = {}
            for i in range(0, len(unique_names), 40):
                chunk = unique_names[i:i+40]
                url = f"https://api.weirdgloop.org/exchange/history/rs/latest?name={urllib.parse.quote('|'.join(chunk))}"
                with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'RS3Calc/3.0'})) as resp:
                    data = json.loads(resp.read().decode())
                    for k, v in data.items():
                        self.prices[k.lower()] = v["price"]
            self.after(0, self.recalculate_all)
        except Exception as e:
            self.after(0, lambda: self.status_var.set(f"Error: {e}"))
        self.after(0, lambda: self.refresh_btn.config(state=tk.NORMAL))
        
    def get_tax(self): return 0.98 if self.apply_tax.get() else 1.0

    def recalculate_all(self):
        try:
            self.master_leaderboard = []
            divine_charge = self.prices.get("divine charge", 0)
            charge_cost = divine_charge / MACHINE_CHARGES_PER_DIVINE_CHARGE
            self.status_var.set(f"Prices Updated. Div Charge: {divine_charge:,}")
            self.update_alch_tree(charge_cost)
            self.update_plank_tree(charge_cost)
            self.update_tanner_tree(charge_cost)
            self.update_potion_tree(charge_cost)
            self.update_dis_tree(charge_cost)
            self.update_dash_tree()
        except Exception as e: self.status_var.set(f"Error: {e}")
            
    def clear_tree(self, tree):
        for i in tree.get_children(): tree.delete(i)

    def update_alch_tree(self, c_cost):
        self.clear_tree(self.alch_tree)
        nat_price = self.prices.get("nature rune", 0)
        daily_req = ALCHEMISER_ITEMS_PER_HOUR * 24
        for i in self.alch_items:
            p = self.prices.get(i["name"].lower(), 0)
            prof = i["alch"] - (p + nat_price + (ALCH_CHARGES_PER_ITEM * c_cost))
            tag = "bottleneck" if (i.get("limit", 0) * 6) < daily_req and i.get("limit", 0) > 0 else ""
            self.alch_tree.insert("", tk.END, values=(i["name"], f"{p:,}", f"{i['alch']:,}", f"{i.get('limit', 'N/A')}", f"{int(prof):,}", f"{int(prof*25):,}", f"{int(prof*daily_req):,}"), tags=(tag,))
            self.master_leaderboard.append({"machine": "Alchemiser", "item": i["name"], "profit_item": prof, "profit_day": prof*daily_req})
        if self.alch_tree in self.sort_state:
            c, r = self.sort_state[self.alch_tree]
            self.treeview_sort_column(self.alch_tree, c, r, False)
            
    def update_plank_tree(self, c_cost):
        self.clear_tree(self.plank_tree)
        tax = self.get_tax()
        daily_req = PLANK_MAKER_ITEMS_PER_HOUR * 24
        for r in PLANK_RECIPES:
            log_p = self.prices.get(r["log"].lower(), 0)
            plank_p = self.prices.get(r["plank"].lower(), 0)
            prof = (plank_p * tax) - (log_p + r["coin_cost"] + (PLANK_CHARGES_PER_ITEM * c_cost))
            tag = "bottleneck" if (r["limit"] * 6) < daily_req else ""
            self.plank_tree.insert("", tk.END, values=(r["log"], r["plank"], f"{log_p:,}", f"{plank_p:,}", f"{r['limit']}", f"{int(prof):,}", f"{int(prof*40):,}", f"{int(prof*daily_req):,}"), tags=(tag,))
            self.master_leaderboard.append({"machine": "Plank Maker", "item": f"{r['log']} -> {r['plank']}", "profit_item": prof, "profit_day": prof*daily_req})
        if self.plank_tree in self.sort_state:
            c, r = self.sort_state[self.plank_tree]
            self.treeview_sort_column(self.plank_tree, c, r, False)
            
    def update_tanner_tree(self, c_cost):
        self.clear_tree(self.tanner_tree)
        tax = self.get_tax()
        daily_req = TANNER_ITEMS_PER_HOUR * 24
        for r in TANNER_RECIPES:
            hide_p = self.prices.get(r["hide"].lower(), 0)
            lea_p = self.prices.get(r["leather"].lower(), 0)
            prof = (lea_p * tax) - (hide_p + r["coin_cost"] + (TANNER_CHARGES_PER_ITEM * c_cost))
            tag = "bottleneck" if (r["limit"] * 6) < daily_req else ""
            self.tanner_tree.insert("", tk.END, values=(r["hide"], r["leather"], f"{hide_p:,}", f"{lea_p:,}", f"{r['limit']}", f"{int(prof):,}", f"{int(prof*140):,}", f"{int(prof*daily_req):,}"), tags=(tag,))
            self.master_leaderboard.append({"machine": "Hide Tanner", "item": f"{r['hide']} -> {r['leather']}", "profit_item": prof, "profit_day": prof*daily_req})
        if self.tanner_tree in self.sort_state:
            c, r = self.sort_state[self.tanner_tree]
            self.treeview_sort_column(self.tanner_tree, c, r, False)

    def update_potion_tree(self, c_cost):
        self.clear_tree(self.potion_tree)
        vial_p = self.prices.get("vial of water", 0)
        tax = self.get_tax()
        daily_req = POTION_ITEMS_PER_HOUR * 24
        for r in POTION_RECIPES:
            herb_p = self.prices.get(r["herb"].lower(), 0)
            pot_p = self.prices.get(r["potion"].lower(), 0)
            prof = (pot_p * tax) - (herb_p + vial_p + (POTION_CHARGES_PER_ITEM * c_cost))
            tag = "bottleneck" if (r["limit"] * 6) < daily_req else ""
            self.potion_tree.insert("", tk.END, values=(r["herb"], r["potion"], f"{herb_p:,}", f"{pot_p:,}", f"{r['limit']}", f"{int(prof):,}", f"{int(prof*40):,}", f"{int(prof*daily_req):,}"), tags=(tag,))
            self.master_leaderboard.append({"machine": "Potion Producer", "item": f"{r['herb']} -> {r['potion']}", "profit_item": prof, "profit_day": prof*daily_req})
        if self.potion_tree in self.sort_state:
            c, r = self.sort_state[self.potion_tree]
            self.treeview_sort_column(self.potion_tree, c, r, False)

    def update_dis_tree(self, c_cost):
        self.clear_tree(self.dis_tree)
        tax = self.get_tax()
        tier = int(self.junk_tier.get())
        junk_mult = 1.0 + (tier * 0.015)
        daily_req = DISASSEMBLER_ITEMS_PER_HOUR * 24
        for r in self.dis_items:
            item_p = self.prices.get(r["item"].lower(), 0)
            prod_p = self.prices.get(r["output"].lower(), 0)
            items_needed = r["parts_needed"] / (r["yield_rate"] * junk_mult)
            m_cost = DISASSEMBLER_CHARGES_PER_ITEM * c_cost
            prof_per_prod = (prod_p * tax) - (items_needed * (item_p + m_cost))
            prod_hr = DISASSEMBLER_ITEMS_PER_HOUR / items_needed
            prof_hr = prod_hr * prof_per_prod
            tag = "bottleneck" if (r["limit"] * 6) < daily_req else ""
            self.dis_tree.insert("", tk.END, values=(r["item"], r["output"], f"{item_p:,}", f"{prod_p:,}", f"{r['limit']}", f"{int(prof_hr):,}", f"{int(prof_hr*24):,}"), tags=(tag,))
            self.master_leaderboard.append({"machine": "Auto Disassembler", "item": f"{r['item']} -> {r['output']}", "profit_item": prof_per_prod, "profit_day": prof_hr*24})
        if self.dis_tree in self.sort_state:
            c, r = self.sort_state[self.dis_tree]
            self.treeview_sort_column(self.dis_tree, c, r, False)

    def update_dash_tree(self):
        self.clear_tree(self.dash_tree)
        self.master_leaderboard.sort(key=lambda x: x["profit_day"], reverse=True)
        for i, row in enumerate(self.master_leaderboard[:25]):
            self.dash_tree.insert("", tk.END, values=(f"#{i+1}", row["machine"], row["item"], f"{int(row['profit_item']):,}", f"{int(row['profit_day']):,}"))
        if self.dash_tree in self.sort_state:
            c, r = self.sort_state[self.dash_tree]
            self.treeview_sort_column(self.dash_tree, c, r, False)

if __name__ == "__main__":
    app = InventionProfitApp()
    app.mainloop()
