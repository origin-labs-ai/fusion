const fs = require('fs');
const p = process.argv[2];
const s = fs.readFileSync(p, 'utf8');
const lines = s.split(/\r?\n/);

console.log('=== SIZE ===');
console.log('lines: ' + lines.length + '  chars: ' + s.length);

const heads = new Set();
lines.forEach(l => {
  const m = l.match(/^#{2,4} ([0-9]+(?:bis)?(?:\.[0-9]+[a-z]?)?)\.? /);
  if (m) heads.add(m[1]);
});
const refs = new Set();
for (const m of s.matchAll(/§([0-9]+(?:bis)?(?:\.[0-9]+[a-z]?)?)/g)) refs.add(m[1]);
const bad = [...refs].filter(r => !heads.has(r) && !['13','15'].includes(r));
console.log('\n=== REFS ===');
console.log('refs found: ' + refs.size);
console.log(bad.length ? 'BROKEN: ' + bad.join(', ') : 'ALL RESOLVE');

console.log('\n=== DUPLICATE H2 ===');
const seen = new Set(), dup = [];
lines.forEach(l => { const m = l.match(/^## (.+)$/); if (m) { if (seen.has(m[1])) dup.push(m[1]); seen.add(m[1]); } });
console.log(dup.length ? dup.join(' | ') : 'none');

console.log('\n=== V GATES ===');
const v = [...new Set([...s.matchAll(/\*\*V(\d+)\*\*/g)].map(m => +m[1]))].sort((a,b)=>a-b);
const gaps = [];
for (let i = 1; i <= v[v.length-1]; i++) if (!v.includes(i)) gaps.push(i);
console.log('gates V1..V' + v[v.length-1] + (gaps.length ? '  GAPS: ' + gaps.join(',') : '  contiguous'));

console.log('\n=== KEY MARKERS ===');
[['5c research', /§5c/g], ['papers cited', /arXiv `?\d{4}\.\d{4,5}/g], ['UNKNOWN labels', /UNKNOWN/g],
 ['EAIN', /EAIN/g], ['NCM', /NCM/g], ['KAT', /KAT/g]].forEach(([k, re]) => {
  console.log('  ' + k.padEnd(14) + (s.match(re) || []).length);
});

console.log('\n=== HEADINGS 1-16 ===');
lines.filter(l => /^#{2} /.test(l)).forEach(l => console.log('  ' + l));
