"""
SDV Farm Map v5 - The Masterpiece.
- Native 16px tiles on a 54x42 grid (864x672 total).
- Expansive layout, smaller house ratio.
- Fix purple fence lines.
- Organic clutter and professional layering.
"""
from PIL import Image
import os, random

random.seed(123)
SRC = r"D:\Stardew Valley Assets"
OUT = r"D:\Nong Trai\public\assets"
os.makedirs(OUT, exist_ok=True)

# Load Sheets
def load_rgba(name):
    return Image.open(os.path.join(SRC, name)).convert("RGBA")

od = load_rgba("PC _ Computer - Stardew Valley - Tilesets - Outdoors (Spring).png")
fb = load_rgba("PC _ Computer - Stardew Valley - Tilesets - Farm Buildings.png")
tr = load_rgba("PC _ Computer - Stardew Valley - Environment - Trees.png")
fc = load_rgba("PC _ Computer - Stardew Valley - Tilesets - Fences.png")
dt = load_rgba("PC _ Computer - Stardew Valley - Tilesets - Dirt (Hoed).png")
bu = load_rgba("PC _ Computer - Stardew Valley - Environment - Bushes.png")
cr = load_rgba("PC _ Computer - Stardew Valley - Tilesets - Craftables.png")
fl = load_rgba("PC _ Computer - Stardew Valley - Tilesets - Flooring.png")

# 864x672 / 16 = 54x42 tiles
TW, TH = 54, 42
T = 16
canvas = Image.new("RGBA", (TW*T, TH*T), (33, 148, 26, 255))

# --- TILE PREP ---
grass_tiles = [
    od.crop((16, 96, 32, 112)),   # Main
    od.crop((0, 96, 16, 112)),    # Detailed
    od.crop((0, 80, 16, 96)),     # Flower 1
    od.crop((16, 80, 32, 96))     # Flower 2
]

# --- 1. BASE GRASS ---
for r in range(TH):
    for c in range(TW):
        tile = grass_tiles[0]
        rnd = random.random()
        if rnd < 0.15: tile = grass_tiles[1]
        elif rnd < 0.03: tile = grass_tiles[2]
        elif rnd < 0.02: tile = grass_tiles[3]
        canvas.paste(tile, (c*T, r*T), tile)

# --- 2. DIRT PATHS ---
dirt_main = od.crop((48, 96, 64, 112))
# Draw a winding path from house area to bottom and right
def draw_rect_dirt(x, y, w, h):
    for r in range(y, y+h):
        for c in range(x, x+w):
            if 0<=c<TW and 0<=r<TH:
                canvas.paste(dirt_main, (c*T, r*T), dirt_main)

# Path around house
draw_rect_dirt(20, 5, 14, 12) 
# Path leading to farm area
draw_rect_dirt(15, 15, 25, 20)
# Path to right exit
draw_rect_dirt(40, 20, 14, 4)

# --- 3. FARM PLOTS (Hoed Dirt) ---
hd_c = dt.crop((16, 16, 32, 32))
# Multiple 4x4 plots
for pr, pc in [(18, 18), (18, 28), (26, 18), (26, 28)]:
    for r in range(pr, pr+5):
        for c in range(pc, pc+7):
            canvas.paste(hd_c, (c*T, r*T), hd_c)

# --- 4. HOUSE & BUILDINGS ---
# Farmhouse
house = fb.crop((0, 272, 152, 412))
canvas.paste(house, (20*T, 2*T), house)

# Shipping Bin
bin_img = fb.crop((16, 0, 48, 32))
canvas.paste(bin_img, (35*T, 10*T), bin_img)

# Well
well = fb.crop((336, 16, 368, 64))
canvas.paste(well, (12*T, 10*T), well)

# --- 5. FENCE (Fixing the purple lines) ---
# We take the fence from outdoors sheet where it's already on grass
fence_wood = od.crop((128, 224, 176, 256)) # 3x2 tiles
# Use individual clean pieces
f_post = fence_wood.crop((0, 16, 16, 32))
f_rail = fence_wood.crop((16, 16, 32, 32))

def draw_fence_h(row, c1, c2):
    for c in range(c1, c2+1):
        tile = f_post if (c-c1)%4 == 0 else f_rail
        canvas.paste(tile, (c*T, row*T), tile)

# Fence around the farm area
draw_fence_h(16, 16, 36)
draw_fence_h(32, 16, 36)

# --- 6. TREES & CLUTTER ---
oak = tr.crop((0, 0, 48, 80))
maple = tr.crop((120, 0, 168, 80))
pine = tr.crop((240, 0, 288, 80))

# Scatter trees around the edges
for pos in [(2,2), (5,10), (2,25), (10,45), (30,5), (35,45), (2,50)]:
    t_img = random.choice([oak, maple, pine])
    canvas.paste(t_img, (pos[1]*T, pos[0]*T), t_img)

# Bushes
bush1 = bu.crop((0, 0, 32, 32))
for pos in [(15,5), (38,15), (20,48), (5,40)]:
    canvas.paste(bush1, (pos[1]*T, pos[0]*T), bush1)

# Scarecrow & Chests
scarecrow = cr.crop((0, 0, 16, 32))
canvas.paste(scarecrow, (27*T, 22*T), scarecrow)
chest = cr.crop((32, 256, 48, 288))
canvas.paste(chest, (28*T, 10*T), chest)

# --- SAVE ---
canvas.save(os.path.join(OUT, "map_rendered.png"))

# Internal backgrounds
field_bg = Image.new("RGBA", (TW*T, TH*T), (33, 148, 26, 255))
for r in range(TH):
    for c in range(TW):
        t = grass_tiles[0] if random.random() < 0.8 else grass_tiles[1]
        field_bg.paste(t, (c*T, r*T), t)
field_bg.save(os.path.join(OUT, "field_bg.png"))

wood_floor = fl.crop((128, 0, 144, 16))
house_bg = Image.new("RGBA", (TW*T, TH*T), (101, 67, 33, 255))
for r in range(TH):
    for c in range(TW):
        house_bg.paste(wood_floor, (c*T, r*T), wood_floor)
house_bg.save(os.path.join(OUT, "house_bg.png"))

print("Map v5 Masterpiece Created!")
