import Phaser from 'phaser';
import { CROPS } from '../data/crops.js';


const GW = 864, GH = 672, CX = GW / 2;

export default class ShopScene extends Phaser.Scene {
    constructor() { super('ShopScene'); }

    create() {
        this.add.image(0, 0, 'house_bg').setOrigin(0).setDisplaySize(GW, GH);
        const g = this.add.graphics();
        g.fillStyle(0xCD853F); g.fillRect(0, 0, GW, 80);
        g.fillStyle(0x8B6914); g.fillRect(0, 75, GW, 5);

        this.add.text(CX, 95, '🏪 CỬA HÀNG', { fontSize: '24px', fontFamily: '"Press Start 2P", monospace', color: '#f1c40f', stroke: '#8B4513', strokeThickness: 5 }).setOrigin(0.5);
        this.add.image(90, 200, 'barrel').setScale(0.9);
        this.add.image(GW - 90, 200, 'barrel').setScale(0.9);

        const p = this.add.graphics();
        p.fillStyle(0x2c3e50, 0.92); p.fillRoundedRect(CX-266, 135, 532, 420, 15);
        p.lineStyle(3, 0xd35400); p.strokeRoundedRect(CX-266, 135, 532, 420, 15);

        this.add.text(CX, 160, '── MUA HẠT GIỐNG ──', { fontSize: '18px', color: '#e67e22', fontStyle: 'bold' }).setOrigin(0.5);
        this.moneyT = this.add.text(CX, 190, '', { fontSize: '15px', color: '#f1c40f', fontStyle: 'bold', stroke: '#000', strokeThickness: 2 }).setOrigin(0.5);

        // Scrollable area for buying
        const mask = this.add.graphics().fillRect(CX - 250, 210, 500, 160).setVisible(false).createGeometryMask();
        this.shopContainer = this.add.container(0, 0);
        this.shopContainer.setMask(mask);

        const cropKeys = Object.keys(CROPS);
        cropKeys.forEach((key, i) => {
            const it = CROPS[key];
            const y = 230 + i * 45;
            const itemText = this.add.text(CX - 220, y, `${it.icon} Hạt ${it.name}`, { fontSize: '14px', color: '#ecf0f1', fontStyle: 'bold' });
            const costText = this.add.text(CX + 20, y, `$${it.cost}`, { fontSize: '14px', color: '#f39c12', fontStyle: 'bold' });
            const b = this.add.rectangle(CX + 140, y + 5, 80, 28, 0x27ae60).setInteractive({ useHandCursor: true }).setStrokeStyle(2, 0x1e8449);
            const bText = this.add.text(CX + 140, y + 5, 'Mua', { fontSize: '12px', color: '#fff', fontStyle: 'bold' }).setOrigin(0.5);
            
            b.on('pointerdown', () => this.buy(`seed_${key}`, it.cost));
            b.on('pointerover', () => b.setFillStyle(0x2ecc71));
            b.on('pointerout', () => b.setFillStyle(0x27ae60));
            
            this.shopContainer.add([itemText, costText, b, bText]);
        });

        // Add scrolling logic
        this.input.on('wheel', (pointer, gameObjects, deltaX, deltaY, deltaZ) => {
            const minY = -(cropKeys.length * 45 - 140);
            this.shopContainer.y = Phaser.Math.Clamp(this.shopContainer.y - deltaY, minY, 0);
        });


        this.add.text(CX, 390, '── BÁN NÔNG SẢN ──', { fontSize: '18px', color: '#27ae60', fontStyle: 'bold' }).setOrigin(0.5);
        this.sellT = this.add.text(CX, 430, '', { fontSize: '13px', color: '#bdc3c7', lineSpacing: 5, align: 'center' }).setOrigin(0.5);


        const sellBtn = this.add.rectangle(CX, 475, 200, 40, 0xe74c3c).setInteractive({ useHandCursor: true }).setStrokeStyle(2, 0xc0392b);
        this.add.text(CX, 475, '💰 Bán tất cả', { fontSize: '15px', color: '#fff', fontStyle: 'bold' }).setOrigin(0.5);
        sellBtn.on('pointerdown', () => this.sellAll());

        const back = this.add.rectangle(CX, 535, 200, 40, 0x7f8c8d).setInteractive({ useHandCursor: true }).setStrokeStyle(2, 0x6c7a7d);
        this.add.text(CX, 535, '← Về bản đồ', { fontSize: '15px', color: '#fff', fontStyle: 'bold' }).setOrigin(0.5);
        back.on('pointerdown', () => this.scene.switch('MapScene'));

        this.upd(); this.events.on('wake', () => this.upd());
    }

    upd() {
        const inv = window.GameState.inventory;
        this.moneyT.setText(`💰 Tiền của bạn: $${window.GameState.money}`);
        
        let stockText = "";
        let count = 0;
        Object.keys(CROPS).forEach(key => {
            if (inv[key] > 0) {
                stockText += `${CROPS[key].icon} ${CROPS[key].name}: ${inv[key]}  `;
                count++;
                if (count % 3 === 0) stockText += "\n";
            }
        });
        this.sellT.setText(stockText || "Bạn không có nông sản nào để bán.");
    }


    buy(key, cost) {
        if (window.GameState.money >= cost) {
            window.GameState.money -= cost;
            window.GameState.inventory[key] = (window.GameState.inventory[key] || 0) + 1;
            this.upd(); this.game.events.emit('updateHUD');
            this.float('Đã mua! ✅', '#2ecc71');
        } else this.float('Không đủ tiền! ❌', '#e74c3c');
    }

    sellAll() {
        const inv = window.GameState.inventory;
        let totalEarned = 0;
        Object.keys(CROPS).forEach(key => {
            if (inv[key] > 0) {
                totalEarned += inv[key] * CROPS[key].sell;
                inv[key] = 0;
            }
        });
        
        if (totalEarned > 0) { 
            window.GameState.money += totalEarned; 
            this.upd(); 
            this.game.events.emit('updateHUD'); 
            this.float(`Đã bán hết! +$${totalEarned} 💰`, '#f1c40f'); 
        }
        else this.float('Không có gì để bán!', '#e74c3c');
    }


    float(text, color) {
        const t = this.add.text(CX, 300, text, { fontSize: '18px', color, stroke: '#000', strokeThickness: 3, fontStyle: 'bold' }).setOrigin(0.5);
        this.tweens.add({ targets: t, y: 250, alpha: 0, duration: 1200, onComplete: () => t.destroy() });
    }
}
