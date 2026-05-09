import Phaser from 'phaser';
import { CROPS, GIANT_CROPS } from '../data/crops.js';


export default class Boot extends Phaser.Scene {
    constructor() { super('Boot'); }

    preload() {
        this.load.image('map_bg', '/assets/map_rendered.png');
        this.load.image('field_bg', '/assets/field_bg.png');
        this.load.image('house_bg', '/assets/house_bg.png');
        this.load.image('farmhouse', '/assets/farmhouse.png');
        this.load.image('dirt', '/assets/dirt.png');
        this.load.image('dirt_wet', '/assets/dirt_wet.png');
        this.load.image('tree_green', '/assets/tree_green.png');
        this.load.image('bush', '/assets/bush.png');
        this.load.image('stump', '/assets/stump.png');
        this.load.image('barrel', '/assets/barrel.png');
        this.load.image('chest', '/assets/chest.png');
        this.load.image('scarecrow', '/assets/scarecrow.png');
        this.load.image('bed', '/assets/bed.png');
        this.load.image('well', '/assets/well.png');

        // Load all crop tilesets from dynamic data
        const allCrops = { ...CROPS, ...GIANT_CROPS };
        
        Object.keys(allCrops).forEach(key => {
            const capName = key.charAt(0).toUpperCase() + key.slice(1);
            this.load.image(key, `/assets/Crops/${capName}.png`);
        });



        const w = this.cameras.main.width, h = this.cameras.main.height;
        const box = this.add.graphics();
        box.fillStyle(0x222222, 0.8);
        box.fillRect(w/2-160, h/2-15, 320, 30);
        const bar = this.add.graphics();
        this.load.on('progress', v => { bar.clear(); bar.fillStyle(0x2ecc71,1); bar.fillRect(w/2-155, h/2-10, 310*v, 20); });
        this.load.on('complete', () => { bar.destroy(); box.destroy(); });
    }

    create() {
        this.scene.start('UIScene');
        this.scene.start('MapScene');
    }
}
