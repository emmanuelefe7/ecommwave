"""Render an animated HTML page (window.DUR + render(t)) to a silent 1080x1920 30fps MP4.
Usage: python3 tools/render_video.py page.html out.mp4
       python3 tools/render_video.py page.html --frames 1.5,4,9   (preview JPEGs in /tmp)"""
import sys, subprocess, os, asyncio
from playwright.async_api import async_playwright
async def main():
    src=os.path.abspath(sys.argv[1]); out=sys.argv[2]
    async with async_playwright() as p:
        exe='/usr/bin/google-chrome' if os.path.exists('/usr/bin/google-chrome') else None
        b=await p.chromium.launch(executable_path=exe,args=['--force-color-profile=srgb','--allow-file-access-from-files'])
        pg=await b.new_page(viewport={'width':1080,'height':1920})
        await pg.goto('file://'+src); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
        if out=='--frames':
            for t in sys.argv[3].split(','):
                await pg.evaluate(f'render({t})'); f=f'/tmp/frame_{t}.jpg'
                await pg.screenshot(path=f,type='jpeg',quality=85); print(f)
        else:
            dur=await pg.evaluate('window.DUR'); fps=30; n=int(dur*fps); tmp=out+'.tmp.mp4'
            ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate',str(fps),'-c:v','mjpeg','-i','-',
                '-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',tmp],stdin=subprocess.PIPE)
            for i in range(n):
                await pg.evaluate(f'render({i/fps})'); ff.stdin.write(await pg.screenshot(type='jpeg',quality=92))
            ff.stdin.close()
            if ff.wait()==0: os.replace(tmp,out); print('ok',out,n,'frames')
            else: print('ffmpeg failed'); sys.exit(1)
        await b.close()
asyncio.run(main())
