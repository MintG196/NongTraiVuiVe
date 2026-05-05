"""
Fix: Extract the CORRECT grass and dirt tiles from LPC.
LPC autotile layout: the solid center fill is at grid (1,2) for most tilesets.
Also, the grass.png uses a different autotile format.
Let's inspect and pick the right ones.
"""
from PIL import Image
import os

OUT = r"D:\Nong Trai\public\assets"
LPC = r"D:\Nong Trai\LPC Base Assets\tiles"

def save(img, name, scale=1):
    if scale > 1:
        img = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
    img.save(os.path.join(OUT, name))
    print(f"  Saved {name} ({img.width}x{img.height})")

# === GRASS ===
# grass.png is 96x192. Let's look at the autotile layout.
# For LPC, the pure grass fill tile is at the BOTTOM row, left tile
grass_img = Image.open(os.path.join(LPC, "grass.png")).convert("RGBA")
print(f"grass.png size: {grass_img.size}")
# The bottom of grass.png (y=160) should have the pure fill
# Actually in LPC autotile, the solid fill is at position (1,1) in a 3-column layout
# grass.png is 96x192 = 3 cols x 6 rows of 32x32
# Let's try row 5 (bottom), col 1 (center) = pure green
grass_tile = grass_img.crop((32, 160, 64, 192))
save(grass_tile, "grass.png", scale=2)

# === DIRT (farmable soil) ===
dirt_img = Image.open(os.path.join(LPC, "dirt2.png")).convert("RGBA")
print(f"dirt2.png size: {dirt_img.size}")
# Same autotile format. Solid fill = row 5, col 1
dirt_tile = dirt_img.crop((32, 160, 64, 192))
save(dirt_tile, "dirt.png", scale=2)

# Wet dirt (watered)
dirt1_img = Image.open(os.path.join(LPC, "dirt.png")).convert("RGBA")
dirt_wet = dirt1_img.crop((32, 160, 64, 192))
save(dirt_wet, "dirt_wet.png", scale=2)

# === Rebuild grass background with proper tile ===
grass_clean = Image.open(os.path.join(OUT, "grass.png")).convert("RGBA")
bg = Image.new("RGBA", (800, 600), (0, 0, 0, 255))
gw, gh = grass_clean.size
for x in range(0, 800, gw):
    for y in range(0, 600, gh):
        bg.paste(grass_clean, (x, y), grass_clean)
bg.save(os.path.join(OUT, "map_bg.png"))
bg.save(os.path.join(OUT, "field_bg.png"))
print("  Saved map_bg.png and field_bg.png (800x600)")

# === Rebuild house interior with proper floor ===
inside_img = Image.open(os.path.join(LPC, "inside.png")).convert("RGBA")
print(f"inside.png size: {inside_img.size}")
# Floor tile - inside.png top section has wall tiles. 
# The floor is typically the lighter colored area
# Let's use castlefloors.png for a nice wooden floor
castlefloor_img = Image.open(os.path.join(LPC, "castlefloors.png")).convert("RGBA")
print(f"castlefloors.png size: {castlefloor_img.size}")
# Wooden floor tile is usually in the bottom rows
floor_tile = castlefloor_img.crop((32, 160, 64, 192)).resize((64, 64), Image.NEAREST)
house_bg = Image.new("RGBA", (800, 600), (0, 0, 0, 255))
for x in range(0, 800, 64):
    for y in range(0, 600, 64):
        house_bg.paste(floor_tile, (x, y), floor_tile)
house_bg.save(os.path.join(OUT, "house_bg.png"))
print("  Saved house_bg.png (800x600)")

print("\n=== Fix complete! ===")
