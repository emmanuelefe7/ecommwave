"""Render a three.js concept post (page sets window.READY=true when done) to a 1080x1350 JPEG.
One-time setup (from kit/):  npm pack three && tar xzf three-*.tgz && mv package three_pkg && rm three-*.tgz
Usage (from kit/):  python3 tools/render_3d.py page.html "query" out.jpg     e.g. tpl_3d_concepts.html "s=pawn" /tmp/p.jpg
The page must bake the WebGL canvas into an <img> before READY (see tpl_3d_concepts.html), otherwise screenshots can glitch."""
import asyncio, sys, os
from playwright.async_api import async_playwright
async def main():
    page, q, out = sys.argv[1], sys.argv[2], sys.argv[3]
    async with async_playwright() as p:
        exe='/usr/bin/google-chrome' if os.path.exists('/usr/bin/google-chrome') else None
        b=await p.chromium.launch(executable_path=exe,args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--allow-file-access-from-files'])
        pg=await b.new_page(viewport={'width':1080,'height':1350}); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+os.path.abspath(page)+'?'+q)
        await pg.wait_for_function('window.READY===true',timeout=180000)
        await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
        await (pg.screenshot(path=out,omit_background=True) if out.endswith('.png') else pg.screenshot(path=out,type='jpeg',quality=94)); print('ok',out,errs)
        await b.close()
asyncio.run(main())
