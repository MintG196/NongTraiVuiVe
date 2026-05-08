import fs from 'fs';
import path from 'path';

const cropsDir = 'd:/Nong Trai/assets/Crops';
const files = fs.readdirSync(cropsDir).filter(f => f.endsWith('.png'));

files.forEach(file => {
    const filePath = path.join(cropsDir, file);
    const buffer = fs.readFileSync(filePath);
    const width = buffer.readUInt32BE(16);
    const height = buffer.readUInt32BE(20);
    console.log(`${file}: ${width}x${height}`);
});
