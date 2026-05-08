import fs from 'fs';
import path from 'path';

const cropsDir = 'd:/Nong Trai/assets/Crops';
const files = fs.readdirSync(cropsDir).filter(f => f.endsWith('.png'));

// We need a simple way to check if a row is empty without a full image library
// Since they are PNGs, we can't easily read pixels without a library.
// But wait, I can use the browser to do this!
console.log("Files detected: " + files.length);
