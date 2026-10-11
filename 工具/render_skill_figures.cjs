const {chromium}=require('C:/Users/xy/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const path=require('path');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const page=await browser.newPage({viewport:{width:1200,height:620},deviceScaleFactor:1});
 for(const name of ['limit','derivative','ftc']){
  const file=path.resolve('skills/calculus-visual-tutor/assets',name+'.svg');
  await page.goto('file:///'+file.replaceAll('\\','/'));
  await page.screenshot({path:file.replace('.svg','.png')});
 }
 await browser.close();
})();
