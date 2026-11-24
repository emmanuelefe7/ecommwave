"""Render each <section class="s" id="s1..sN"> (1080x1350) of an HTML page to JPEG.
Usage: python3 tools/render_carousel.py page.html out_dir prefix"""
import sys, os, asyncio
from playwright.async_api import async_playwright
async def main():
    src=os.path.abspath(sys.argv[1]); od=sys.argv[2]; pre=sys.argv[3]; os.makedirs(od,exist_ok=True)
    async with async_playwright() as p:
        exe='/usr/bin/google-chrome' if os.path.exists('/usr/bin/google-chrome') else None
        b=await p.chromium.launch(executable_path=exe,args=['--force-color-profile=srgb'])
        pg=await b.new_page(viewport={'width':1080,'height':1350})
        await pg.goto('file://'+src); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(500)
        n=await pg.evaluate("document.querySelectorAll('section.s').length")
        for i in range(1,n+1):
            f=f'{od}/{pre}_{i:02d}.jpg'; await pg.locator(f'#s{i}').screenshot(path=f,type='jpeg',quality=95); print(f)
        await b.close()
asyncio.run(main())
