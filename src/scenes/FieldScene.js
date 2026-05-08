import Phaser from 'phaser';
const TILE = 64;

// Crop maturity days = actual growth frame count from PNG tilesets (480x416 / 32px = 15 frames max)
const CROP_MATURITY = {
    // Spring Crops
    parsnip: 6,
    cauliflower: 12,
    potato: 10,
    garlic: 6,
    rhubarb: 8,
    greenbean: 8,
    strawberry: 8,
    // Summer Crops
    blueberry: 12,
    melon: 12,
    corn: 13,
    hotpepper: 12,
    starfruit: 8,
    eggplant: 11,
    tomato: 13,
    sunflower: 10,
    pumpkin: 10,
    wheat: 8,
    cranberries: 12,
    // Fall Crops
    bokchoy: 7,
    carrot: 10,
    radish: 7,
    redcabbage: 9,
    yam: 10,
    // Other
    beet: 10,
    pineapple: 12,
    giantpumpkin: 12,
    giantcauliflower: 12,
    giantmelon: 13,
};

const CROP_ICONS = { 
    tomato: '🍅', cabbage: '🥬', corn: '🌽', melon: '🍈', pumpkin: '🎃', 
    hotpepper: '🌶️', eggplant: '🍆', parsnip: '🥕', potato: '🥔', cauliflower: '🥦', 
    greenbean: '🫘', carrot: '🥕', yam: '🍠', blueberry: '🫐', starfruit: '⭐'
};

function getGrowthStage(cropType, growthValue) {
    const maturity = CROP_MATURITY[cropType] || 12;
    const icon = CROP_ICONS[cropType] || '🌱';
    
    // Simple 3-state display
    if (growthValue === 0) {
        return { emoji: '🌱', isMatured: false, maturityDays: maturity };
    } else if (growthValue >= maturity) {
        return { emoji: icon, isMatured: true, maturityDays: maturity };
    } else {
        return { emoji: '🌿', isMatured: false, maturityDays: maturity };
    }
}

export default class FieldScene extends Phaser.Scene {
    constructor() { super('FieldScene'); this.plotSprites = []; this.selectedToolIdx = 0; this.toolButtons = []; }

    create() {
        this.add.image(0, 0, 'field_bg').setOrigin(0, 0).setDisplaySize(864, 672);
        this.plotSprites = []; this.toolButtons = [];

        this.add.text(432, 20, '🌾 VƯỜN RAU', {
            fontSize: '22px', fontFamily: '"Press Start 2P", monospace',
            color: '#fff', stroke: '#2d572c', strokeThickness: 4,
        }).setOrigin(0.5);

        // 4x3 grid of plots (centered)
        const cols = 4, rows = 3;
        const startX = (864 - cols * TILE) / 2;
        const startY = 60;

        const border = this.add.graphics();
        border.lineStyle(4, 0x4e342e);
        border.strokeRect(startX - 6, startY - 6, cols * TILE + 12, rows * TILE + 12);
        border.fillStyle(0x3a2a1a, 0.3);
        border.fillRect(startX - 6, startY - 6, cols * TILE + 12, rows * TILE + 12);

        for (let r = 0; r < rows; r++) {
            for (let c = 0; c < cols; c++) {
                const x = startX + c * TILE + TILE / 2;
                const y = startY + r * TILE + TILE / 2;
                const idx = r * cols + c;

                const plot = this.add.image(x, y, 'dirt').setDisplaySize(TILE, TILE)
                    .setInteractive({ useHandCursor: true });
                // Create crop as IMAGE sprite (not text) to support frame slicing
                const cropImage = this.add.image(x, y, 'parsnip').setDisplaySize(TILE, TILE).setVisible(false);
                const stateText = this.add.text(x + 20, y + 20, '', { fontSize: '12px' }).setOrigin(0.5);

                plot.on('pointerdown', () => this.handlePlotClick(idx, x, y));
                plot.on('pointerover', () => plot.setAlpha(0.8));
                plot.on('pointerout', () => plot.setAlpha(1));
                this.plotSprites.push({ plot, cropImage, stateText });
            }
        }

        // Toolbar
        const tbY = 590;
        this.add.graphics().fillStyle(0x2c3e50, 0.92).fillRoundedRect(60, tbY - 35, 740, 70, 10);

        const tools = [
            { id: 'hand', icon: '✋', label: 'Thu hoạch' },
            { id: 'water', icon: '💧', label: 'Tưới' },
            { id: 'seed_tomato', icon: '🍅', label: 'Cà chua' },
            { id: 'seed_cabbage', icon: '🥬', label: 'Bắp cải' },
            { id: 'scythe', icon: '⚔️', label: 'Dọn' },
        ];
        const spacing = 120, sx = 432 - ((tools.length - 1) * spacing) / 2;
        tools.forEach((t, i) => {
            const tx = sx + i * spacing;
            const btn = this.add.rectangle(tx, tbY, 100, 50, i === 0 ? 0x27ae60 : 0x34495e)
                .setInteractive({ useHandCursor: true }).setStrokeStyle(2, 0x1a252f);
            this.add.text(tx - 25, tbY, t.icon, { fontSize: '18px' }).setOrigin(0.5);
            this.add.text(tx + 15, tbY, t.label, { fontSize: '11px', color: '#ecf0f1', fontStyle: 'bold' }).setOrigin(0.5);
            btn.on('pointerdown', () => { this.selectedToolIdx = i; window.GameState.tool = t.id; this.updateToolbar(); });
            this.toolButtons.push({ btn });
        });

        // Back & inventory
        const back = this.add.rectangle(780, tbY - 55, 100, 35, 0xc0392b).setInteractive({ useHandCursor: true }).setStrokeStyle(2, 0x922b21);
        this.add.text(780, tbY - 55, '← Bản đồ', { fontSize: '12px', color: '#fff', fontStyle: 'bold' }).setOrigin(0.5);
        back.on('pointerdown', () => this.scene.switch('MapScene'));

        this.invText = this.add.text(80, tbY - 55, '', { fontSize: '12px', color: '#f1c40f', stroke: '#000', strokeThickness: 2, lineSpacing: 3 });

        this.updateFieldVisuals(); this.updateInventoryText();
        this.events.on('wake', () => { this.updateFieldVisuals(); this.updateInventoryText(); });
    }

