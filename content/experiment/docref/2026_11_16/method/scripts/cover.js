const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1300, height: 860 }, deviceScaleFactor: 2 });
  await p.setContent('<!doctype html><meta charset="utf-8">' + require('fs').readFileSync(process.argv[2], 'utf8'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: process.argv[3], type: 'jpeg', quality: 86 });
  await b.close();
})();
