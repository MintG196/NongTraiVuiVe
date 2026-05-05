"""
SDV Farm Map v3 - Final polished version.
Fixes: no white squares, proper tree/bush placement, clean autotile dirt, correct fence.
"""
from PIL import Image
import os, random

random.seed(42)
SRC = r"D:\Stardew Valley Assets"
OUT = r"D:\Nong Trai\public\assets"
os.makedirs(OUT, exist_ok=True)

# Load sheets
od = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Tilesets - Outdoors (Spring).png")).convert("RGBA")
fb = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Tilesets - Farm Buildings.png")).convert("RGBA")
tr = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Environment - Trees.png")).convert("RGBA")
fc = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Tilesets - Fences.png")).convert("RGBA")
dt = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Tilesets - Dirt (Hoed).png")).convert("RGBA")
bu = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Environment - Bushes.png")).convert("RGBA")
cr = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Tilesets - Craftables.png")).convert("RGBA")
ti = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Tilesets - Town Interiors.png")).convert("RGBA")
fl = Image.open(os.path.join(SRC, "PC _ Computer - Stardew Valley - Tilesets - Flooring.png")).convert("RGBA")

T = 16; S = 4

def sc(img):
    return img.resize((img.width*S, img.height*S), Image.NEAREST)

# ===================================================================
# TILE LIBRARY
# ===================================================================
# Grass variations (all from outdoors, verified opaque)
g = [
    od.crop((16, 96, 32, 112)),   # Plain grass (main)
    od.crop((0, 96, 16, 112)),    # Grass with small detail
    od.crop((16, 112, 32, 128)),  # Slightly different green
    od.crop((0, 112, 16, 128)),   # Another variant
]
# Grass with flowers (decorative, scattered)
gf1 = od.crop((0, 80, 16, 96))   # White/pink flowers on grass
gf2 = od.crop((16, 80, 32, 96))  # Alternate flowers

# Dirt ground (solid brown)
dg = od.crop((48, 96, 64, 112))
dg2 = od.crop((64, 96, 80, 112))   # Slightly different dirt

# Hoed dirt autotile (dry - cols 0-2)
hd = {}
for name, c, r in [('tl',0,0),('t',1,0),('tr',2,0),
                     ('l',0,1),('c',1,1),('r',2,1),
                     ('bl',0,2),('b',1,2),('br',2,2)]:
    hd[name] = dt.crop((c*T, r*T, (c+1)*T, (r+1)*T))

# Hoed dirt (wet - cols 6-8)
hw = {}
for name, c, r in [('tl',6,0),('t',7,0),('tr',8,0),
                     ('l',6,1),('c',7,1),('r',8,1),
                     ('bl',6,2),('b',7,2),('br',8,2)]:
    hw[name] = dt.crop((c*T, r*T, (c+1)*T, (r+1)*T))

# Fence tiles from Fences.png
# Wood fence (col 0): Each tile is 16x16
# Row 0: Single post facing forward  
# Row 1: Post with rails extending
# Row 2: Full horizontal fence
# Row 3: Fence with damage
# For horizontal runs, use these:
fc_post = fc.crop((0, 32, 16, 48))     # Fence post bottom
fc_hrail = fc.crop((16, 32, 32, 48))   # Horizontal rail
fc_post_t = fc.crop((0, 16, 16, 32))   # Post top section
fc_hrail_t = fc.crop((16, 16, 32, 32)) # Rail top section

# Trees (from tree sheet, verified proper alpha)
tree1 = tr.crop((0, 0, 48, 80))        # Oak
tree2 = tr.crop((120, 0, 168, 80))     # Maple
tree3 = tr.crop((240, 0, 288, 80))     # Pine

# Bushes (verified from debug - row 0 has green bushes)
# bush sheet: 128x352
# Row 0: 4 bushes each 32x32 (green with berries, green, teal, palm)
bush1 = bu.crop((0, 0, 32, 32))   # Green with berries  
bush2 = bu.crop((32, 0, 64, 32))  # Plain green
bush3 = bu.crop((64, 0, 96, 32))  # Teal/cyan
# Row 4 (y=128): Large round bushes ~48x48
bush_big = bu.crop((0, 128, 48, 176))  # Big dark green
# Small bushes row 6 (y=224): tiny 16x16
bush_sm = bu.crop((0, 224, 16, 240))

