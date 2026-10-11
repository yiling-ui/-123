"""Generate original, mathematically specified teaching diagrams (stdlib only)."""
import argparse
import html
from pathlib import Path

BLUE, ORANGE, GREEN = '#2563eb', '#d97706', '#059669'

class Drawing:
    def __init__(self, title, subtitle):
        self.parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="620" viewBox="0 0 1200 620">', '<rect width="1200" height="620" fill="#fff"/>', '<g font-family="Microsoft YaHei,Arial,sans-serif" fill="#172033">']
        self.text(42, 45, title, 26)
        self.text(42, 78, subtitle, 17, '#536078')
    def text(self, x, y, s, size=16, color='#172033'):
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{html.escape(s)}</text>')
    def line(self, x1, y1, x2, y2, color='#bac4d3', dash=''):
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2" stroke-dasharray="{dash}"/>')
    def polygon(self, pts, color, opacity=.18):
        self.parts.append(f'<polygon points="{" ".join(f"{x},{y}" for x,y in pts)}" fill="{color}" opacity="{opacity}"/>')
    def curve(self, pts, color=BLUE, dash=''):
        self.parts.append(f'<polyline points="{" ".join(f"{x},{y}" for x,y in pts)}" fill="none" stroke="{color}" stroke-width="3" stroke-dasharray="{dash}"/>')
    def dot(self, x, y, color=BLUE, hollow=False):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{"white" if hollow else color}" stroke="{color}" stroke-width="2"/>')
    def save(self, path):
        path.write_text(''.join(self.parts)+ '</g></svg>', encoding='utf-8')

def panel(d, left, width, xmax, ymax, ymin=0):
    top, bottom = 135, 465
    def xy(x,y):
        return left+x/xmax*width, bottom-(y-ymin)/(ymax-ymin)*(bottom-top)
    d.line(*xy(0,ymin), *xy(xmax,ymin))
    d.line(*xy(0,ymin), *xy(0,ymax))
    for x in range(int(xmax)+1):
        xx,yy=xy(x,ymin)
        d.text(xx-4,yy+24,str(x),13)
    for y in range(int(ymin),int(ymax)+1):
        xx,yy=xy(0,y)
        d.text(xx-27,yy+4,str(y),13)
    d.text(left+width+7,bottom+4,'x',14)
    d.text(left-7,top-12,'y',14)
    return xy

def sample(xy, f, start, end, n=160):
    return [xy(start+(end-start)*i/n, f(start+(end-start)*i/n)) for i in range(n+1)]

def limit(out):
    d=Drawing('极限：点值改变，邻近趋势仍可保持', '例：x ≠ 2 时 f(x)=x²；f(2)=5。极限 L=4，ε=0.8，取 δ=0.16。')
    p=panel(d,90,650,3,7)
    d.polygon([p(0,3.2),p(3,3.2),p(3,4.8),p(0,4.8)],GREEN)
    d.polygon([p(1.84,0),p(2.16,0),p(2.16,7),p(1.84,7)],ORANGE,.13)
    d.curve(sample(p,lambda x:x*x,0,2.64))
    for y in (3.2,4,4.8): d.line(*p(0,y),*p(3,y),GREEN,'6 5')
    for x in (1.84,2.16): d.line(*p(x,0),*p(x,7),ORANGE,'6 5')
    d.dot(*p(2,4),hollow=True); d.dot(*p(2,5),ORANGE)
    d.text(790,160,'绿色：输出误差带',20,GREEN)
    d.text(790,196,'3.2 < f(x) < 4.8')
    d.text(790,258,'橙色：输入控制范围',20,ORANGE)
    d.text(790,294,'1.84 < x < 2.16，排除 x=2')
    d.text(790,356,'空心点：趋近高度 4')
    d.text(790,392,'实心点：实际点值 5')
    d.text(90,538,'先给 ε，再选择 δ；控制范围中的所有 x，而不是只找到几个合适的点。',20)
    d.text(90,574,'一般可取 δ=min(1, ε/5)：|x²−4|=|x−2||x+2|<5δ≤ε。',18)
    d.save(out/'limit.svg')

def derivative(out):
    d=Drawing('导数：割线的斜率逐渐靠近切线斜率', '蓝色为 y=x²，绿色虚线为 x=1 处切线；橙色为割线。三幅图使用相同坐标尺度。')
    for left,h in zip((70,460,850),(.8,.3,.08)):
        p=panel(d,left,280,2,4)
        d.curve(sample(p,lambda x:x*x,0,2))
        d.curve(sample(p,lambda x:2*x-1,.5,2),GREEN,'7 5')
        m=2+h
        d.curve(sample(p,lambda x:1+m*(x-1),max(0,1-1/m),2),ORANGE)
        d.dot(*p(1,1)); d.dot(*p(1+h,(1+h)**2),ORANGE)
        d.line(*p(1,1),*p(1+h,1),ORANGE,'4 4')
        d.line(*p(1+h,1),*p(1+h,(1+h)**2),ORANGE,'4 4')
        d.text(left,112,f'h={h}，割线斜率={m:g}',18)
    d.text(70,539,'h≠0 时：(f(1+h)−f(1))/h = 2+h；再让 h→0，才得到导数 2。',21)
    d.text(70,578,'精确增量 Δy=2h+h²；线性估计 Δy≈2h。图示正 h，定义还须考虑负 h。',18)
    d.save(out/'derivative.svg')

def ftc(out):
    d=Drawing('基本定理：新增面积 ÷ 移动距离 → 当前高度', 'f(t)=t²，A(x)=∫₀ˣ t²dt。右端从 x=1.5 移动到 x+h=1.8（h=0.3）。')
    for left,strip in ((80,False),(650,True)):
        p=panel(d,left,450,2.2,5)
        d.text(left,112,'原累积量 A(1.5)' if not strip else '新增量 A(1.8)−A(1.5)',18)
        if not strip:
            d.polygon([p(0,0)]+sample(p,lambda t:t*t,0,1.5)+[p(1.5,0)],BLUE)
        else:
            d.polygon([p(1.5,0)]+sample(p,lambda t:t*t,1.5,1.8)+[p(1.8,0)],ORANGE,.35)
            d.curve([p(1.5,0),p(1.5,2.25),p(1.8,2.25),p(1.8,0)],GREEN,'5 5')
            d.text(left+15,170,'绿色框：近似面积 h·f(x)',16,GREEN)
        d.curve(sample(p,lambda t:t*t,0,2.2))
        for x in ((1.5,) if not strip else (1.5,1.8)):
            d.line(*p(x,0),*p(x,x*x),ORANGE,'5 5')
            d.text(p(x,0)[0]-10,507,str(x),14,ORANGE)
    d.text(80,548,'曲顶窄条并非精确矩形；h→0 时，平均高度趋向 f(x)，所以 A′(x)=f(x)。',20)
    d.text(80,584,'本例 ΔA/h=x²+xh+h²/3；h=0.3 时为2.73，极限 h→0 时为2.25。',18)
    d.save(out/'ftc.svg')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--topic',choices=['all','limit','derivative','ftc'],default='all')
    parser.add_argument('--outdir',type=Path,required=True)
    args=parser.parse_args(); args.outdir.mkdir(parents=True,exist_ok=True)
    for topic,fn in [('limit',limit),('derivative',derivative),('ftc',ftc)]:
        if args.topic in ('all',topic): fn(args.outdir)
