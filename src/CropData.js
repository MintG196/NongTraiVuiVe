// Crop growth data based on Stardew Valley crops
// Each crop has multiple growth stages with specific day requirements
// The maturityDays field is the TOTAL days needed to fully mature and harvest

export const CROP_DATA = {
    tomato: {
        name: 'Cà chua',
        icon: '🍅',
        // Stages: 0 days (seed), 3 days, 6 days, 9 days, 12 days, 15 days (mature, ready to harvest)
        maturityDays: 15,  
        stages: [
            { daysNeeded: 0, emoji: '🌱' },    // Stage 0: Seed (day 1)
            { daysNeeded: 3, emoji: '🌿' },    // Stage 1: Sprout
            { daysNeeded: 6, emoji: '🌿' },    // Stage 2: Young plant
            { daysNeeded: 9, emoji: '🌿' },    // Stage 3: Plant
            { daysNeeded: 12, emoji: '🌿' },   // Stage 4: Flowering
            { daysNeeded: 15, emoji: '🍅' },   // Stage 5: Mature with fruit (HARVESTABLE)
        ],
        regrows: false,
    },
    cabbage: {
        name: 'Bắp cải',
        icon: '🥬',
        // Stages: 0, 2, 5, 8, 11, 14 days
        maturityDays: 14,
        stages: [
            { daysNeeded: 0, emoji: '🌱' },    // Seed
            { daysNeeded: 2, emoji: '🌿' },    // Sprout
            { daysNeeded: 5, emoji: '🌿' },    // Young
            { daysNeeded: 8, emoji: '🌿' },    // Plant
            { daysNeeded: 11, emoji: '🌿' },   // Growing
            { daysNeeded: 14, emoji: '🥬' },   // Mature (HARVESTABLE)
        ],
        regrows: false,
    },
    // SUMMER CROPS
    corn: {
        name: 'Bắp',
        icon: '🌽',
        maturityDays: 14,
        stages: [
            { daysNeeded: 0, emoji: '🌱' },
            { daysNeeded: 2, emoji: '🌿' },
            { daysNeeded: 5, emoji: '🌿' },
            { daysNeeded: 8, emoji: '🌿' },
            { daysNeeded: 11, emoji: '🌿' },
            { daysNeeded: 14, emoji: '🌽' },
        ],
        regrows: true,  // Can regrow after harvest
    },
    melon: {
        name: 'Dưa',
        icon: '🍈',
        maturityDays: 12,
        stages: [
            { daysNeeded: 0, emoji: '🌱' },
            { daysNeeded: 2, emoji: '🌿' },
            { daysNeeded: 4, emoji: '🌿' },
            { daysNeeded: 6, emoji: '🌿' },
            { daysNeeded: 8, emoji: '🌿' },
            { daysNeeded: 10, emoji: '🌿' },
            { daysNeeded: 12, emoji: '🍈' },
        ],
        regrows: false,
    },
    pumpkin: {
        name: 'Bí ngô',
        icon: '🎃',
        maturityDays: 13,
        stages: [
            { daysNeeded: 0, emoji: '🌱' },
            { daysNeeded: 3, emoji: '🌿' },
            { daysNeeded: 6, emoji: '🌿' },
            { daysNeeded: 9, emoji: '🌿' },
            { daysNeeded: 11, emoji: '🌿' },
            { daysNeeded: 13, emoji: '🎃' },
        ],
        regrows: false,
    },
    hotpepper: {
        name: 'Ớt cay',
        icon: '🌶️',
        maturityDays: 10,
        stages: [
            { daysNeeded: 0, emoji: '🌱' },
            { daysNeeded: 3, emoji: '🌿' },
            { daysNeeded: 6, emoji: '🌿' },
            { daysNeeded: 8, emoji: '🌿' },
            { daysNeeded: 10, emoji: '🌶️' },
        ],
        regrows: true,
    },
    eggplant: {
        name: 'Cà tím',
        icon: '🍆',
        maturityDays: 10,
        stages: [
            { daysNeeded: 0, emoji: '🌱' },
            { daysNeeded: 3, emoji: '🌿' },
            { daysNeeded: 6, emoji: '🌿' },
            { daysNeeded: 8, emoji: '🌿' },
            { daysNeeded: 10, emoji: '🍆' },
        ],
        regrows: true,
    },
    // SPRING CROPS
    parsnip: {
        name: 'Cà rốt trắng',
        icon: '🥕',
        maturityDays: 6,
        stages: [
            { daysNeeded: 0, emoji: '🌱' },
            { daysNeeded: 1, emoji: '🌿' },
            { daysNeeded: 3, emoji: '🌿' },
            { daysNeeded: 5, emoji: '🌿' },
            { daysNeeded: 6, emoji: '🥕' },
        ],
        regrows: false,
    },
    potato: {
        name: 'Khoai tây',
        icon: '🥔',
        maturityDays: 6,
        stages: [
            { daysNeeded: 0, emoji: '🌱' },
            { daysNeeded: 2, emoji: '🌿' },
            { daysNeeded: 4, emoji: '🌿' },
            { daysNeeded: 6, emoji: '🥔' },
        ],
        regrows: false,
    },
    cauliflower: {
        name: 'Súp lơ',
        icon: '🥦',
        maturityDays: 12,
        stages: [
            { daysNeeded: 0, emoji: '🌱' },
            { daysNeeded: 2, emoji: '🌿' },
            { daysNeeded: 5, emoji: '🌿' },
            { daysNeeded: 8, emoji: '🌿' },
            { daysNeeded: 10, emoji: '🌿' },
            { daysNeeded: 12, emoji: '🥦' },
        ],
        regrows: false,
    },
    greenbean: {
        name: 'Đậu xanh',
        icon: '🫘',
        maturityDays: 10,
        stages: [
            { daysNeeded: 0, emoji: '🌱' },
            { daysNeeded: 2, emoji: '🌿' },
            { daysNeeded: 4, emoji: '🌿' },
            { daysNeeded: 6, emoji: '🌿' },
            { daysNeeded: 8, emoji: '🌿' },
            { daysNeeded: 10, emoji: '🫘' },
        ],
        regrows: true,
    },
    // FALL CROPS
    carrot: {
        name: 'Cà rốt',
        icon: '🥕',
        maturityDays: 9,
        stages: [
            { daysNeeded: 0, emoji: '🌱' },
            { daysNeeded: 3, emoji: '🌿' },
            { daysNeeded: 6, emoji: '🌿' },
            { daysNeeded: 9, emoji: '🥕' },
        ],
        regrows: false,
    },
    yam: {
        name: 'Khoai lang',
        icon: '🍠',
        maturityDays: 10,
        stages: [
            { daysNeeded: 0, emoji: '🌱' },
            { daysNeeded: 3, emoji: '🌿' },
            { daysNeeded: 6, emoji: '🌿' },
            { daysNeeded: 8, emoji: '🌿' },
            { daysNeeded: 10, emoji: '🍠' },
        ],
        regrows: false,
    },
};

export function getCropData(cropType) {
    return CROP_DATA[cropType] || CROP_DATA.parsnip; // Default to parsnip
}

export function getGrowthStage(cropType, growthValue) {
    const data = getCropData(cropType);
    if (!data) return { emoji: '❓', stage: 0 };
    
    // Find the current stage based on growth value (number of days elapsed)
    let stage = 0;
    for (let i = data.stages.length - 1; i >= 0; i--) {
        if (growthValue >= data.stages[i].daysNeeded) {
            stage = i;
            break;
        }
    }
    
    return {
        emoji: data.stages[stage].emoji,
        stage: stage,
        isMatured: growthValue >= data.maturityDays,
        maturityDays: data.maturityDays,
        daysToMaturity: Math.max(0, data.maturityDays - growthValue),
    };
}

