"""Render a connected 3-post grid set from one 3240x1350 panorama (#pano) and split it into 3 tiles.
Usage (from kit/): python3 tools/render_triptych.py page.html out_dir prefix
Writes out_dir/prefix_1.jpg (LEFT), _2 (MIDDLE), _3 (RIGHT), prefix_full.png, and prefix_grid_preview.jpg
(the 3:4 crops Instagram's profile grid shows, side by side — LOOK at it before posting).
POST ORDER: _3 first, then _2, then _1 (the newest post shows at the top-left of the grid)."""
import sys, os, asyncio
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    page, od, pre = sys.argv[1], sys.argv[2], sys.argv[3]; os.makedirs(od, exist_ok=True)
    async with async_playwright() as p:
        exe='/usr/bin/google-chrome' if os.path.exists('/usr/bin/google-chrome') else None
        b=await p.chromium.launch(executable_path=exe,args=['--force-color-profile=srgb'])
        pg=await b.new_page(viewport={'width':3300,'height':1400}); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+os.path.abspath(page)); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(600)
        await pg.locator('#pano').screenshot(path=f'{od}/{pre}_full.png'); await b.close()
        if errs: print('PAGE ERRORS:',errs)
    pano=Image.open(f'{od}/{pre}_full.png').convert('RGB')
    for i in range(3): pano.crop((i*1080,0,(i+1)*1080,1350)).save(f'{od}/{pre}_{i+1}.jpg',quality=95)
    tiles=[pano.crop((i*1080+34,0,i*1080+1046,1350)).resize((450,600)) for i in range(3)]
    g=Image.new('RGB',(1362,600),'white'); [g.paste(t,(i*456,0)) for i,t in enumerate(tiles)]; g.save(f'{od}/{pre}_grid_preview.jpg')
    print('ok', od)
asyncio.run(main())
