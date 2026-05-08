# 🌾 Sửa Lỗi Hệ Thống Phát Triển Cây Trồng

## ❌ Lỗi Ban Đầu

Các cây trồng có thể được thu hoạch ngay từ khi vừa trồng mà không cần chờ phát triển đủ. Điều này xảy ra vì:

1. **Không có cơ chế tăng growth**: Giá trị `p.growth` được set = 0 khi trồng nhưng không bao giờ tăng
2. **Hardcoded thresholds sai**: 
   - Cà chua = 2 (nhưng thực tế cần 15 ngày)
   - Bắp cải = 3 (nhưng thực tế cần 14 ngày)
3. **Watering logic lỗi**: Chỉ crops được tưới mới mọc
   - Cũ: `if (p.crop && p.watered) p.growth++;`
   - Vấn đề: Crops không tưới sẽ không mọc!

## ✅ Sửa Chữa

### 1️⃣ Tạo File CropData.js

**Vị trí**: `src/CropData.js`

File này định nghĩa tất cả crops với:
- **maturityDays**: Tổng số ngày cần thiết để chín
- **stages**: Các bước phát triển với emoji display
- **regrows**: Có mọc lại sau khi thu hoạch không (Corn, Hot Pepper, Green Bean, v.v.)

**Dữ liệu dựa vào Stardew Valley standards:**
```
Parsnip (Cà rốt trắng):  6 ngày
Potato (Khoai tây):      6 ngày
Tomato (Cà chua):        15 ngày ⭐
Cabbage (Bắp cải):       14 ngày ⭐
Corn (Bắp):              14 ngày (regrows)
Melon (Dưa):             12 ngày
Pumpkin (Bí ngô):        13 ngày
Hot Pepper (Ớt cay):     10 ngày (regrows)
Green Bean (Đậu xanh):   10 ngày (regrows)
```

### 2️⃣ Cập Nhật FieldScene.js

**Thay đổi 3 chỗ:**

**A) Import CropData:**
```javascript
import { getCropData, getGrowthStage } from '../CropData.js';
```

**B) Sửa handlePlotClick() - Harvest Logic:**
- Thay vì check `p.growth >= 2` hoặc `>= 3`
- Giờ check: `p.growth >= cropData.maturityDays`
- Nếu chưa chín: hiện "Chưa chín! (X ngày)"

**C) Sửa updateFieldVisuals() - Display:**
- Dùng `getGrowthStage()` để lấy đúng emoji
- Hiển thị 🌱 → 🌿 → 🌿 → ... → 🍅 (tùy loại crop)

### 3️⃣ Cập Nhật HouseScene.js

**Sửa endDay() - Growth Mechanics:**

**CŨ (SAI):**
```javascript
s.plots.forEach(p => { if (p.crop && p.watered) p.growth++; p.watered = false; });
```

**MỚI (ĐÚNG):**
```javascript
s.plots.forEach(p => { if (p.crop) p.growth++; p.watered = false; });
```

**Lý do:** 
- Tất cả crops phải mọc mỗi ngày, dù có tưới hay không
- Watering sẽ ảnh hưởng đến quality/other factors (có thể thêm sau)

## 🎮 Cách Hoạt Động

### Quy Trình Một Ngày:

1. **Người chơi trồng hạt**: `growth = 0`, `watered = false`
2. **Người chơi tưới nước** (tuỳ chọn): `watered = true`
3. **Người chơi đi ngủ**: Kích hoạt `endDay()`
   - `growth` tăng thêm 1
   - `watered` reset về false
   - Ngày tăng lên 1
4. **Hôm sau**: Người chơi có thể:
   - Tưới lại nước
   - Kiểm tra trạng thái crop (emoji khác nhau)
   - Thu hoạch nếu `growth >= maturityDays`

### Ví Dụ: Cà Chua (Tomato)
```
Ngày 1: Trồng hạt          → growth=0, emoji=🌱
Ngày 2: Đi ngủ            → growth=1, emoji=🌿
Ngày 3: growth=2          → emoji=🌿
...
Ngày 15: growth=14        → emoji=🌿 (chưa chín)
Ngày 16: Đi ngủ           → growth=15 ✅ CHÍN, emoji=🍅
→ Có thể thu hoạch ngay hôm nay!
```

## 📊 Growth Stages (Cà Chua - Ví Dụ)

| Growth Value | Ngày | Emoji | Trạng Thái |
|---|---|---|---|
| 0 | 1 | 🌱 | Hạt vừa gieo |
| 1-2 | 2-3 | 🌿 | Mầm non |
| 3-5 | 4-6 | 🌿 | Cây con |
| 6-8 | 7-9 | 🌿 | Cây lớn |
| 9-11 | 10-12 | 🌿 | Ra hoa |
| 12-14 | 13-15 | 🌿 | Đang nở quả |
| **15+** | **16+** | **🍅** | **CHÍN - THU HOẠCH** |

## 🔍 Cách Kiểm Tra Lỗi Đã Sửa

### Test Case 1: Crops mọc không phải chỉ khi tưới
- Trồng 2 cà chua
- Cây A: tưới nước mỗi ngày
- Cây B: không tưới
- Ngày 16: Cả hai cây phải chín và có thể thu hoạch ✅

### Test Case 2: Crops chỉ thu hoạch khi đủ ngày
- Trồng cà chua ngày 1
- Cố gắng thu hoạch ngày 2-15: "Chưa chín! (X ngày)" ✅
- Ngày 16 trở đi: Thu hoạch thành công ✅

### Test Case 3: Khác loại crop, khác thời gian
- Parsnip (6 ngày): Thu hoạch được ngày 7
- Cabbage (14 ngày): Thu hoạch được ngày 15
- Tomato (15 ngày): Thu hoạch được ngày 16

## 📝 Thêm Crops Mới

Để thêm crop mới, chỉnh sửa `CropData.js`:

```javascript
yourCrop: {
    name: 'Tên tiếng Việt',
    icon: '🎯',  // Emoji icon
    maturityDays: 10,
    stages: [
        { daysNeeded: 0, emoji: '🌱' },
        { daysNeeded: 3, emoji: '🌿' },
        { daysNeeded: 6, emoji: '🌿' },
        { daysNeeded: 10, emoji: '🎯' },  // Mature state
    ],
    regrows: false,  // true nếu có thể mọc lại
}
```

Sau đó thêm seed vào `GameState.inventory` ở `main.js`:
```javascript
inventory: { seed_tomato: 2, seed_cabbage: 0, seed_yourCrop: 5, ... }
```

## 🐛 Nếu Còn Lỗi

**Problem**: Crops vẫn không mọc
- Check: Có gọi `endDay()` không?
- Check: `HouseScene.js` line với `if (p.crop) p.growth++;`

**Problem**: Crops không display đúng emoji
- Check: `CropData.js` có định nghĩa crop loại đó không?
- Check: `FieldScene.js` import `getGrowthStage` chưa?

**Problem**: Thu hoạch lúc chưa chín
- Check: `handlePlotClick()` logic có xài `cropData.maturityDays` không?

---

**Hoàn thành ngày:** May 8, 2026
**Phiên bản:** 1.0 - Fix Growth Mechanics
