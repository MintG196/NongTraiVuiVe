"""
Compose a proper LPC house at NATIVE 32x32 tile size first, then scale up.
house.png is 288x224 = 9 cols x 7 rows of 32x32.

Tile map (from debug grid):
Row 0: brick_TL | brick_TM | brick_TR | door_T  | beam   | pump_T |      | window_TL | window_TR
Row 1: brick_ML | brick_MM | brick_MR | door_B  | door2  | pump_B |      | window_BL | window_BR
Row 2: brick_BL | brick_BM | brick_BR |         | ornmnt |        |      | column_T  | column_TB
Row 3: roof_L   | roof_M   | roof_R   | roof_F  | roof_F |        |      |           | column
Row 4: wall_L   | wall_win | wall_R   | wall_F  | wall_F |        |      | col_base  | col_base
Row 5: stair_L  | stair_M  | stair_R  | floor_F | floor_F|        |      |           |
Row 6: corner_L | floor    | corner_R | floor   | floor  |        |      |           |

House composition (5 wide x 5 tall at 32px = 160x160 native):
  Row 0: roof peaked
  Row 1: roof wall / upper storey
  Row 2: brick wall top
  Row 3: brick wall mid + door center + windows sides
  Row 4: brick wall bottom + door bottom + windows bottom
"""
from PIL import Image
import os

OUT = r"D:\Nong Trai\public\assets"
src = Image.open(r"D:\Nong Trai\LPC Base Assets\tiles\house.png").convert("RGBA")

def t(col, row):
    """Get 32x32 tile at grid position."""
    return src.crop((col*32, row*32, col*32+32, row*32+32))

def mirror(tile):
    return tile.transpose(Image.FLIP_LEFT_RIGHT)

# ============================================================
# HOUSE (5 tiles wide x 5 tiles tall = 160x160, then scale 3x = 480x480)
# ============================================================
house = Image.new("RGBA", (160, 160), (0,0,0,0))

# Row 0: ROOF (from spritesheet row 3)
house.paste(t(0,3), (0,0), t(0,3))      # Roof left peak
house.paste(t(1,3), (32,0), t(1,3))     # Roof middle
house.paste(t(3,3), (64,0), t(3,3))     # Roof flat center
house.paste(mirror(t(1,3)), (96,0), mirror(t(1,3)))   # Mirror middle
house.paste(mirror(t(0,3)), (128,0), mirror(t(0,3)))  # Mirror left peak

# Row 1: Upper grey wall below roof (from spritesheet row 4)
house.paste(t(0,4), (0,32), t(0,4))
house.paste(t(3,4), (32,32), t(3,4))
house.paste(t(1,4), (64,32), t(1,4))    # Grey wall with small window
house.paste(t(3,4), (96,32), t(3,4))
house.paste(mirror(t(0,4)), (128,32), mirror(t(0,4)))

# Row 2: Brick wall top (from spritesheet row 0)
house.paste(t(0,0), (0,64), t(0,0))
house.paste(t(1,0), (32,64), t(1,0))
house.paste(t(1,0), (64,64), t(1,0))
house.paste(t(1,0), (96,64), t(1,0))
house.paste(t(2,0), (128,64), t(2,0))

# Row 3: Brick wall mid + windows + door top (row 1 + door from row 0 col 3)
house.paste(t(7,0), (0,96), t(7,0))      # Window TL
house.paste(t(1,1), (32,96), t(1,1))     # Brick mid
house.paste(t(3,0), (64,96), t(3,0))     # Door top
house.paste(t(1,1), (96,96), t(1,1))     # Brick mid
house.paste(mirror(t(7,0)), (128,96), mirror(t(7,0)))  # Window TR (mirrored)

# Row 4: Brick wall bottom + window bottom + door bottom (row 2 + door row 1 col 3)
house.paste(t(7,1), (0,128), t(7,1))     # Window BL
house.paste(t(1,2), (32,128), t(1,2))    # Brick bottom
house.paste(t(3,1), (64,128), t(3,1))    # Door bottom
house.paste(t(1,2), (96,128), t(1,2))    # Brick bottom
house.paste(mirror(t(7,1)), (128,128), mirror(t(7,1)))  # Window BR (mirrored)

# Scale up 3x for the game (160 -> 480)
house_big = house.resize((480, 480), Image.NEAREST)
house_big.save(os.path.join(OUT, "house_lpc.png"))
print("Saved house_lpc.png (480x480)")

# ============================================================
# SHOP (5 wide x 5 tall, all grey/purple style)
# ============================================================
shop = Image.new("RGBA", (160, 160), (0,0,0,0))

# Row 0: Same roof
shop.paste(t(0,3), (0,0), t(0,3))
shop.paste(t(1,3), (32,0), t(1,3))
shop.paste(t(3,3), (64,0), t(3,3))
shop.paste(mirror(t(1,3)), (96,0), mirror(t(1,3)))
shop.paste(mirror(t(0,3)), (128,0), mirror(t(0,3)))

# Row 1: Grey wall (row 4)
shop.paste(t(0,4), (0,32), t(0,4))
shop.paste(t(1,4), (32,32), t(1,4))   # Window
shop.paste(t(3,4), (64,32), t(3,4))
shop.paste(mirror(t(1,4)), (96,32), mirror(t(1,4)))  # Window mirrored
shop.paste(mirror(t(0,4)), (128,32), mirror(t(0,4)))

# Row 2: Grey wall continued
shop.paste(t(0,4), (0,64), t(0,4))
shop.paste(t(3,4), (32,64), t(3,4))
shop.paste(t(3,4), (64,64), t(3,4))
shop.paste(t(3,4), (96,64), t(3,4))
shop.paste(mirror(t(0,4)), (128,64), mirror(t(0,4)))

# Row 3: Grey wall + windows + door
shop.paste(t(7,0), (0,96), t(7,0))
shop.paste(t(3,4), (32,96), t(3,4))
shop.paste(t(3,0), (64,96), t(3,0))     # Door top
shop.paste(t(3,4), (96,96), t(3,4))
shop.paste(mirror(t(7,0)), (128,96), mirror(t(7,0)))

# Row 4: Bottom + door bottom
shop.paste(t(7,1), (0,128), t(7,1))
shop.paste(t(3,5), (32,128), t(3,5))    # Grey floor
shop.paste(t(3,1), (64,128), t(3,1))    # Door bottom
shop.paste(t(3,5), (96,128), t(3,5))
shop.paste(mirror(t(7,1)), (128,128), mirror(t(7,1)))

shop_big = shop.resize((480, 480), Image.NEAREST)
shop_big.save(os.path.join(OUT, "shop_lpc.png"))
print("Saved shop_lpc.png (480x480)")

print("\nDone! Both buildings composed at native 32x32 then scaled 3x.")
