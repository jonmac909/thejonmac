// Measures the footer social link text tops at 390 and 1280-1920 wide. Runs on GPU2 via hf_gpu2.py exec (puppeteer-core from the hyperframes fork).
const fs = require('fs'), path = require('path'), { createRequire } = require('module');
const puppeteer = createRequire('D:/AgentTeam/hyperframes-fork/packages/cli/x.js')('puppeteer-core');
function findChrome() {
  const fixed = ['C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'];
  const roots = ['C:/Users/jonst/.cache/puppeteer', 'C:/Users/jonmac/.cache/puppeteer', 'C:/Users/jonst/AppData/Local/ms-playwright'];
  const walk = (d, n) => { if (n > 5) return null; let es; try { es = fs.readdirSync(d, { withFileTypes: true }); } catch { return null; }
    for (const e of es) { const p = path.join(d, e.name); if (e.isFile() && /^chrome(-headless-shell)?\.exe$/.test(e.name)) return p; }
    for (const e of es) if (e.isDirectory()) { const r = walk(path.join(d, e.name), n + 1); if (r) return r; } return null; };
  for (const r of roots) { const x = walk(r, 0); if (x) return x; }
  return fixed.find(f => fs.existsSync(f));
}
(async () => {
  let file = process.argv[2];
  const browser = await puppeteer.launch({ executablePath: findChrome(), headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.goto('file:///' + path.resolve(file).split(String.fromCharCode(92)).join('/'), { waitUntil: 'load', timeout: 60000 });
  for (const w of [1280, 1366, 1440, 1536, 1920, 390]) {
    await page.setViewport({ width: w, height: 900 }); await new Promise(r => setTimeout(r, 400));
    const tops = await page.evaluate(() => ['6EY2cJpiAe', 'VermR5vsN4', 'cRdWGDvt4W'].map(i => {
      const r = document.querySelector('#button-' + i + '_btn .main-heading-button').getBoundingClientRect(); return [r.top, r.top + r.height / 2]; }));
    console.log('MEASURE ' + JSON.stringify({ width: w, tops: tops.map(t => +t[0].toFixed(1)), centers: tops.map(t => +t[1].toFixed(1)) }));
  }
  await browser.close();
})().catch(e => { console.log('MEASURE_ERROR ' + e.message); process.exit(1); });
