import Phaser from 'phaser';
import Boot from './scenes/Boot.js';
import MapScene from './scenes/MapScene.js';
import FieldScene from './scenes/FieldScene.js';
import HouseScene from './scenes/HouseScene.js';
import ShopScene from './scenes/ShopScene.js';
import UIScene from './scenes/UIScene.js';

const config = {
    type: Phaser.AUTO,
    width: 864,
    height: 672,
    parent: 'game-container',
    backgroundColor: '#1a1a2e',
    pixelArt: true,
    scale: {
        mode: Phaser.Scale.FIT,
        autoCenter: Phaser.Scale.CENTER_BOTH,
    },
    scene: [Boot, MapScene, FieldScene, HouseScene, ShopScene, UIScene]
};

import { CROPS } from './data/crops.js';

window.GameState = {
    day: 1, money: 400, energy: 100, maxEnergy: 100,
    tool: 'hand', activeSeed: 'parsnip',
    inventory: {},
    plots: Array(12).fill(null).map(() => ({ watered: false, crop: null, growth: 0 }))
};

// Initialize inventory with 0 for all seeds and crops
Object.keys(CROPS).forEach(key => {
    window.GameState.inventory[`seed_${key}`] = 0;
    window.GameState.inventory[key] = 0;
});
// Give some starting seeds
window.GameState.inventory['seed_parsnip'] = 5;


new Phaser.Game(config);
