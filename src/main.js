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

window.GameState = {
    day: 1, money: 400, energy: 100, maxEnergy: 100,
    tool: 'hand',
    inventory: { seed_tomato: 2, seed_cabbage: 0, tomato: 0, cabbage: 0 },
    plots: Array(12).fill(null).map(() => ({ watered: false, crop: null, growth: 0 }))
};

new Phaser.Game(config);
