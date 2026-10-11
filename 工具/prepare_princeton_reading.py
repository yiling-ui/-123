from pathlib import Path
import json,re

root=Path(__file__).parent.parent/'普林斯顿阅读'
starts=[1,21,34,47,63,84,111,132,148,182,203,220,240,264,277,295,323,349,374,394,411,435,457,475,490,505,526,541,559,581,601,633,644,647,651]
names=['函数、图像和直线','三角学回顾','极限导论','多项式与有理函数极限','连续性和可导性','求解微分问题','三角函数极限和导数','隐函数求导和相关变化率','指数函数和对数函数','反函数和反三角函数','导数和图像','绘制函数图像','最优化和线性化','洛必达法则及极限综述','积分入门','定积分','微积分基本定理','积分方法第一部分','积分方法第二部分','反常积分基本概念','反常积分解题','数列和级数基本概念','级数解题','泰勒多项式、泰勒级数和幂级数','估算问题','泰勒级数和幂级数解题','参数方程和极坐标','复数','体积、弧长和表面积','微分方程','附录A：极限及其证明','附录B：估算积分','符号列表','索引']
rows=[json.loads(x) for x in (root/'全书.jsonl').read_text(encoding='utf-8').splitlines()]
for r in rows:r['text']=r['text'].replace(' ','')
chapters=[]
for i,(a,b,name) in enumerate(zip(starts,starts[1:],names),1):
    pages=[r for r in rows if a+20<=r['page']<b+20]
    (root/f'{i:02d}-{name}.txt').write_text('\n\n'.join(f"PDF {r['page']} / 原书 {r['page']-20}\n{r['text']}" for r in pages),encoding='utf-8')
    # 每页保留解释性语句作为阅读导航，全文另存，不将导航当作全文。
    digest=[]
    for r in pages:
        sentences=re.split(r'[。．！？]',r['text'])
        prose=[s for s in sentences if len(re.findall(r'[\u4e00-\u9fff]',s))>=16]
        ranked=[s for s in prose if re.search(r'注意|为什么|记住|关键|重要|总结|方法|步骤|因此|直观|定义|意味着|错误|条件',s)]
        chosen=(ranked or prose)[:2]
        digest.append(f"p{r['page']-20}: "+'。'.join(s[:125] for s in chosen))
    chapters.append({'chapter':i,'name':name,'pages':[a,b-1],'navigation':digest})
(root/'逐页阅读导航.json').write_text(json.dumps(chapters,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'全文识别.txt').write_text('\n\n'.join(f"=== PDF {r['page']} ===\n{r['text']}" for r in rows),encoding='utf-8')
print('OCR pages',len(rows),'chars',sum(len(r['text']) for r in rows),'navigation chars',sum(len(s) for c in chapters for s in c['navigation']))
