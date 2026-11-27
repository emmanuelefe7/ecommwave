import sys,asyncio,os
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--allow-file-access-from-files'])
        pg=await b.new_page(viewport={'width':1080,'height':1920})
        pg.on('console',lambda m:print('console',m.text))
        pg.on('pageerror',lambda e:print('ERR',e))
        await pg.goto('file://'+os.path.abspath(sys.argv[1]),timeout=20000); print('loaded')
        await pg.evaluate('document.fonts.ready'); print('fonts')
        print(await pg.evaluate('typeof render+" "+window.DUR'))
        await b.close()
if len(sys.argv)<3: asyncio.run(main())
async def m2():
    import time
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--allow-file-access-from-files'])
        pg=await b.new_page(viewport={'width':1080,'height':1920})
        pg.on('pageerror',lambda e:print('ERR',e))
        await pg.goto('file://'+os.path.abspath(sys.argv[1]))
        for t in sys.argv[2].split(','):
            t0=time.time(); await pg.evaluate(f'render({t})'); t1=time.time()
            await pg.screenshot(path=f'/tmp/frame_{t}.jpg',type='jpeg',quality=85); print(t,round(t1-t0,2),round(time.time()-t1,2),flush=True)
        await b.close()
if len(sys.argv)>2: asyncio.run(m2())
