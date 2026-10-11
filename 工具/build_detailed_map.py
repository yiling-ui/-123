from pathlib import Path
import json,re,xml.etree.ElementTree as ET
import build_math_mindmap as base
from math_question_types import types

root=Path(__file__).parent.parent
chapters=base.chapters
extra=base.extra
pages=['1—70','71—121','122—181','182—218','219—266','267—288','289—354','1—51','52—129','130—179','180—240','241—314']
more={
 (0,0):['分段函数','隐函数与参数表示','双曲函数及恒等式','反双曲函数及对数表达式'],
 (0,1):['数列极限与子数列的关系'],
 (0,4):['有限个无穷小的和','有界函数乘无穷小'],
 (1,1):['双曲函数及反双曲函数求导','对数求导法'],
 (1,2):['★莱布尼茨高阶乘积求导公式'],
 (2,6):['显式与参数形式曲率公式'],
 (4,0):['矩形法与梯形法','定积分与位移和路程'],
 (4,2):['积分递推公式','三角函数幂的定积分'],
 (4,4):['★Γ函数在半整数处的值'],
 (5,1):['圆盘与圆环方法','柱壳法的积分推导','绕非坐标轴旋转'],
 (5,2):['提升液体与抽水做功','非恒定引力做功','曲线细棒引力'],
 (6,2):['齐次型与齐次线性方程的区别'],
 (6,5):['线性无关解的个数','非齐次方程特解的叠加'],
 (7,0):['单位向量与向径','两点距离','空间卦限'],
 (7,2):['平面束与交线'],
 (7,3):['异面直线与公垂线'],
 (8,0):['聚点与多元极限','累次极限与二重极限的区别'],
 (8,3):['齐次函数与欧拉关系'],
 (8,7):['边界最值与内部驻点'],
 (9,4):['★变动积分限的莱布尼茨公式'],
 (10,2):['全微分方程与积分因子'],
 (10,5):['★拉普拉斯算子','★格林第一与第二公式'],
 (11,0):['级数分组与重排的限制'],
 (11,1):['正项级数部分和有界判别','交错级数截断误差'],
 (11,2):['阿贝尔定理','缺项幂级数与平移中心'],
 (11,5):['★魏尔斯特拉斯M判别法'],
 (11,6):['狄利克雷收敛条件','间断点收敛到左右极限平均值']
}
more_types={
 (1,1):['对数求导法处理幂指函数','双曲函数及反双曲函数求导'],
 (1,2):['★莱布尼茨公式求高阶导数'],
 (4,1):['分段被积函数的变上限积分','利用积分关系求函数与参数'],
 (4,2):['三角幂积分递推','含绝对值的定积分分段'],
 (5,1):['绕非坐标轴旋转求体积','柱壳法求体积','面积或体积与最优化综合'],
 (5,2):['非恒定引力做功','曲线细棒引力'],
 (7,0):['求单位方向向量','空间卦限与对称点'],
 (7,3):['求公垂线与异面直线距离'],
 (8,3):['齐次函数欧拉关系证明'],
 (9,0):['选择区域使积分最大'],
 (9,4):['★变动积分限含参积分求导'],
 (10,2):['求使微分形式成为全微分的参数','全微分方程求通解'],
 (10,5):['★证明格林恒等式'],
 (11,0):['★柯西审敛原理应用','分组前后收敛性判断'],
 (11,1):['截断误差估计'],
 (11,2):['缺项与非零中心幂级数收敛域'],
 (11,6):['间断点处傅里叶级数求和']
}

data={'chapters':[],'appendix':[
 {'title':'附录Ⅰ 初等数学工具','points':['集合、区间与绝对值','三角恒等式与三角方程','复数的代数形式与三角形式','多项式与因式分解','常用不等式']},
 {'title':'附录Ⅱ 基本初等函数图像','points':['幂函数','指数与对数函数','三角与反三角函数']},
 {'title':'附录Ⅲ 常用曲线','points':['直线与圆锥曲线','参数曲线','极坐标曲线']},
 {'title':'附录Ⅳ 积分表','points':['基本积分与查表','代换归一化','适用条件与求导验算']}
]}
for ci,(c,ex,ty) in enumerate(zip(chapters,extra,types)):
    assert len(c['sections'])==len(ex)==len(ty)
    new={'title':c['name'],'volume':'上册' if ci<7 else '下册','printPages':pages[ci],'sections':[]}
    for si,(s,k,t) in enumerate(zip(c['sections'],ex,ty)):
        title=re.sub(r'^★?第.+?节\s*','',s['name'])
        if s['name'].startswith('★'):title='★ '+title
        knowledge=list(dict.fromkeys(k.split('|')+more.get((ci,si),[])))
        questions=list(dict.fromkeys(t.split('|')+more_types.get((ci,si),[])))
        new['sections'].append({'id':f'{ci+1}.{si+1}','title':title,'knowledge':knowledge,'types':questions})
    data['chapters'].append(new)

