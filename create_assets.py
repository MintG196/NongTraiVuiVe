"""
Final Stardew Valley asset extraction.
Creates the farm map and all tiles needed for the game.
Fence tiles are 16x32 in Fences.png with column layout.
"""
from PIL import Image, ImageDraw
import os

SRC = r"D:\Stardew Valley Assets"
OUT = r"D:\Nong Trai\public\assets"
os.makedirs(OUT, exist_ok=True)

outdoors = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Tilesets - Outdoors (Spring).png")).convert("RGBA")
farm_bld = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Tilesets - Farm Buildings.png")).convert("RGBA")
trees_sh = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Environment - Trees.png")).convert("RGBA")
fences   = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Tilesets - Fences.png")).convert("RGBA")
dirt_sh  = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Tilesets - Dirt (Hoed).png")).convert("RGBA")
bushes   = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Environment - Bushes.png")).convert("RGBA")
craft_sh = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Tilesets - Craftables.png")).convert("RGBA")
town_int = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Tilesets - Town Interiors.png")).convert("RGBA")
flooring = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Tilesets - Flooring.png")).convert("RGBA")

T = 16; S = 3

def scale(img):
    return img.resize((img.width*S, img.height*S), Image.NEAREST)

# === TILE EXTRACTION ===
# Grass (2 variants from outdoors)
g1 = outdoors.crop((0, 96, 16, 112))
g2 = outdoors.crop((16, 96, 32, 112))
scale(g1).save(os.path.join(OUT, "grass.png"))

# Dirt ground  
dg = outdoors.crop((48, 96, 64, 112))
scale(dg).save(os.path.join(OUT, "dirt_path.png"))

# Hoed dirt
hd = dirt_sh.crop((16, 16, 32, 32))
scale(hd).save(os.path.join(OUT, "dirt.png"))
wd = dirt_sh.crop((112, 16, 128, 32))
scale(wd).save(os.path.join(OUT, "dirt_wet.png"))

# Farmhouse (verified correct crop)
fh = farm_bld.crop((0, 272, 152, 412))
scale(fh).save(os.path.join(OUT, "farmhouse.png"))

# Trees
t1 = trees_sh.crop((0, 0, 48, 80))
scale(t1).save(os.path.join(OUT, "tree_green.png"))
t2 = trees_sh.crop((120, 0, 168, 80))
scale(t2).save(os.path.join(OUT, "tree_dark.png"))

# Bush
b1 = bushes.crop((0, 0, 32, 32))
scale(b1).save(os.path.join(OUT, "bush.png"))

# Stump
st = trees_sh.crop((8, 80, 40, 112))
scale(st).save(os.path.join(OUT, "stump.png"))

# Craftables
scale(craft_sh.crop((96, 256, 112, 288))).save(os.path.join(OUT, "barrel.png"))
scale(craft_sh.crop((32, 256, 48, 288))).save(os.path.join(OUT, "chest.png"))
scale(craft_sh.crop((0, 0, 16, 32))).save(os.path.join(OUT, "scarecrow.png"))

# Bed
scale(town_int.crop((192, 0, 224, 48))).save(os.path.join(OUT, "bed.png"))

# Well (from outdoors - the stone well)
# Actually the well is in Craftables around row 6-8
# Let me use the well from farm buildings
well = farm_bld.crop((336, 16, 368, 64))
scale(well).save(os.path.join(OUT, "well.png"))

print("=== Tiles extracted ===")

# === COMPOSE MAP ===
# 18 tiles wide x 14 tiles tall = 288x224 native -> 864x672 at 3x
MW, MH = 18, 14
fm = Image.new("RGBA", (MW*T, MH*T), (0,0,0,0))

# Ground: all grass first
for r in range(MH):
    for c in range(MW):
        tile = g1 if (r*7+c*3) % 5 != 0 else g2
        fm.paste(tile, (c*T, r*T), tile)

# Dirt area (farm zone) - around center
for r in range(4, 12):
    for c in range(3, 15):
        fm.paste(dg, (c*T, r*T), dg)

# Path from top to farm area
for r in range(1, 5):
    for c in range(8, 10):
        fm.paste(dg, (c*T, r*T), dg)

# Hoed dirt farm plots (EMPTY - no crops, user specified)
for r in range(6, 11):
    for c in range(5, 13):
        fm.paste(hd, (c*T, r*T), hd)

# === FENCE (draw simple brown wooden fence with PIL) ===
draw = ImageDraw.Draw(fm)
# Fence colors matching SDV wood fence
fc_dark = (101, 67, 33, 255)
fc_light = (139, 90, 43, 255)
fc_med = (120, 78, 38, 255)

def draw_fence_h(y, x1, x2):
    """Draw horizontal fence line."""
    # Posts
    for x in range(x1, x2+1, T):
        # Post
        draw.rectangle([x+5, y-2, x+10, y+14], fill=fc_dark)
        draw.rectangle([x+6, y-1, x+9, y+13], fill=fc_med)
    # Horizontal rails
    draw.rectangle([x1+2, y+2, x2+14, y+5], fill=fc_light)
    draw.rectangle([x1+2, y+8, x2+14, y+11], fill=fc_light)

def draw_fence_v(x, y1, y2):
    """Draw vertical fence line."""
    for y in range(y1, y2+1, T):
        draw.rectangle([x+5, y, x+10, y+14], fill=fc_dark)
        draw.rectangle([x+6, y+1, x+9, y+13], fill=fc_med)
    draw.rectangle([x+3, y1, x+5, y2+14], fill=fc_light)
    draw.rectangle([x+10, y1, x+12, y2+14], fill=fc_light)

# Farm fence (around the dirt area)
draw_fence_h(4*T-2, 3*T, 14*T)    # Top
draw_fence_h(11*T+2, 3*T, 14*T)   # Bottom
draw_fence_v(3*T-2, 4*T, 11*T)    # Left
draw_fence_v(14*T+2, 4*T, 11*T)   # Right

# === DECORATIVE OBJECTS ===
# Trees
fm.paste(t1, (0, 0), t1)       # Top-left
fm.paste(t1, (0, 96), t1)      # Mid-left
fm.paste(t2, (256, 0), t2)     # Top-right
fm.paste(t2, (256, 112), t2)   # Mid-right
fm.paste(t1, (0, 160), t1)     # Bot-left

# Bushes
fm.paste(b1, (48, 0), b1)
fm.paste(b1, (208, 192), b1)
bush_sm = bushes.crop((0, 176, 16, 192))
fm.paste(bush_sm, (240, 176), bush_sm)

# Stump
fm.paste(st, (240, 128), st)

# Scale entire map 3x
map_big = fm.resize((MW*T*S, MH*T*S), Image.NEAREST)
map_big.save(os.path.join(OUT, "map_rendered.png"))
print(f"Map: {map_big.size}")

# === FIELD BG ===
fb = Image.new("RGBA", (MW*T, MH*T), (0,0,0,0))
for r in range(MH):
    for c in range(MW):
        fb.paste(g1 if (r+c)%3 else g2, (c*T, r*T), g1 if (r+c)%3 else g2)
scale(fb).save(os.path.join(OUT, "field_bg.png"))

# === HOUSE INTERIOR BG ===
wf = flooring.crop((128, 0, 144, 16))
hb = Image.new("RGBA", (MW*T, MH*T), (0,0,0,0))
for r in range(MH):
    for c in range(MW):
        hb.paste(wf, (c*T, r*T), wf)
scale(hb).save(os.path.join(OUT, "house_bg.png"))

print("=== ALL DONE ===")
