"""Render a CONNECTED 6-post grid set (2 rows x 3) from one 3240x2700 panorama (#pano) and split it into 6 tiles.
Usage (from kit/): python3 tools/render_grid6.py page.html out_dir prefix
Tiles (as they appear on the profile grid):
    row 1:  _1 (top-left)     _2 (top-middle)     _3 (top-right)
    row 2:  _4 (bottom-left)  _5 (bottom-middle)  _6 (bottom-right)
Writes prefix_1..6.jpg (1080x1350 each), prefix_full.png and prefix_grid_preview.jpg (the 3:4 crops Instagram's
profile grid shows, with the real gaps — LOOK at it before posting: the connecting line/arrow must read as ONE path).
POST ORDER (newest shows top-left): _6, _5, _4, _3, _2, _1 — back to back, nothing in between."""
import sys, os, asyncio
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    page, od, pre = sys.argv[1], sys.argv[2], sys.argv[3]; os.makedirs(od, exist_ok=True)
    async with async_playwright() as p:
        exe='/usr/bin/google-chrome' if os.path.exists('/usr/bin/google-chrome') else None
        b=await p.chromium.launch(executable_path=exe,args=['--force-color-profile=srgb'])
        pg=await b.new_page(viewport={'width':3300,'height':2760}); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+os.path.abspath(page)); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(700)
        await pg.locator('#pano').screenshot(path=f'{od}/{pre}_full.png'); await b.close()
        if errs: print('PAGE ERRORS:',errs)
    pano=Image.open(f'{od}/{pre}_full.png').convert('RGB')
    assert pano.size==(3240,2700), pano.size
    n=0
    for r in range(2):
        for c in range(3):
            n+=1; pano.crop((c*1080,r*1350,(c+1)*1080,(r+1)*1350)).save(f'{od}/{pre}_{n}.jpg',quality=95)
    g=Image.new('RGB',(3*450+2*6,2*600+6),'white')
    for r in range(2):
        for c in range(3):
            t=pano.crop((c*1080+34,r*1350,c*1080+1046,(r+1)*1350)).resize((450,600)); g.paste(t,(c*456,r*606))
    g.save(f'{od}/{pre}_grid_preview.jpg'); print('ok', od)
asyncio.run(main())
