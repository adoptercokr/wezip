const fs = require('fs');
const html = fs.readFileSync('01-Nova-Web-Studio/money-calc/gov-finder.html', 'utf8');
const startIdx = html.indexOf('const POLICIES = [');
const endMarker = '];';
const endIdx = html.indexOf(endMarker, startIdx);
const jsCode = html.substring(startIdx + 'const POLICIES = '.length, endIdx + 1);
const policies = eval(jsCode);

const noCat = policies.filter(p => !p.category);
console.log('Total without category:', noCat.length);
noCat.forEach((p, idx) => {
    console.log(`${idx + 1}. [${p.id}] ${p.name}`);
});
