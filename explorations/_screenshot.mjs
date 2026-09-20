import { chromium } from "playwright";
const EXE="/home/wardsi/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome";
const OUT="/tmp/claude-1000/-home-wardsi-projects/24625545-a671-4e92-b39d-380d363f89c7/scratchpad";
const b=await chromium.launch({executablePath:EXE,args:["--no-sandbox"]});
const ctx=await b.newContext({viewport:{width:1240,height:1400},deviceScaleFactor:1.5});
const p=await ctx.newPage();
p.on("console",m=>{if(m.type()==="error")console.log("PAGE-ERR:",m.text());});
await p.goto("file://"+OUT+"/bluepadel-sportstech.html",{waitUntil:"networkidle"});
await p.waitForTimeout(1200);
await p.screenshot({path:`${OUT}/sportstech-full.png`,fullPage:true});
// also a focused crop of the five plates region: screenshot directions section
console.log("done");
await b.close();
