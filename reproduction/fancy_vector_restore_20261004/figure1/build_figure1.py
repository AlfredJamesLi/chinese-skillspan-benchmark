"""Editable vector reconstruction of the earlier illustrated workflow.

All artwork is drawn from geometric primitives. No bitmap is embedded.
Model icons use neutral symbols unless an exact, permitted official asset is
supplied in the optional official_logo_assets.json mapping.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import json, math, re
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, toColor

O = Path(__file__).resolve().parent
W, H = 1640, 1008
pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold', 'C:/Windows/Fonts/arialbd.ttf'))
c = canvas.Canvas(str(O/'Figure1_fancy_vector.pdf'), pagesize=(W,H))
c.setTitle('Chinese-SkillSpan: corpus, annotation, models and evaluation')
c.setAuthor('Chinese-SkillSpan authors')
c.setSubject('Editable vector reconstruction of the earlier illustrated workflow')
parts=[]
INK='#152432'; BLUE='#1667da'; CYAN='#06add3'; TEAL='#009fac'; GREEN='#00a044'; ORANGE='#f36b23'; PURPLE='#7440d8'; RED='#ec3835'; GREY='#5b6b78'
ASSETS=json.loads((O/'official_logo_assets.json').read_text()) if (O/'official_logo_assets.json').exists() else {}

def path(points, color=INK, width=3, fill=None, close=False, dash=False):
    d='M '+' L '.join(f'{x:.2f},{y:.2f}' for x,y in points)+(' Z' if close else '')
    parts.append(f'<path d="{d}" stroke="{color}" stroke-width="{width}" fill="{fill or "none"}" stroke-linejoin="round" stroke-linecap="round"'+(' stroke-dasharray="9 7"' if dash else '')+'/>')
    p=c.beginPath();p.moveTo(points[0][0], H-points[0][1])
    for x,y in points[1:]:p.lineTo(x,H-y)
    if close:p.close()
    c.setStrokeColor(HexColor(color));c.setLineWidth(width);c.setLineCap(1);c.setLineJoin(1);c.setDash([9,7] if dash else [])
    if fill:c.setFillColor(HexColor(fill))
    c.drawPath(p,stroke=1,fill=bool(fill));c.setDash([])

def bezier(coords,color=INK,width=3,fill=None,close=False):
    # First coordinate is start; following triplets are cubic Bezier controls/end.
    d=f'M {coords[0][0]},{coords[0][1]}';p=c.beginPath();p.moveTo(coords[0][0],H-coords[0][1])
    for i in range(1,len(coords),3):
        a,b,z=coords[i:i+3];d+=f' C {a[0]},{a[1]} {b[0]},{b[1]} {z[0]},{z[1]}'
        p.curveTo(a[0],H-a[1],b[0],H-b[1],z[0],H-z[1])
    if close:d+=' Z';p.close()
    parts.append(f'<path d="{d}" stroke="{color}" stroke-width="{width}" fill="{fill or "none"}" stroke-linecap="round" stroke-linejoin="round"/>')
    c.setStrokeColor(HexColor(color));c.setLineWidth(width)
    if fill:c.setFillColor(HexColor(fill))
    c.drawPath(p,stroke=1,fill=bool(fill))

def rect(x,y,w,h,fill='#ffffff',stroke=INK,r=10,width=2.8):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
    c.setFillColor(HexColor(fill));c.setStrokeColor(HexColor(stroke));c.setLineWidth(width);c.roundRect(x,H-y-h,w,h,r,fill=1,stroke=bool(width))

def ellipse(x,y,rx,ry,color=INK,fill='#ffffff',width=3):
    parts.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill or "none"}" stroke="{color}" stroke-width="{width}"/>')
    c.setStrokeColor(HexColor(color));c.setLineWidth(width)
    if fill:c.setFillColor(HexColor(fill))
    c.ellipse(x-rx,H-y-ry,x+rx,H-y+ry,stroke=1,fill=bool(fill))

def circle(x,y,r,color=INK,fill='#ffffff',width=3):ellipse(x,y,r,r,color,fill,width)

def text(x,y,s,size=25,color=INK,bold=False,anchor='middle',maxw=None):
    font='ArialBold' if bold else 'Arial'
    if maxw and pdfmetrics.stringWidth(s,font,size)>maxw:
        raise ValueError(f'Text overflow ({pdfmetrics.stringWidth(s,font,size):.1f}>{maxw}): {s}')
    parts.append(f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-weight="{"700" if bold else "400"}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{escape(s)}</text>')
    c.setFont(font,size);c.setFillColor(HexColor(color))
    getattr(c,{'middle':'drawCentredString','start':'drawString','end':'drawRightString'}[anchor])(x,H-y,s)

def arrow(points,color=INK,width=3,dash=False):
    path(points,color,width,dash=dash);x,y=points[-1];u,v=points[-2];ang=math.atan2(y-v,x-u)
    path([(x,y),(x-14*math.cos(ang)+6.5*math.sin(ang),y-14*math.sin(ang)-6.5*math.cos(ang)),(x-14*math.cos(ang)-6.5*math.sin(ang),y-14*math.sin(ang)+6.5*math.cos(ang))],color,1,color,True)

def star(x,y,r,color=ORANGE,n=5):
    pts=[]
    for i in range(2*n):
        a=-math.pi/2+i*math.pi/n;rr=r if i%2==0 else r*.4;pts.append((x+rr*math.cos(a),y+rr*math.sin(a)))
    path(pts,color,1,color,True)

def database(x,y,w=58,h=70,color=BLUE):
    rx=w/2;ry=w*.17
    # side shell, then front arcs and the upper ellipse
    rect(x,y+ry,w,h-ry,'#ffffff',color,0,0)
    ellipse(x+rx,y+h-ry,rx,ry,color,'#ffffff',3.5)
    path([(x,y+ry),(x,y+h-ry)],color,3.5);path([(x+w,y+ry),(x+w,y+h-ry)],color,3.5)
    for z in [y+ry+(h-2*ry)*.36,y+ry+(h-2*ry)*.70]:
        bezier([(x,z),(x,z+ry*1.3),(x+w,z+ry*1.3),(x+w,z)],color,3.2)
    ellipse(x+rx,y+ry,rx,ry,color,'#ffffff',3.5)

def doc(x,y,w=53,h=72,color=BLUE,check=False):
    k=w*.27
    path([(x,y),(x+w-k,y),(x+w,y+k),(x+w,y+h),(x,y+h)],color,3.6,'#ffffff',True)
    path([(x+w-k,y),(x+w-k,y+k),(x+w,y+k)],color,3)
    for j in range(3):path([(x+w*.20,y+h*.43+j*h*.16),(x+w*.77,y+h*.43+j*h*.16)],color,3)
    if check:tick(x+w-2,y+h-2,18,GREEN)

def tick(x,y,r=23,color=CYAN):
    circle(x,y,r,color,'#ffffff',3.8);path([(x-r*.5,y),(x-r*.12,y+r*.36),(x+r*.5,y-r*.42)],color,4)

def bot(x,y,s=.7,color=BLUE):
    rect(x-38*s,y-25*s,76*s,56*s,'#f7fcff',color,10*s,3.5)
    path([(x,y-25*s),(x,y-43*s)],color,3);circle(x,y-47*s,5*s,color,'#ffffff',2.5)
    circle(x-15*s,y-3*s,4*s,color,color,2);circle(x+15*s,y-3*s,4*s,color,color,2)
    path([(x-11*s,y+16*s),(x+11*s,y+16*s)],color,3.5)
    for side in [-1,1]:path([(x+44*s*side,y-6*s),(x+44*s*side,y+13*s)],color,3.5)

def chip(x,y,s=.8,color=ORANGE):
    rect(x-22*s,y-22*s,44*s,44*s,'#ffffff',color,3,3.5)
    for q in [-14,-5,5,14]:
        for side in [-1,1]:
            path([(x+q*s,y+22*s*side),(x+q*s,y+31*s*side)],color,3)
            path([(x+22*s*side,y+q*s),(x+31*s*side,y+q*s)],color,3)

def network(x,y,s=.8,color=PURPLE):
    pts=[(x,y-23*s),(x-25*s,y+22*s),(x+25*s,y+22*s)]
    path([pts[0],pts[1],pts[2],pts[0]],color,4)
    for a,b in pts:circle(a,b,9*s,color,'#ffffff',4)

def chat(x,y,s=.8,color=INK):
    bezier([(x-30*s,y),(x-30*s,y-27*s),(x+30*s,y-27*s),(x+30*s,y),(x+30*s,y+20*s),(x+8*s,y+24*s),(x-9*s,y+20*s)],color,3.6)
    path([(x-9*s,y+20*s),(x-22*s,y+31*s),(x-20*s,y+15*s)],color,3.6)
    bezier([(x-20*s,y+15*s),(x-28*s,y+10*s),(x-30*s,y+5*s),(x-30*s,y)],color,3.6)
    for q in [-14,0,14]:circle(x+q*s,y,2.7*s,color,color,1)

def globe(x,y,r=25,color=BLUE):
    circle(x,y,r,color,'#ffffff',3.6);ellipse(x,y,r*.45,r,color,None,2.8)
    ellipse(x,y,r,r*.40,color,None,2.8);path([(x-r,y),(x+r,y)],color,2.8);path([(x,y-r),(x,y+r)],color,2.8)

def official_svg_pdf(root,x,y,size):
    """Render the exact official paths, without rasterization or approximations.

    The two supplied official marks contain filled M/L/H/V/C/Z paths and a
    rounded rectangle. All coordinates are preserved, including asset padding.
    The OpenAI clip rectangles match the asset viewport and do not clip any path.
    Unexpected geometry fails instead of silently changing the mark.
    """
    vx,vy,vw,vh=map(float,root.attrib['viewBox'].split());scale=min(size/vw,size/vh)
    c.saveState();c.translate(x-size/2,H-y+size/2);c.scale(scale,-scale);c.translate(-vx,-vy)
    def visit(e):
        tag=e.tag.split('}')[-1]
        if tag in ['defs','clipPath','title','desc']:return
        if tag in ['svg','g']:
            if 'transform' in e.attrib:raise ValueError('Unexpected transformed official mark')
            for child in e:visit(child)
            return
        if tag=='rect':
            c.setFillColor(toColor(e.attrib.get('fill','#000000')))
            c.roundRect(float(e.attrib.get('x','0')),float(e.attrib.get('y','0')),float(e.attrib['width']),float(e.attrib['height']),float(e.attrib.get('rx','0')),stroke=0,fill=1)
            return
        if tag!='path':raise ValueError('Unsupported official SVG element '+tag)
        tokens=re.findall(r'[A-Za-z]|[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?',e.attrib['d'])
        p=c.beginPath();i=0;cmd=None;px=py=sx=sy=0
        while i<len(tokens):
            if tokens[i].isalpha():cmd=tokens[i];i+=1
            if cmd=='Z' or cmd=='z':p.close();px,py=sx,sy;cmd=None;continue
            if cmd not in ['M','L','H','V','C']:raise ValueError('Unsupported exact path command '+str(cmd))
            n={'M':2,'L':2,'H':1,'V':1,'C':6}[cmd]
            a=list(map(float,tokens[i:i+n]));i+=n
            if cmd=='M':px,py=a;p.moveTo(px,py);sx,sy=px,py;cmd='L'
            elif cmd=='L':px,py=a;p.lineTo(px,py)
            elif cmd=='H':px=a[0];p.lineTo(px,py)
            elif cmd=='V':py=a[0];p.lineTo(px,py)
            elif cmd=='C':p.curveTo(*a);px,py=a[-2:]
        c.setFillColor(toColor(e.attrib.get('fill','#000000')));c.drawPath(p,stroke=0,fill=1,fillMode=1)
    visit(root);c.restoreState()

def model_icon(name,x,y,size=50):
    # An optional genuine official SVG can replace only a permitted mark.
    if name in ASSETS:
        import xml.etree.ElementTree as ET
        fp=Path(ASSETS[name])
        if not fp.is_absolute():fp=O/fp
        root=ET.parse(fp).getroot()
        if any(e.tag.endswith('image') for e in root.iter()):raise ValueError('Raster image inside supplied official SVG')
        vb=root.attrib.get('viewBox','0 0 '+root.attrib.get('width','100')+' '+root.attrib.get('height','100')).split()
        vx,vy,vw,vh=map(float,vb);scale=min(size/vw,size/vh)
        contents=''.join(ET.tostring(ch,encoding='unicode') for ch in root)
        parts.append(f'<g transform="translate({x-size/2},{y-size/2}) scale({scale}) translate({-vx},{-vy})">{contents}</g>')
        official_svg_pdf(root,x,y,size)
        return
    if name=='GPT':chat(x,y,size/65,INK)
    elif name=='Claude':doc(x-size*.33,y-size*.42,size*.56,size*.73,CYAN);chat(x+size*.23,y+size*.24,size/130,CYAN)
    elif name=='DeepSeek':chip(x,y,size/65,BLUE)
    elif name=='Qwen':network(x,y,size/65,PURPLE)
    elif name=='Kimi':network(x,y,size/65,INK)
    else:chip(x,y,size/65,ORANGE)

def cloud(x,y,s=.8,color=CYAN):
    bezier([(x-28*s,y+15*s),(x-52*s,y+16*s),(x-43*s,y-18*s),(x-23*s,y-14*s),(x-22*s,y-39*s),(x+14*s,y-38*s),(x+20*s,y-16*s),(x+46*s,y-17*s),(x+51*s,y+17*s),(x+25*s,y+17*s)],color,3)
    path([(x-28*s,y+15*s),(x+25*s,y+17*s)],color,3)

def building(x,y,s=.8,color=RED):
    path([(x-28*s,y-13*s),(x,y-30*s),(x+28*s,y-13*s),(x-28*s,y-13*s)],color,3,close=True)
    for q in [-20,-7,7,20]:path([(x+q*s,y-8*s),(x+q*s,y+18*s)],color,3)
    path([(x-29*s,y+22*s),(x+29*s,y+22*s)],color,4)

def grad(x,y,s=.8,color=PURPLE):
    path([(x-30*s,y-9*s),(x,y-26*s),(x+30*s,y-9*s),(x,y+8*s)],color,3,'#ffffff',True)
    path([(x-18*s,y),(x-18*s,y+17*s),(x,y+26*s),(x+18*s,y+17*s),(x+18*s,y)],color,3)
    path([(x+30*s,y-9*s),(x+30*s,y+16*s)],color,3)

def funnel(x,y):
    path([(x-25,y-17),(x+25,y-17),(x+8,y+2),(x+8,y+23),(x-8,y+31),(x-8,y+2)],ORANGE,3.5,'#ffffff',True)
    for dx,dy in [(-15,-31),(1,-36),(17,-30)]:star(x+dx,y+dy,5,ORANGE,4)

def split(x,y):
    rect(x-8,y-31,16,14,'#ffffff',PURPLE,1,3);path([(x,y-17),(x,y+1),(x-23,y+1),(x-23,y+16)],PURPLE,3)
    path([(x,y+1),(x+23,y+1),(x+23,y+16)],PURPLE,3);path([(x,y+1),(x,y+16)],PURPLE,3)
    for dx in [-23,0,23]:rect(x+dx-8,y+16,16,14,'#ffffff',PURPLE,1,3)

def target(x,y,r=27):
    circle(x,y,r,RED,'#ffffff',4);circle(x,y,r*.65,RED,'#ffffff',3);circle(x,y,r*.22,RED,RED,1)
    arrow([(x,y),(x+r*.98,y-r*1.02)],RED,3)

def gear(x,y,r=21,color=BLUE):
    pts=[]
    for j in range(32):
        a=j*math.pi/16;rr=r if j%4 in [1,2] else r*.8;pts.append((x+rr*math.cos(a),y+rr*math.sin(a)))
    path(pts,color,3,'#ffffff',True);circle(x,y,r*.37,color,'#ffffff',3)

def cube(x,y,r=22,color=BLUE):
    path([(x,y-r),(x+r,y-r/2),(x+r,y+r/2),(x,y+r),(x-r,y+r/2),(x-r,y-r/2)],color,3,'#ffffff',True)
    path([(x-r,y-r/2),(x,y),(x+r,y-r/2)],color,3);path([(x,y),(x,y+r)],color,3)

# Panels and data flow are drawn before cards, keeping connectors clean.
rect(0,0,W,H,'#ffffff','#ffffff',0,0)
rect(20,15,1600,404,'#fff8f0','#ffc8a6',13,4)
rect(20,432,1600,414,'#eaf4ff','#d0e6fb',13,3)
rect(20,864,1600,125,'#f3efff','#d3c3f5',13,4)
text(38,59,'(a) Corpus & annotation',35,bold=True,anchor='start')
text(38,477,'(b) Models & evaluation',35,bold=True,anchor='start')
text(38,909,'(c) Supplementary',29,bold=True,anchor='start')
text(85,947,'external comparisons',29,bold=True,anchor='start')

for x1,x2 in [(276,319),(540,594),(838,883),(1212,1258)]:arrow([(x1,247),(x2,247)])
arrow([(513,105),(552,67),(977,67),(977,99)],GREEN,4)
text(764,55,'Human coding',26,color=GREEN,bold=True)

rect(36,101,240,300)
rect(320,101,220,300)
rect(594,101,244,300)
rect(884,101,328,300)
rect(1260,101,348,300)

# Recruitment archives: familiar source icons, no company marks.
text(156,142,'Recruitment',29,maxw=216);text(156,173,'archives',29)
rect(111,191,90,59,'#e22b21','#e22b21',0,0);star(127,207,9,'#ffe549')
for sx,sy in [(146,199),(151,210),(150,222),(141,228)]:star(sx,sy,3,'#ffe549')
text(156,278,'Chinese job ads',25,color=BLUE,maxw=217)
bot(69,331,.43,PURPLE);cloud(127,331,.43,CYAN);building(182,332,.50,RED);grad(238,331,.49,PURPLE)
for x,t in [(69,'AI'),(127,'Cloud'),(183,'Public'),(239,'Grad')]:text(x,377,t,18)

# Cleaning and sampling.
text(430,150,'Clean & sample',27,maxw=198)
rect(355,184,42,42,'#ffffff',CYAN,3,3.5);path([(364,204),(374,214),(389,194)],CYAN,3.5)
text(422,214,'Dedup',25,anchor='start')
funnel(377,278);text(422,287,'Clean',25,anchor='start')
split(377,351);text(422,364,'Split',25,anchor='start')

# Silver draft with document/pencil and neutral robot.
text(716,151,'Silver draft',30)
doc(671,190,69,78,PURPLE)
path([(703,258),(743,216),(756,227),(716,270),(701,274)],ORANGE,3,'#ffdc77',True)
path([(743,216),(750,208),(764,220),(756,227)],ORANGE,3,'#fff4d1',True)
bot(716,331,.66,BLUE);text(716,381,'LLM annotator',27)

# Human annotation layer.
text(1048,142,'Human validation',30,maxw=298)
tick(927,186,23,GREEN);text(966,195,'Human audit',27,anchor='start',maxw=226)
rect(908,229,38,40,'#fff4f2',RED,4,2);text(927,256,'CN',19,color=RED,bold=True)
text(961,256,'Chinese boundaries',24,color=RED,anchor='start',maxw=238)
doc(908,290,37,50,BLUE)
text(961,305,'ESCO-informed types',22,color=BLUE,anchor='start',maxw=238)
for x,t,col,fill in [(980,'L',PURPLE,'#e9e0ff'),(1034,'K',CYAN,'#d6f5ff'),(1088,'S',ORANGE,'#ffebba'),(1142,'T',GREEN,'#d9f5e5')]:
    circle(x,337,20,col,fill,1.5);text(x,345,t,24,bold=True)
text(1048,382,'See Figure 2',26,color=BLUE)

# Dataset layers: distinguish the two Silver sizes unambiguously.
text(1434,155,'Chinese-SkillSpan',32,bold=True,maxw=316)
text(1434,190,'Multi-source · ESCO-informed',22,color=RED,maxw=322)
doc(1321,217,64,77,BLUE)
star(1374,291,22,ORANGE,8);circle(1374,291,14,ORANGE,'#fff2c9',2)
database(1486,220,63,78,BLUE)
text(1347,333,'Human reference',22,color=BLUE,maxw=177)
text(1347,364,'150 sentences',20,color=GREY)
text(1520,333,'Silver',24,color=BLUE)
text(1517,360,'Original: 2,451',19,color=GREY,maxw=154)
text(1517,385,'Expanded: 9,540',19,color=GREY,maxw=162)

# Paths from annotation outputs to training and evaluation.
arrow([(1518,405),(1518,436),(22,436),(22,618),(110,618)],ORANGE,3,dash=True)
arrow([(1321,402),(1321,486)],BLUE,3,dash=True)
arrow([(1518,402),(1518,486)],ORANGE,3,dash=True)
text(1284,457,'Human',19,color=BLUE,anchor='end');text(1284,480,'reference',19,color=BLUE,anchor='end')
text(1429,456,'Silver test (Qwen)',18,color=ORANGE);text(1429,480,'Teacher agreement',17,color=ORANGE)

# Training resources and trained systems; prompted baselines have no Silver arrow.
arrow([(442,530),(508,530)])
arrow([(421,618),(467,618),(467,552),(508,552)],ORANGE,3)
arrow([(421,628),(487,628),(487,609),(508,609)],ORANGE,3)
arrow([(421,638),(467,638),(467,687),(508,687)],ORANGE,3)
for yy in [530,609,687]:arrow([(992,yy),(1030,yy)])
arrow([(992,785),(1030,785)])
rect(93,489,349,80)
database(132,501,54,60,CYAN)
text(311,523,'DOMAIN',25,color=BLUE);text(311,551,'PRETRAINING',25,color=BLUE)
rect(110,586,311,95,'#ffffff',ORANGE,10,2.5)
database(140,602,52,63,CYAN)
text(297,622,'Silver labels',25,color=RED);text(297,652,'Train / development',18,color=GREY)
text(374,705,'Supervised training',20,color=ORANGE)

for yy in [489,574,658]:rect(509,yy,483,76)
model_icon('JobBERT',576,527,49);text(791,537,'JobBERT-zh + CRF',28,maxw=375)
model_icon('Qwen',576,612,49);text(791,621,'Qwen2.5-14B-Instruct + LoRA',24,maxw=377)
globe(576,695,25);text(791,690,'XLM-R / ESCOXLM-R',27,maxw=375);text(791,719,'Chinese adaptation',22)

rect(37,749,955,81)
text(55,775,'LLM inference baselines',23,anchor='start')
baseline_positions=[('GPT',118,169),('Claude',285,333),('DeepSeek',475,522),('Qwen',700,746),('Kimi',876,921)]
for name,ix,tx in baseline_positions:
    model_icon(name,ix,803,54 if name=='GPT' else 38)
    text(tx,811,name,23,color=BLUE if name in ['DeepSeek','Qwen'] else INK,anchor='start')

# Evaluation: separate human-reference scoring from teacher agreement.
rect(1031,489,577,341)
text(1319,530,'Evaluation',31,bold=True)
rect(1049,557,263,88,'#ffffff',INK,8,2.5);rect(1327,557,263,88,'#ffffff',INK,8,2.5)
target(1091,602,25);text(1210,611,'Exact F1',31,color=RED)
tick(1369,602,25,CYAN);text(1491,611,'Relaxed F1',29,color=BLUE)
text(1319,680,'Boundary-only · Per-type',23)
rect(1049,698,541,116,'#ffffff',ORANGE,8,2.3)
text(1319,731,'Reproduction materials',26)
doc(1068,750,27,38,BLUE);text(1108,779,'Rules',19,anchor='start')
database(1169,749,29,38,BLUE);text(1208,779,'Manifests',19,anchor='start')
gear(1343,769,19,BLUE);text(1372,779,'Scorer',19,anchor='start')
cube(1473,770,20,BLUE);text(1502,779,'Artifacts',19,anchor='start')

# Supplementary comparisons retain the illustrated style and their proper scope.
rect(528,879,535,93)
doc(551,895,37,58,BLUE);doc(575,903,37,58,GREEN)
text(826,914,'Six public datasets',27)
text(826,949,'XLM-R vs ESCOXLM-R',24,color=BLUE)
rect(1080,879,528,93)
doc(1107,893,44,61,BLUE);circle(1157,933,16,BLUE,'#ffffff',3);path([(1169,945),(1180,956)],BLUE,4)
text(1392,911,'Original-task reruns',27)
text(1392,940,'MaChAmp-CRF · Kompetencer',22,color=BLUE)
text(1392,962,'NNOSE',21,color=BLUE)

c.save()
desc='True vector reconstruction of the earlier illustrated Chinese-SkillSpan workflow, using editable text and geometric paths. Human reference and Silver supervision have distinct roles. Model icons are neutral symbols unless supplied as exact permitted official assets.'
svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><title>Chinese-SkillSpan workflow</title><desc>{escape(desc)}</desc>'+''.join(parts)+'</svg>'
(O/'Figure1_fancy_vector.svg').write_text(svg,encoding='utf-8')
(O/'Figure1_fancy_vector.html').write_text('<!doctype html><meta charset="utf-8"><title>Chinese-SkillSpan workflow</title><style>body{margin:20px;background:#fafafa}svg{width:100%;height:auto}</style>'+svg,encoding='utf-8')
print(O/'Figure1_fancy_vector.pdf')