# Craftables
scarecrow = cr.crop((0, 0, 16, 32))
chest = cr.crop((32, 256, 48, 288))
barrel = cr.crop((96, 256, 112, 288))

# Farmhouse
farmhouse = fb.crop((0, 272, 152, 412))
sc(farmhouse).save(os.path.join(OUT, "farmhouse.png"))

# Well
well = fb.crop((336, 16, 368, 64))
sc(well).save(os.path.join(OUT, "well.png"))

# Save individual tile assets
sc(g[0]).save(os.path.join(OUT, "grass.png"))
sc(g[1]).save(os.path.join(OUT, "grass2.png"))
sc(hd['c']).save(os.path.join(OUT, "dirt.png"))
sc(hw['c']).save(os.path.join(OUT, "dirt_wet.png"))
sc(dg).save(os.path.join(OUT, "dirt_path.png"))
sc(tree1).save(os.path.join(OUT, "tree_green.png"))
sc(tree2).save(os.path.join(OUT, "tree_dark.png"))
sc(bush1).save(os.path.join(OUT, "bush.png"))
sc(scarecrow).save(os.path.join(OUT, "scarecrow.png"))
sc(chest).save(os.path.join(OUT, "chest.png"))
sc(barrel).save(os.path.join(OUT, "barrel.png"))
bed = ti.crop((192, 0, 224, 48))
sc(bed).save(os.path.join(OUT, "bed.png"))
sc(tr.crop((0, 80, 48, 128))).save(os.path.join(OUT, "stump.png"))

print("=== Tiles saved ===")

# ===================================================================
# MAP COMPOSITION
# ===================================================================
MW, MH = 20, 15
canvas = Image.new("RGBA", (MW*T, MH*T), (0,0,0,0))

# ---- LAYER 0: Full grass coverage (NO gaps!) ----
for r in range(MH):
    for c in range(MW):
        rng = random.random()
        if rng < 0.5:
            t = g[0]
        elif rng < 0.75:
            t = g[1]
        elif rng < 0.88:
            t = g[2]
        elif rng < 0.94:
            t = gf1  # Scattered flowers
        else:
            t = gf2
        canvas.paste(t, (c*T, r*T), t)

# ---- LAYER 1: Dirt ground (farm area) ----
# Main farm zone: rows 5-12, cols 4-15
for r in range(5, 13):
    for c in range(4, 16):
        canvas.paste(dg, (c*T, r*T), dg)
# Path from house to farm (cols 9-10, rows 2-5)
for r in range(2, 6):
    canvas.paste(dg, (9*T, r*T), dg)
    canvas.paste(dg, (10*T, r*T), dg)

# ---- LAYER 2: Farm plots with autotile edges ----
def draw_plot(tr_, lc, h, w):
    for ry in range(h):
        for cx in range(w):
            top = (ry == 0); bot = (ry == h-1)
            left = (cx == 0); right = (cx == w-1)
            if top and left: k = 'tl'
            elif top and right: k = 'tr'
            elif bot and left: k = 'bl'
            elif bot and right: k = 'br'
            elif top: k = 't'
            elif bot: k = 'b'
            elif left: k = 'l'
            elif right: k = 'r'
            else: k = 'c'
            canvas.paste(hd[k], ((lc+cx)*T, (tr_+ry)*T), hd[k])

# 4 separate plots
draw_plot(6, 5, 3, 4)    # Top-left
draw_plot(6, 10, 3, 5)   # Top-right 
draw_plot(10, 5, 2, 4)   # Bot-left
draw_plot(10, 10, 2, 5)  # Bot-right

