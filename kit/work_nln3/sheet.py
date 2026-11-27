import sys
from PIL import Image
ts=sys.argv[2].split(','); out=sys.argv[1]
ims=[Image.open(f'/tmp/frame_{t}.jpg').resize((360,640)) for t in ts]
cols=min(6,len(ims)); rows=(len(ims)+cols-1)//cols
S=Image.new('RGB',(cols*364,rows*644),'white')
for i,im in enumerate(ims): S.paste(im,((i%cols)*364,(i//cols)*644))
S.save(out,quality=85)
