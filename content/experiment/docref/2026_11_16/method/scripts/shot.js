const { chromium } = require('playwright');
(async () => {
  const [,, file, out, w, h, scheme, hash] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: 1, colorScheme: scheme || 'light' });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type()==='error' && errs.push(m.text()));
  const html = require('fs').readFileSync(file, 'utf8');
  await p.setContent(`<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>${html}</body></html>`, { waitUntil: 'networkidle' });
  if (hash) { await p.evaluate(h => { location.hash = h }, hash); await p.waitForTimeout(400) }
  await p.waitForTimeout(500);
  const sw = await p.evaluate(() => document.documentElement.scrollWidth);
  await p.screenshot({ path: out, fullPage: process.argv[9] === 'full' });
  console.log('scrollWidth', sw, 'errors', JSON.stringify(errs));
  await b.close();
})();
