const {chromium}=require('C:/Users/xy/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const path=require('path');
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'msedge'});
 const page=await browser.newPage({viewport:{width:1100,height:1000}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('file:///'+path.join(__dirname,'..','高等数学第八版知识与题型思维导图.html').replaceAll('\\','/'));
 await page.screenshot({path:path.join(__dirname,'教材核对','思维导图宽屏.png'),fullPage:true});
 for(let i=0;i<12;i++){
  await page.selectOption('#math-chapter-select',String(i));
  if(!(await page.locator('.section-node').count()))throw Error('Empty chapter '+i);
  await page.locator('.section-node summary').last().click();
 }
 await page.selectOption('#math-chapter-select','11');
 await page.setViewportSize({width:360,height:1000});
 const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
 await page.screenshot({path:path.join(__dirname,'教材核对','思维导图手机.png'),fullPage:true});
 console.log(JSON.stringify({chapters:12,errors,overflow}));
 if(errors.length||overflow)process.exitCode=1;
 await browser.close();
})();
