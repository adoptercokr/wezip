const fs = require('fs');
const html = fs.readFileSync('01-Nova-Web-Studio/money-calc/gov-finder.html', 'utf8');

const startIdx = html.indexOf('const POLICIES = [');
if (startIdx === -1) {
    console.error('POLICIES not found');
    process.exit(1);
}
// Find the end of POLICIES array
const endMarker = '];';
const endIdx = html.indexOf(endMarker, startIdx);
const jsCode = html.substring(startIdx + 'const POLICIES = '.length, endIdx + 1);

// eval the array
const policies = eval(jsCode);
console.log('Total policies in array:', policies.length);

const stats = { business: 0, personal: 0, no_cat: 0 };
const noCatList = [];
policies.forEach((p, i) => {
    if (!p.category) {
        stats.no_cat++;
        noCatList.push({ idx: i + 1, id: p.id, name: p.name });
    } else if (p.category === 'business') {
        stats.business++;
    } else if (p.category === 'personal') {
        stats.personal++;
    }
});

console.log('Stats:', stats);
console.log('Policies without category count:', noCatList.length);
console.log('First 5 without category:', noCatList.slice(0, 5));