    updateToolbar() { this.toolButtons.forEach((tb, i) => tb.btn.setFillStyle(i === this.selectedToolIdx ? 0x27ae60 : 0x34495e)); }

    handlePlotClick(idx, px, py) {
        const p = window.GameState.plots[idx], t = window.GameState.tool, inv = window.GameState.inventory;
        if (t.startsWith('seed_')) {
            const type = t.replace('seed_', '');
            if (!p.crop && inv[t] > 0) { if (this.useEnergy(10)) { inv[t]--; p.crop = type; p.growth = 0; p.watered = false; this.float('Đã trồng 🌱', px, py, '#2ecc71'); } }
            else if (!p.crop) this.float('Hết hạt!', px, py, '#e74c3c');
        } else if (t === 'water') {
            if (p.crop && !p.watered) { if (this.useEnergy(5)) { p.watered = true; this.float('💧', px, py, '#3498db'); } }
        } else if (t === 'hand') {
            if (p.crop) { 
                const maturity = CROP_MATURITY[p.crop] || 15;
                const isMatured = p.growth >= maturity;
                if (isMatured) { 
                    if (this.useEnergy(5)) { 
                        inv[p.crop] = (inv[p.crop] || 0) + 1; 
                        const icon = CROP_ICONS[p.crop] || '🌱';
                        this.float(`+1 ${icon}`, px, py, '#f1c40f'); 
                        p.crop = null; 
                        p.growth = 0; 
                        p.watered = false; 
                    } 
                } else {
                    const daysLeft = maturity - p.growth;
                    this.float(`Chưa chín! (${daysLeft} ngày)`, px, py, '#e67e22');
                }
            }
        } else if (t === 'scythe' && p.crop) { if (this.useEnergy(10)) { p.crop=null; p.growth=0; p.watered=false; this.float('Dọn!',px,py,'#95a5a6'); } }
        this.updateFieldVisuals(); this.updateInventoryText();
    }

    useEnergy(n) { if (window.GameState.energy >= n) { window.GameState.energy -= n; this.game.events.emit('updateHUD'); return true; } this.float('Hết sức! Về ngủ.',432,336,'#e74c3c'); return false; }

    float(text, x, y, color = '#fff') {
        const t = this.add.text(x, y, text, { fontSize: '15px', color, stroke: '#000', strokeThickness: 3, fontStyle: 'bold' }).setOrigin(0.5);
        this.tweens.add({ targets: t, y: y - 50, alpha: 0, duration: 1000, ease: 'Power2', onComplete: () => t.destroy() });
    }

    updateFieldVisuals() {
        window.GameState.plots.forEach((pd, i) => {
            const v = this.plotSprites[i]; if (!v) return;
            v.plot.setTexture(pd.watered ? 'dirt_wet' : 'dirt').setDisplaySize(TILE, TILE);
            if (pd.crop) {
                // Calculate frame index from growth value (0 to maturity)
                const maturity = CROP_MATURITY[pd.crop] || 12;
                
                // Safety: Get actual frame count from the texture
                const texture = this.textures.get(pd.crop).getSourceImage();
                const framesInImage = texture.width > 0 ? Math.floor(texture.width / 16) : 0;
                
                // Clamp frameIndex to available frames in the image
                const maxFrame = framesInImage > 0 ? Math.min(maturity - 1, framesInImage - 1) : maturity - 1;
                const frameIndex = Math.min(Math.max(0, pd.growth), maxFrame);
                
                // Each frame is 16px wide (Standard Stardew Tileset)
                const frameWidth = 16;
                const sourceX = frameIndex * frameWidth;
                
                // Load crop texture
                v.cropImage.setTexture(pd.crop).setDisplaySize(TILE, TILE);
                // Crop only the 16x32 (or 16x64) area for the current stage
                const texHeight = texture.height || 32;
                v.cropImage.setCrop(sourceX, 0, frameWidth, texHeight);
                v.cropImage.setVisible(true);
                v.stateText.setText(pd.watered ? '💧' : '');
            } else {
                v.cropImage.setVisible(false);
                v.stateText.setText('');
            }
        });
    }

    updateInventoryText() {
        const i = window.GameState.inventory;
        this.invText.setText(`🍅Hạt:${i.seed_tomato||0} 🥬Hạt:${i.seed_cabbage||0} | 🍅:${i.tomato||0} 🥬:${i.cabbage||0}`);
    }
}