# ---- LAYER 3: Fence (using fence tiles, horizontal segments) ----
def draw_h_fence(row, c1, c2):
    """Draw horizontal fence across row from col c1 to c2."""
    for c in range(c1, c2+1):
        if c == c1 or c == c2:
            # Posts at ends
            canvas.paste(fc_post_t, (c*T, (row-1)*T), fc_post_t)
            canvas.paste(fc_post, (c*T, row*T), fc_post)
        elif (c - c1) % 3 == 0:
            # Posts every 3 tiles
            canvas.paste(fc_post_t, (c*T, (row-1)*T), fc_post_t)
            canvas.paste(fc_post, (c*T, row*T), fc_post)
        else:
            # Rails between posts
            canvas.paste(fc_hrail_t, (c*T, (row-1)*T), fc_hrail_t)
            canvas.paste(fc_hrail, (c*T, row*T), fc_hrail)

def draw_v_fence(col, r1, r2):
    """Draw vertical fence posts down column."""
    for r in range(r1, r2+1):
        canvas.paste(fc_post, (col*T, r*T), fc_post)

# Top fence
draw_h_fence(5, 4, 15)
# Bottom fence
draw_h_fence(13, 4, 15)
# Left fence
draw_v_fence(4, 5, 12)
# Right fence
draw_v_fence(15, 5, 12)

# Gate opening (remove fence at path entrance)
# Clear the fence at cols 9-10 on top row for the path
canvas.paste(dg, (9*T, 4*T), dg)
canvas.paste(dg, (10*T, 4*T), dg)
canvas.paste(dg, (9*T, 5*T), dg)
canvas.paste(dg, (10*T, 5*T), dg)

# ---- LAYER 4: Trees (placed AFTER grass so no white gaps) ----
# Large trees around edges
canvas.paste(tree1, (0*T, 0*T), tree1)         # Top-left oak
canvas.paste(tree1, (0*T, 6*T), tree1)          # Mid-left oak
canvas.paste(tree2, (17*T, 0*T), tree2)         # Top-right maple
canvas.paste(tree2, (17*T, 7*T), tree2)          # Mid-right maple
canvas.paste(tree3, (0*T, 11*T), tree3)          # Bot-left pine
canvas.paste(tree1, (2*T, 1*T), tree1)           # Near house left

# ---- LAYER 5: Bushes ----
canvas.paste(bush1, (4*T, 0*T), bush1)          # Top bushes
canvas.paste(bush2, (6*T, 0*T), bush2)
canvas.paste(bush3, (14*T, 0*T), bush3)
canvas.paste(bush_big, (16*T, 13*T), bush_big)  # Bottom-right big bush
canvas.paste(bush1, (0*T, 14*T), bush1)         # Bottom-left

# ---- LAYER 6: Objects ----
canvas.paste(scarecrow, (7*T, 7*T), scarecrow)  # Scarecrow in field
canvas.paste(barrel, (3*T, 3*T), barrel)         # Barrel near house
canvas.paste(chest, (12*T, 3*T), chest)          # Chest

# ---- Scale up ----
map_out = canvas.resize((MW*T*S, MH*T*S), Image.NEAREST)
map_out.save(os.path.join(OUT, "map_rendered.png"))
print(f"Map: {map_out.size} ({MW}x{MH} tiles, {S}x scale)")

# ===================================================================
# FIELD BG
# ===================================================================
field = Image.new("RGBA", (MW*T, MH*T), (0,0,0,0))
for r in range(MH):
    for c in range(MW):
        rng = random.random()
        t = g[0] if rng < 0.55 else g[1] if rng < 0.8 else gf1 if rng < 0.93 else gf2
        field.paste(t, (c*T, r*T), t)
sc(field).save(os.path.join(OUT, "field_bg.png"))

# ===================================================================
# HOUSE INTERIOR BG
# ===================================================================
wf = fl.crop((128, 0, 144, 16))
hb = Image.new("RGBA", (MW*T, MH*T), (0,0,0,0))
for r in range(MH):
    for c in range(MW):
        hb.paste(wf, (c*T, r*T), wf)
sc(hb).save(os.path.join(OUT, "house_bg.png"))

print("=== ALL DONE ===")
