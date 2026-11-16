const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 1400 } });
  const errs=[]; p.on('pageerror', e => errs.push(e.message));
  await p.goto(process.argv[2], { waitUntil: 'networkidle' });
  await p.screenshot({ path: process.argv[3], fullPage: true });
  console.log('errors', errs);
  await b.close();
})();
