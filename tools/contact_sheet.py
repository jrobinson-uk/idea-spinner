import glob, os, re, sys
files=sorted(glob.glob(sys.argv[1]+'/*.svg')); cols=7; size=170
rows=(len(files)+cols-1)//cols
out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{cols*size}" height="{rows*(size+24)}"><rect width="100%" height="100%" fill="#e1f4f1"/>']
for i,f in enumerate(files):
    x=(i%cols)*size; y=(i//cols)*(size+24)
    s=open(f).read().replace('<svg ', f'<svg x="{x+5}" y="{y+5}" width="160" height="160" ',1)
    out.append(s+f'<text x="{x+85}" y="{y+182}" font-size="14" text-anchor="middle" font-family="Helvetica">{os.path.basename(f)[:-4]}</text>')
out.append('</svg>'); open(sys.argv[2],'w').write(''.join(out))
