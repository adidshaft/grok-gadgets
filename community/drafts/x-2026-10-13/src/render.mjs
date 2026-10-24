import { chromium } from "../../explainer-video/node_modules/playwright-core/index.mjs";
import fs from "fs"; import os from "os"; import path from "path";
const exe = path.join(os.homedir(),"Library/Caches/ms-playwright/chromium_headless_shell-1217/chrome-headless-shell-mac-arm64/chrome-headless-shell");
const b = await chromium.launch({ executablePath: exe, args:["--allow-file-access-from-files"] });
const p = await b.newPage({ viewport:{width:2000,height:1200}, deviceScaleFactor:1 });
await p.goto("file://"+path.resolve("cards.html")); await p.waitForTimeout(400);
for (const id of ["route","wifi","stack","status","sim","kit","native","alwayson","howitworks","security","claim","ota","endcard"]) await p.locator("#"+id).screenshot({ path:`../media/card-${id}.png` });
await b.close();
