from html.parser import HTMLParser
from pathlib import Path

class Catalog(HTMLParser):
    def __init__(self):
        super().__init__(); self.active=False; self.divs=0; self.depth=0; self.lines=[]; self.text=''
    def flush(self):
        t=self.text.strip(); self.text=''
        if t and t!='目录': self.lines.append('  '*max(0,self.depth-2)+'- '+t.replace('*',r'\*'))
    def handle_starttag(self,tag,attrs):
        if tag=='div' and dict(attrs).get('id')=='catalog': self.active=True
        if not self.active: return
        if tag=='div': self.divs+=1
        if tag=='ul': self.flush(); self.depth+=1
        if tag=='li': self.flush()
    def handle_endtag(self,tag):
        if not self.active:return
        if tag=='li':self.flush()
        if tag=='ul':self.flush();self.depth-=1
        if tag=='div':
            self.divs-=1
            if self.divs==0:self.active=False
    def handle_data(self,data):
        if self.active:self.text+=data

root=Path(__file__).parent
out=['# 同济大学《高等数学》第八版上下册目录','','来源：高等教育出版社官网。保留目录层级、习题和星号标记；官网目录未列页码。','']
for name,bid in [('上册','62cdab46938b7cc2960eedb1'),('下册','62bc8b97938b7cc2960eebb7')]:
    p=Catalog();p.feed((root/('目录'+name+'.html')).read_text(encoding='utf-8'))
    assert len(p.lines)>100,(name,len(p.lines))
    out.extend(['## '+name,'','来源：https://xuanshu.hep.com.cn/front/book/findBookDetails?bookId='+bid,'']+p.lines+[''])
target=root/'高等数学第八版上下册目录.md'
target.write_text('\n'.join(out),encoding='utf-8')
print('目录条目：',sum(x.lstrip().startswith('- ') for x in out))
print('\n'.join(out[:15]))
