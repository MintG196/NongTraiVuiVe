"""
Extract individual tiles from LPC Base Assets spritesheets.
LPC tiles are 32x32 grid based.
"""
from PIL import Image
import os

OUT = r"D:\Nong Trai\public\assets"
LPC = r"D:\Nong Trai\LPC Base Assets\tiles"
os.makedirs(OUT, exist_ok=True)

def crop_tile(src, x, y, w=32, h=32, name=None, scale=1):
    """Crop a tile from a spritesheet at grid position (x*32, y*32)."""
    img = Image.open(os.path.join(LPC, src)).convert("RGBA")
    box = (x * 32, y * 32, x * 32 + w, y * 32 + h)
    tile = img.crop(box)
    if scale > 1:
        tile = tile.resize((w * scale, h * scale), Image.NEAREST)
    tile.save(os.path.join(OUT, name))
    print(f"  Saved {name} ({w}x{h}) from {src}")

def crop_px(src, x, y, w, h, name, scale=1):
    """Crop by exact pixel coordinates."""
    img = Image.open(os.path.join(LPC, src)).convert("RGBA")
    tile = img.crop((x, y, x + w, y + h))
    if scale > 1:
        tile = tile.resize((w * scale, h * scale), Image.NEAREST)
    tile.save(os.path.join(OUT, name))
    print(f"  Saved {name} ({w}x{h}) from {src}")

print("=== Extracting LPC tiles ===")

# --- GRASS tile (simple green grass, top-left of grass.png) ---
crop_tile("grass.png", 0, 0, name="grass.png", scale=2)

# --- DIRT tile (farmland soil - from dirt.png, the solid fill area) ---
# dirt.png has transitions; let's grab the center solid dirt
# The solid fill is typically at position (2,2) in the autotile layout
crop_tile("dirt2.png", 2, 2, name="dirt.png", scale=2)

# --- DIRT tilled/watered (darker dirt) ---
crop_tile("dirt.png", 2, 2, name="dirt_wet.png", scale=2)

# --- TREE (treetop + trunk combined) ---
# treetop.png has 2 rows: round bushes (row 0) and pine trees (row 1)
# Each tree top is roughly 64x64 (2x2 tiles)
crop_px("treetop.png", 0, 0, 64, 64, "tree_top.png", scale=2)
crop_px("trunk.png", 0, 0, 32, 32, "tree_trunk.png", scale=2)

# --- HOUSE parts ---
# house.png has walls, doors, windows - let's compose a simple house
# We'll just grab the whole spritesheet and use parts in-game
img = Image.open(os.path.join(LPC, "house.png")).convert("RGBA")
img_scaled = img.resize((img.width * 2, img.height * 2), Image.NEAREST)
img_scaled.save(os.path.join(OUT, "house_sheet.png"))
print(f"  Saved house_sheet.png")

# Grab individual house components at 2x scale
# Red brick wall section (top-left of house.png)
crop_px("house.png", 0, 0, 96, 80, "house_wall.png", scale=2)

# Door 
crop_px("house.png", 96, 0, 32, 64, "door.png", scale=2)

# Window
crop_px("house.png", 160, 0, 32, 32, "window.png", scale=2)

# --- BARREL ---
crop_px("barrel.png", 0, 0, 32, 40, "barrel.png", scale=2)

# --- BUCKET ---  
crop_px("buckets.png", 0, 0, 32, 32, "bucket.png", scale=2)

# --- CHEST ---
crop_px("chests.png", 0, 0, 32, 32, "chest.png", scale=2)

# --- SIGN ---
crop_px("signs.png", 0, 0, 32, 32, "sign.png", scale=2)

# --- BED (for house interior scene) ---
crop_px("country.png", 0, 0, 64, 96, "bed.png", scale=2)

# --- CHAIR ---
crop_px("country.png", 96, 32, 32, 32, "chair.png", scale=2)

# --- Compose a simple house sprite (wall + roof) ---
# Let's build a 3x3 tile house (96x96 -> 192x192 at 2x)
house_canvas = Image.new("RGBA", (192, 192), (0, 0, 0, 0))
# Load wall brick tile
wall_src = Image.open(os.path.join(LPC, "house.png")).convert("RGBA")
# The brick pattern is at row 0, a single red brick tile
brick = wall_src.crop((0, 0, 32, 32)).resize((64, 64), Image.NEAREST)
# Place bricks as walls
for cx in range(3):
    for cy in range(1, 3):
        house_canvas.paste(brick, (cx * 64, cy * 64), brick)
# Simple roof (use a darker tinted version of brick as placeholder)
roof_src = wall_src.crop((0, 64, 32, 96)).resize((64, 64), Image.NEAREST)
for cx in range(3):
    house_canvas.paste(roof_src, (cx * 64, 0), roof_src)
# Door in center
door = wall_src.crop((96, 0, 128, 64)).resize((64, 128), Image.NEAREST)
house_canvas.paste(door, (64, 64), door)
house_canvas.save(os.path.join(OUT, "house_built.png"))
print(f"  Saved house_built.png (192x192 composed house)")

# --- Compose a shop sprite (use victoria/inside elements) ---
victoria = Image.open(os.path.join(LPC, "victoria.png")).convert("RGBA")
shop_canvas = Image.new("RGBA", (192, 192), (0, 0, 0, 0))
# Use victoria furniture + inside walls to create a shop look
inside_src = Image.open(os.path.join(LPC, "inside.png")).convert("RGBA")
# Get a wall piece
iwall = inside_src.crop((0, 0, 32, 32)).resize((64, 64), Image.NEAREST)
for cx in range(3):
    for cy in range(3):
        shop_canvas.paste(iwall, (cx * 64, cy * 64), iwall)
# Door in center
shop_canvas.paste(door, (64, 64), door)
shop_canvas.save(os.path.join(OUT, "shop_built.png"))
print(f"  Saved shop_built.png (192x192 composed shop)")

# --- Create a field background (tileable grass) ---
grass_src = Image.open(os.path.join(LPC, "grass.png")).convert("RGBA")
grass_tile = grass_src.crop((0, 0, 32, 32))
field_bg = Image.new("RGBA", (800, 600), (0, 0, 0, 255))
for gx in range(0, 800, 32):
    for gy in range(0, 600, 32):
        field_bg.paste(grass_tile, (gx, gy), grass_tile)
field_bg.save(os.path.join(OUT, "field_bg.png"))
print(f"  Saved field_bg.png (800x600 grass tiled)")

# --- Create a map background (same grass tiled) ---
field_bg.save(os.path.join(OUT, "map_bg.png"))
print(f"  Saved map_bg.png (800x600 grass tiled)")

# --- Create a house interior background ---
floor_src = Image.open(os.path.join(LPC, "inside.png")).convert("RGBA")
floor_tile = floor_src.crop((0, 0, 32, 32))
house_bg = Image.new("RGBA", (800, 600), (0, 0, 0, 255))
for gx in range(0, 800, 32):
    for gy in range(0, 600, 32):
        house_bg.paste(floor_tile, (gx, gy), floor_tile)
house_bg.save(os.path.join(OUT, "house_bg.png"))
print(f"  Saved house_bg.png (800x600 floor tiled)")

print("\n=== Done! All tiles extracted to", OUT, "===")