# 全文识别完整性与教材审阅线索；保留每页文字以便后续回查。
audit=[]
for v,count in [('上册',442),('下册',354)]:
    raw=[json.loads(x) for x in (root/'教材核对'/f'{v}.jsonl').read_text(encoding='utf-8').splitlines()]
    assert len(raw)==count and [r['page'] for r in raw]==list(range(1,count+1))
    for r in raw:r['text']=r['text'].replace(' ','')
    (root/'教材核对'/f'{v}全文识别.txt').write_text('\n\n'.join(f"=== PDF第{r['page']}页 ===\n{r['text']}" for r in raw),encoding='utf-8')
    audit.append(f'- {v}：{count}页均已识别，页序连续。')
    snippets=[]
    for r in raw:
        for m in re.finditer(r'(?:习题\s*\d|例\s*\d|证明|求证|试求|判断|计算下列|试建立)',r['text']):
            snippets.append({'pdf_page':r['page'],'text':r['text'][max(0,m.start()-12):m.start()+200]})
    (root/'教材核对'/f'{v}题型核对线索.json').write_text(json.dumps(snippets,ensure_ascii=False,indent=2),encoding='utf-8')

(root/'高等数学第八版知识题型数据.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
fragment=(root/'工具'/'math-map-fragment.html').read_text(encoding='utf-8').replace('__MATH_DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/'))
viz=Path(r'C:\Users\xy\.codex\visualizations\2026\10\11\01a1299f-40f2-76a2-b87d-f90d215afaf0')
(viz/'calculus-knowledge-types.html').write_text(fragment,encoding='utf-8')
standalone='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>同济第八版 · 知识与题型思维导图</title><style>
:root{color-scheme:light dark;--background:light-dark(#fafbf8,#161a19);--foreground:light-dark(#23342e,#e3ebe6);--muted-foreground:light-dark(#63756b,#a3b6a9);--border:light-dark(#d4e0d8,#34493d);--viz-series-1:light-dark(#35705b,#86bd9d);--viz-series-2:light-dark(#6d71a7,#aaa9d6);--primary:light-dark(#315c49,#8dc2a0);--primary-foreground:light-dark(#ffffff,#152d20);}
body{margin:0;background:var(--background);color:var(--foreground);font:16px/1.65 system-ui,"Microsoft YaHei",sans-serif;}main{max-width:1100px;margin:32px auto;padding:0 24px;}h2{font-size:24px;font-weight:500;}h3{font-size:20px;font-weight:500;}.text-small{font-size:13px}.form-select{width:100%;box-sizing:border-box;padding:10px 12px;color:var(--foreground);background:var(--background);border:1px solid var(--border);border-radius:8px;font:inherit;}summary{cursor:pointer;}summary:focus-visible,select:focus-visible{outline:2px solid var(--viz-series-1);outline-offset:3px}.source-note{margin-top:24px;color:var(--muted-foreground);font-size:13px;}@media(max-width:560px){main{padding:0 16px;margin:18px auto;}}
</style></head><body><main>'''+fragment+'''<p class="source-note">依据用户下载的同济《高等数学》第八版上下册：上册442页、下册354页。全文OCR与目录核对后归纳；重要主题抽查原页。题型是归类标签，未逐题编号，公式及全部习题尚未逐一人工复核。</p></main></body></html>'''
(root/'高等数学第八版知识与题型思维导图.html').write_text(standalone,encoding='utf-8')

md=['# 同济《高等数学》第八版：知识点与题型细分','','依据用户下载的第八版上下册及全文OCR。★为教材星号内容或该星号节中的主题。下列题型为归类，不等同于每一道习题的独立编号。扫描公式存在识别误差；已对重要主题抽查原图，但未逐题人工复核全部公式。','']
op=ET.Element('opml',version='2.0');head=ET.SubElement(op,'head');ET.SubElement(head,'title').text='同济第八版知识与题型';body=ET.SubElement(op,'body');main=ET.SubElement(body,'outline',text='同济高等数学第八版')
for c in data['chapters']:
    md.extend(['## '+c['title'],'',f"教材印刷页：{c['printPages']}",'']);ch=ET.SubElement(main,'outline',text=c['title'])
    for s in c['sections']:
        md.extend(['### '+s['id']+' '+s['title'],'','**知识点**','']+['- '+x for x in s['knowledge']]+['','**题型**','']+['- '+x for x in s['types']]+[''])
        sec=ET.SubElement(ch,'outline',text=s['id']+' '+s['title'])
        for label,values in [('知识点',s['knowledge']),('题型',s['types'])]:
            group=ET.SubElement(sec,'outline',text=label)
            for x in values:ET.SubElement(group,'outline',text=x)
md.extend(['## 附录与基础工具',''])
app=ET.SubElement(main,'outline',text='附录与基础工具')
for a in data['appendix']:
    md.extend(['### '+a['title'],'']+['- '+p for p in a['points']]+[''])
    node=ET.SubElement(app,'outline',text=a['title'])
    for p in a['points']:ET.SubElement(node,'outline',text=p)
ET.indent(op);ET.ElementTree(op).write(root/'高等数学第八版知识与题型.opml',encoding='utf-8',xml_declaration=True)
(root/'高等数学第八版知识与题型细分.md').write_text('\n'.join(md),encoding='utf-8')
counts={'chapters':len(data['chapters']),'sections':sum(len(c['sections']) for c in data['chapters']),'knowledge':sum(len(s['knowledge']) for c in data['chapters'] for s in c['sections']),'types':sum(len(s['types']) for c in data['chapters'] for s in c['sections'])}
(root/'教材核对'/'核对说明.md').write_text('# 核对记录\n\n'+'\n'.join(audit)+'\n\n'+str(counts)+'\n\n核对方法：全文文字识别、章节目录对齐、例题习题关键词线索提取、重要主题原页抽查。没有把OCR完成视为逐题人工复核。公式OCR不用于原样复刻题目。\n',encoding='utf-8')
print(json.dumps(counts));print('fragment bytes',len(fragment.encode()))
