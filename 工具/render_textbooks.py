import pypdfium2 as p
from pathlib import Path
root=Path(__file__).parent.parent
for v in ['上册','下册']:
    out=root/'教材核对'/v;out.mkdir(parents=True,exist_ok=True)
    d=p.PdfDocument(str(root/f'高等数学第8版{v}.pdf'))
    for i in range(len(d)):
        img=d[i].render(scale=1.3).to_pil();img.save(out/f'{i+1:04d}.png')
    print(v,len(d),flush=True)
