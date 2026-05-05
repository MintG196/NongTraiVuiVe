import Phaser from 'phaser';

const GW = 864, GH = 672;

export default class MapScene extends Phaser.Scene {
    constructor() { super('MapScene'); }

    create() {
        // 1. The pre-rendered background (v5 Masterpiece)
        this.add.image(0, 0, 'map_bg').setOrigin(0, 0).setDisplaySize(GW, GH);

        // 2. Title
        this.add.text(GW/2, 28, '🌾 NÔNG TRẠI 🌾', {
            fontSize: '30px', fontFamily: '"Press Start 2P", monospace',
            color: '#f1c40f', stroke: '#654321', strokeThickness: 6,
        }).setOrigin(0.5).setDepth(100);

        // 3. HOUSE INTERACTION (Position x=320, y=32, Size 152x140)
        const houseBtn = this.add.rectangle(396, 102, 150, 130, 0x000000, 0)
            .setInteractive({ useHandCursor: true });
        
        const houseLabel = this.add.text(396, 160, '🏠 Vào Nhà', {
            fontSize: '18px', fontStyle: 'bold', color: '#fff',
            stroke: '#000', strokeThickness: 4,
            backgroundColor: 'rgba(0,0,0,0.5)', padding: { x: 10, y: 5 },
        }).setOrigin(0.5).setVisible(false).setDepth(101);

        houseBtn.on('pointerdown', () => this.scene.switch('HouseScene'));
        houseBtn.on('pointerover', () => houseLabel.setVisible(true));
        houseBtn.on('pointerout', () => houseLabel.setVisible(false));

        // 4. FARM AREA INTERACTION (Area within fences)
        // Center: x=416, y=384, Width: 320, Height: 260
        const farmBtn = this.add.rectangle(416, 384, 320, 260, 0x000000, 0)
            .setInteractive({ useHandCursor: true });

        const farmLabel = this.add.text(416, 384, '🌱 Vào Vườn', {
            fontSize: '18px', fontStyle: 'bold', color: '#fff',
            stroke: '#2d572c', strokeThickness: 4,
            backgroundColor: 'rgba(46,125,50,0.85)', padding: { x: 12, y: 6 },
        }).setOrigin(0.5).setVisible(false).setDepth(101);

        farmBtn.on('pointerdown', () => this.scene.switch('FieldScene'));
        farmBtn.on('pointerover', () => farmLabel.setVisible(true));
        farmBtn.on('pointerout', () => farmLabel.setVisible(false));

        // 5. SHOP INTERACTION (Over the Shipping Bin area)
        const shopBtn = this.add.rectangle(575, 175, 50, 50, 0x000000, 0)
            .setInteractive({ useHandCursor: true });
        
        const shopLabel = this.add.text(575, 175, '🏪 Shop', {
            fontSize: '16px', fontStyle: 'bold', color: '#f1c40f',
            stroke: '#000', strokeThickness: 4,
            backgroundColor: 'rgba(139,69,19,0.8)', padding: { x: 8, y: 4 },
        }).setOrigin(0.5).setVisible(false).setDepth(101);

        shopBtn.on('pointerdown', () => this.scene.switch('ShopScene'));
        shopBtn.on('pointerover', () => shopLabel.setVisible(true));
        shopBtn.on('pointerout', () => shopLabel.setVisible(false));

        // 6. WELL DECORATION (Visual only for now)
        const wellBtn = this.add.rectangle(208, 195, 40, 50, 0x000000, 0)
            .setInteractive({ useHandCursor: true });
        wellBtn.on('pointerover', () => {
            const t = this.add.text(208, 160, '💧 Giếng nước', { fontSize: '14px', color: '#3498db', stroke: '#000', strokeThickness: 3 }).setOrigin(0.5);
            this.time.delayedCall(1000, () => t.destroy());
        });

        // Hint text
        this.add.text(GW/2, GH - 30, 'Di chuột để khám phá nông trại', {
            fontSize: '14px', color: '#fff', fontStyle: 'italic', stroke: '#000', strokeThickness: 3
        }).setOrigin(0.5);
    }
}
