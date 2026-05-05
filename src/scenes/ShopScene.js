import Phaser from 'phaser';

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

        this.add.text(CX, 160, '── MUA ──', { fontSize: '18px', color: '#e67e22', fontStyle: 'bold' }).setOrigin(0.5);
        this.moneyT = this.add.text(CX, 190, '', { fontSize: '15px', color: '#f1c40f', fontStyle: 'bold', stroke: '#000', strokeThickness: 2 }).setOrigin(0.5);

        const items = [
            { name: '🍅 Hạt Cà Chua', key: 'seed_tomato', cost: 20 },
            { name: '🥬 Hạt Bắp Cải', key: 'seed_cabbage', cost: 35 },
        ];
        items.forEach((it, i) => {
            const y = 235 + i * 55;
            this.add.text(CX - 196, y, it.name, { fontSize: '15px', color: '#ecf0f1', fontStyle: 'bold' });
            this.add.text(CX + 24, y, `$${it.cost}`, { fontSize: '15px', color: '#f39c12', fontStyle: 'bold' });
            const b = this.add.rectangle(CX + 144, y + 5, 80, 30, 0x27ae60).setInteractive({ useHandCursor: true }).setStrokeStyle(2, 0x1e8449);
            this.add.text(CX + 144, y + 5, 'Mua', { fontSize: '13px', color: '#fff', fontStyle: 'bold' }).setOrigin(0.5);
            b.on('pointerdown', () => this.buy(it.key, it.cost));
            b.on('pointerover', () => b.setFillStyle(0x2ecc71));
            b.on('pointerout', () => b.setFillStyle(0x27ae60));
        });

        this.add.text(CX, 380, '── BÁN ──', { fontSize: '18px', color: '#27ae60', fontStyle: 'bold' }).setOrigin(0.5);
        this.sellT = this.add.text(CX, 415, '', { fontSize: '13px', color: '#bdc3c7', lineSpacing: 5 }).setOrigin(0.5);

        const sellBtn = this.add.rectangle(CX, 475, 200, 40, 0xe74c3c).setInteractive({ useHandCursor: true }).setStrokeStyle(2, 0xc0392b);
        this.add.text(CX, 475, '💰 Bán tất cả', { fontSize: '15px', color: '#fff', fontStyle: 'bold' }).setOrigin(0.5);
        sellBtn.on('pointerdown', () => this.sellAll());

        const back = this.add.rectangle(CX, 535, 200, 40, 0x7f8c8d).setInteractive({ useHandCursor: true }).setStrokeStyle(2, 0x6c7a7d);
        this.add.text(CX, 535, '← Về bản đồ', { fontSize: '15px', color: '#fff', fontStyle: 'bold' }).setOrigin(0.5);
        back.on('pointerdown', () => this.scene.switch('MapScene'));

        this.upd(); this.events.on('wake', () => this.upd());
    }

    upd() {
        const i = window.GameState.inventory;
        this.moneyT.setText(`💰 Tiền: $${window.GameState.money}`);
        this.sellT.setText(`🍅 Cà chua: ${i.tomato||0} ($40/cái)\n🥬 Bắp cải: ${i.cabbage||0} ($70/cái)`);
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
        const i = window.GameState.inventory;
        let e = (i.tomato||0)*40 + (i.cabbage||0)*70;
        i.tomato = 0; i.cabbage = 0;
        if (e > 0) { window.GameState.money += e; this.upd(); this.game.events.emit('updateHUD'); this.float(`+$${e} 💰`, '#f1c40f'); }
        else this.float('Không có gì!', '#e74c3c');
    }

    float(text, color) {
        const t = this.add.text(CX, 300, text, { fontSize: '18px', color, stroke: '#000', strokeThickness: 3, fontStyle: 'bold' }).setOrigin(0.5);
        this.tweens.add({ targets: t, y: 250, alpha: 0, duration: 1200, onComplete: () => t.destroy() });
    }
}
