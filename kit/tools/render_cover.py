"""Render a designed Reel COVER (the still shown on the profile grid; the video plays when tapped).
Usage (from kit/): python3 tools/render_cover.py cover.html out_dir prefix
The page needs an element #cover of exactly 1080x1920. Writes:
  prefix_cover.jpg       1080x1920 JPEG -> host it and pass as cover_url to Windsor create_video_post (NOT thumb_offset)
  prefix_cover_grid.jpg  the centre 3:4 crop (1080x1440, y 240-1680) the profile grid shows - LOOK at it: headline,
                         face and key visual must sit fully inside it, >= 80 px from its edges.
"""
import sys, os, asyncio
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    page, od, pre = sys.argv[1], sys.argv[2], sys.argv[3]; os.makedirs(od, exist_ok=True)
    async with async_playwright() as p:
        exe='/usr/bin/google-chrome' if os.path.exists('/usr/bin/google-chrome') else None
        b=await p.chromium.launch(executable_path=exe,args=['--force-color-profile=srgb'])
        pg=await b.new_page(viewport={'width':1140,'height':1980}); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+os.path.abspath(page)); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(700)
        await pg.locator('#cover').screenshot(path=f'{od}/{pre}_cover.png'); await b.close()
        if errs: print('PAGE ERRORS:',errs)
    im=Image.open(f'{od}/{pre}_cover.png').convert('RGB'); assert im.size==(1080,1920), im.size
    im.save(f'{od}/{pre}_cover.jpg',quality=93); os.remove(f'{od}/{pre}_cover.png')
    im.crop((0,240,1080,1680)).save(f'{od}/{pre}_cover_grid.jpg',quality=90); print('ok',od)
asyncio.run(main())
