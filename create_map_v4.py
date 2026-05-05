"""
SDV Farm Map v4 - The "Perfect" Version.
- Standard 864x672 resolution.
- Opaque grass base to fix white squares.
- Organic layering (Grass -> Path -> Dirt -> Objects -> Trees).
"""
from PIL import Image, ImageDraw
import os, random

random.seed(99) # New seed for better layout
SRC = r"D:\Stardew Valley Assets"
OUT = r"D:\Nong Trai\public\assets"
os.makedirs(OUT, exist_ok=True)

# Load Sheets
od = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Tilesets - Outdoors (Spring).png")).convert("RGBA")
fb = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Tilesets - Farm Buildings.png")).convert("RGBA")
tr = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Environment - Trees.png")).convert("RGBA")
fc = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Tilesets - Fences.png")).convert("RGBA")
dt = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Tilesets - Dirt (Hoed).png")).convert("RGBA")
bu = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Environment - Bushes.png")).convert("RGBA")
cr = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Tilesets - Craftables.png")).convert("RGBA")
fl = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Tilesets - Flooring.png")).convert("RGBA")

# Game uses 3x scale usually for pixel perfect look
# Target: 864x672. 
# 864/3 = 288px. 672/3 = 224px.
# We will draw on a 288x224 canvas and scale by 3.
# 288/16 = 18 tiles. 224/16 = 14 tiles.
TW, TH = 18, 14
T = 16
SCALE = 3

canvas = Image.new("RGBA", (TW*T, TH*T), (33, 148, 26, 255)) # Solid SDV Green base

# --- 1. GRASS LAYER ---
grass_main = od.crop((16, 96, 32, 112))
grass_detail = od.crop((0, 96, 16, 112))
grass_flower = od.crop((0, 80, 16, 96))

for r in range(TH):
    for c in range(TW):
        tile = grass_main
        if random.random() < 0.2: tile = grass_detail
        if random.random() < 0.05: tile = grass_flower
        canvas.paste(tile, (c*T, r*T), tile)

# --- 2. PATHS (Organic dirt) ---
dirt_tile = od.crop((48, 96, 64, 112))
# Draw a path from top (house) down to center
for r in range(1, 6):
    for c in range(8, 11):
        canvas.paste(dirt_tile, (c*T, r*T), dirt_tile)
# Connect to a main area
for r in range(6, 11):
    for c in range(3, 15):
        canvas.paste(dirt_tile, (c*T, r*T), dirt_tile)

# --- 3. FARM PLOTS (Hoed dirt) ---
# Extract dry hoed dirt center
hd_c = dt.crop((16, 16, 32, 32))
for r in range(7, 10):
    for c in range(4, 8):
        canvas.paste(hd_c, (c*T, r*T), hd_c)
    for c in range(10, 14):
        canvas.paste(hd_c, (c*T, r*T), hd_c)

# --- 4. BUILDINGS ---
# Farmhouse (152x140 pixels)
house = fb.crop((0, 272, 152, 412))
# Place house at top center
canvas.paste(house, (60, 0), house)

# Shipping bin (next to house)
bin_tile = fb.crop((16, 0, 48, 32))
canvas.paste(bin_tile, (212, 60), bin_tile)

# --- 5. FENCE ---
# Using the clean fence from fences.png
fence_h = fc.crop((16, 32, 32, 48))
fence_p = fc.crop((0, 32, 16, 48))
# Bottom fence line
for c in range(3, 15):
    canvas.paste(fence_h, (c*T, 11*T), fence_h)
    if c % 3 == 0: canvas.paste(fence_p, (c*T, 11*T), fence_p)

# --- 6. ENVIRONMENT (TREES & BUSHES) ---
# Trees at the edges
oak = tr.crop((0, 0, 48, 80))
maple = tr.crop((120, 0, 168, 80))
canvas.paste(oak, (0, -10), oak)
canvas.paste(oak, (240, -10), oak)
canvas.paste(maple, (0, 100), maple)
canvas.paste(maple, (240, 100), maple)

# Bushes and clutter
bush = bu.crop((0, 0, 32, 32))
canvas.paste(bush, (40, 40), bush)
canvas.paste(bush, (200, 180), bush)

scarecrow = cr.crop((0, 0, 16, 32))
canvas.paste(scarecrow, (140, 130), scarecrow)

# --- FINAL SCALE ---
map_final = canvas.resize((864, 672), Image.NEAREST)
map_final.save(os.path.join(OUT, "map_rendered.png"))

# Also update field_bg and house_bg to match
field_bg = Image.new("RGBA", (TW*T, TH*T), (33, 148, 26, 255))
for r in range(TH):
    for c in range(TW):
        t = grass_main if random.random() < 0.8 else grass_detail
        field_bg.paste(t, (c*T, r*T), t)
field_bg.resize((864, 672), Image.NEAREST).save(os.path.join(OUT, "field_bg.png"))

wood_floor = fl.crop((128, 0, 144, 16))
house_bg = Image.new("RGBA", (TW*T, TH*T), (101, 67, 33, 255))
for r in range(TH):
    for c in range(TW):
        house_bg.paste(wood_floor, (c*T, r*T), wood_floor)
house_bg.resize((864, 672), Image.NEAREST).save(os.path.join(OUT, "house_bg.png"))

print("Map v4 Generated Successfully!")
