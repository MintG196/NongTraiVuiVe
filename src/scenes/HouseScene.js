import Phaser from 'phaser';

const GW = 864, GH = 672;

export default class HouseScene extends Phaser.Scene {
    constructor() { super('HouseScene'); }

    create() {
        this.add.image(0, 0, 'house_bg').setOrigin(0).setDisplaySize(GW, GH);
        const g = this.add.graphics();
        g.fillStyle(0x8B4513, 1); g.fillRect(0, 0, GW, 80);
        g.fillStyle(0x654321, 1); g.fillRect(0, 75, GW, 5);

        this.add.image(700, 180, 'bed').setScale(1.1);
        this.add.image(160, 140, 'chest').setScale(1.3);
        this.add.image(110, 400, 'barrel').setScale(1);

        this.add.text(GW/2, 95, '🏠 TRONG NHÀ', {
            fontSize: '24px', fontFamily: '"Press Start 2P", monospace',
            color: '#f1c40f', stroke: '#654321', strokeThickness: 5,
        }).setOrigin(0.5);

        const p = this.add.graphics();
        p.fillStyle(0x34495e, 0.9); p.fillRoundedRect(GW/2-200, 170, 400, 340, 15);
        p.lineStyle(3, 0x2c3e50); p.strokeRoundedRect(GW/2-200, 170, 400, 340, 15);

        this.dayT = this.add.text(GW/2, 210, '', { fontSize: '20px', color: '#ecf0f1', fontStyle: 'bold', stroke: '#000', strokeThickness: 2 }).setOrigin(0.5);
        this.monT = this.add.text(GW/2, 250, '', { fontSize: '20px', color: '#f1c40f', fontStyle: 'bold', stroke: '#000', strokeThickness: 2 }).setOrigin(0.5);
        this.engT = this.add.text(GW/2, 290, '', { fontSize: '20px', color: '#2ecc71', fontStyle: 'bold', stroke: '#000', strokeThickness: 2 }).setOrigin(0.5);

        this.makeBtn(GW/2, 360, 250, 50, 0x8e44ad, '🌙 Đi ngủ (Qua ngày)', () => this.endDay());
        this.makeBtn(GW/2, 430, 250, 50, 0x2980b9, '← Về bản đồ', () => this.scene.switch('MapScene'));

        this.upd(); this.events.on('wake', () => this.upd());
    }

    makeBtn(x, y, w, h, color, label, cb) {
        const b = this.add.rectangle(x, y, w, h, color).setInteractive({ useHandCursor: true }).setStrokeStyle(3, Phaser.Display.Color.IntegerToColor(color).darken(20).color);
        this.add.text(x, y, label, { fontSize: '15px', color: '#fff', fontStyle: 'bold' }).setOrigin(0.5);
        b.on('pointerdown', cb);
        b.on('pointerover', () => b.setAlpha(0.85));
        b.on('pointerout', () => b.setAlpha(1));
    }

    upd() {
        const s = window.GameState;
        this.dayT.setText(`📅 Ngày: ${s.day}`);
        this.monT.setText(`💰 Tiền: $${s.money}`);
        this.engT.setText(`💚 Năng lượng: ${s.energy}/${s.maxEnergy}`);
    }

    endDay() {
        const s = window.GameState;
        s.day++; s.energy = s.maxEnergy;
        // Crops grow every day, watered or not. Watering just helps quality/other factors
        s.plots.forEach(p => { if (p.crop) p.growth++; p.watered = false; });
        this.game.events.emit('updateHUD');
        this.cameras.main.fadeOut(600, 0, 0, 30);
        this.cameras.main.once(Phaser.Cameras.Scene2D.Events.FADE_OUT_COMPLETE, () => {
            this.upd();
            this.cameras.main.fadeIn(600, 0, 0, 30);
            const t = this.add.text(GW/2, 336, `☀️ Ngày ${s.day}!`, { fontSize: '22px', color: '#f1c40f', stroke: '#000', strokeThickness: 4, fontStyle: 'bold' }).setOrigin(0.5);
            this.tweens.add({ targets: t, y: 280, alpha: 0, duration: 2000, onComplete: () => t.destroy() });
        });
    }
}
