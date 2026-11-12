const fs = require('fs');
const p = process.argv[2];
let s = fs.readFileSync(p, 'utf8');
const lines = s.split(/\r?\n/);
const i = lines.findIndex(l => l.startsWith('formula'));
if (i < 0) { console.log('formula line not found'); process.exit(1); }
lines.splice(i + 1, 0, 'generation    = NCM (Next-Concept Modeling, arXiv 2610.14162)');
// also add an alias row to the mechanisms table
const j = lines.findIndex(l => l.includes('The attention formula'));
if (j > 0) lines.splice(j + 1, 0,
  '| **The generation mechanism** | `NCM` · `Next Concept Modeling` · `Next-Concept Modeling` · arXiv `2610.14162` · "coarse-to-fine generation" · "level-by-level decoding" |');
fs.writeFileSync(p, lines.join('\n'));
console.log('alias registry updated at line ' + (i + 1) + (j > 0 ? ' and mechanisms row ' + (j + 2) : ''));