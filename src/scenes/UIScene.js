import Phaser from 'phaser';

export default class UIScene extends Phaser.Scene {
    constructor() { super({ key: 'UIScene', active: false }); }

    create() {
        const ep = this.add.graphics();
        ep.fillStyle(0x000000, 0.5); ep.fillRoundedRect(692, 8, 160, 36, 8);
        this.heart = this.add.text(712, 26, '💚', { fontSize: '20px' }).setOrigin(0.5);
        this.energyT = this.add.text(792, 26, '100', { fontSize: '18px', fontStyle: 'bold', color: '#2ecc71', stroke: '#000', strokeThickness: 3 }).setOrigin(0.5);

        const ip = this.add.graphics();
        ip.fillStyle(0x2980b9, 0.85); ip.fillRoundedRect(8, 8, 190, 70, 10);
        ip.lineStyle(2, 0x1f618d); ip.strokeRoundedRect(8, 8, 190, 70, 10);
        this.dayT = this.add.text(20, 18, '📅 Ngày: 1', { fontSize: '16px', fontStyle: 'bold', color: '#ecf0f1', stroke: '#000', strokeThickness: 2 });
        this.monT = this.add.text(20, 48, '💰 Tiền: $400', { fontSize: '16px', fontStyle: 'bold', color: '#f1c40f', stroke: '#000', strokeThickness: 2 });

        this.tweens.add({ targets: this.heart, scale: 1.3, duration: 600, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
        this.game.events.on('updateHUD', this.updateHUD, this);
    }

    updateHUD() {
        const s = window.GameState;
        this.dayT.setText(`📅 Ngày: ${s.day}`);
        this.monT.setText(`💰 Tiền: $${s.money}`);
        this.energyT.setText(`${s.energy}`);
        this.energyT.setColor(s.energy > 60 ? '#2ecc71' : s.energy > 30 ? '#f39c12' : '#e74c3c');
    }
}
