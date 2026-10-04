"""Restore the established Fancy Figure 2 style using native vector objects.

No image-generation output or bitmap is embedded.
Dependency: reportlab; provide Arial and Comic Sans fonts via --font-dir.
"""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from xml.sax.saxutils import escape
import math
import argparse
parser=argparse.ArgumentParser(description='Build the Fancy Figure 2 as editable SVG and native vector PDF.')
parser.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent)
parser.add_argument('--font-dir',type=Path,default=Path('C:/Windows/Fonts'))
args=parser.parse_args(); O=args.output_dir; O.mkdir(parents=True,exist_ok=True)
pdfmetrics.registerFont(TTFont('Hand',str(args.font_dir/'comic.ttf')))
pdfmetrics.registerFont(TTFont('HandBold',str(args.font_dir/'comicbd.ttf')))
pdfmetrics.registerFont(TTFont('Arial',str(args.font_dir/'arial.ttf')))
W,HT=1600,1140
c=canvas.Canvas(str(O/'Figure2_illustrated.pdf'),pagesize=(W,HT));c.setTitle('Figure 2 — illustrated annotation paths')
parts=[];INK='#24323d';BLUE='#2860d4';TEAL='#079bad';ORANGE='#ec792d';GREEN='#218466';PURPLE='#8661cc';MUTED='#586474'
def path(points,color=INK,width=3,close=False,fill=None,dash=False):
 d='M '+' L '.join(f'{x} {y}' for x,y in points)+(' Z' if close else '')
 parts.append(f'<path d="{d}" stroke="{color}" stroke-width="{width}" fill="{fill or "none"}" stroke-linecap="round" stroke-linejoin="round" '+('stroke-dasharray="8 6"' if dash else '')+'/>')
 p=c.beginPath();p.moveTo(points[0][0],HT-points[0][1])
 for x,y in points[1:]:p.lineTo(x,HT-y)
 if close:p.close()
 c.setStrokeColor(HexColor(color));c.setLineWidth(width);c.setLineCap(1);c.setLineJoin(1);c.setDash([8,6] if dash else [])
 if fill:c.setFillColor(HexColor(fill))
 c.drawPath(p,stroke=1,fill=bool(fill));c.setDash([])
def rect(x,y,w,h,fill='white',stroke=INK,r=15,width=2):
 parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
 c.setFillColor(HexColor(fill) if fill!='white' else HexColor('#ffffff'));c.setStrokeColor(HexColor(stroke));c.setLineWidth(width);c.roundRect(x,HT-y-h,w,h,r,fill=1,stroke=1)
def circle(x,y,r,color=INK,fill='white',width=4):
 parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{color}" stroke-width="{width}"/>')
 c.setStrokeColor(HexColor(color));c.setFillColor(HexColor(fill) if fill!='white' else HexColor('#ffffff'));c.setLineWidth(width);c.circle(x,HT-y,r,stroke=1,fill=1)
def text(x,y,s,size=25,font='Arial',color=INK,anchor='middle'):
 family='Comic Sans MS' if font.startswith('Hand') else 'Arial';weight='bold' if font=='HandBold' else 'normal'
 parts.append(f'<text x="{x}" y="{y}" font-family="{family}" font-weight="{weight}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{escape(s)}</text>')
 c.setFillColor(HexColor(color));c.setFont(font,size);getattr(c,{'middle':'drawCentredString','start':'drawString','end':'drawRightString'}[anchor])(x,HT-y,s)
def arrow(a,b,color=INK,dash=False):
 path([a,b],color,3,dash=dash);x,y=b;u,v=a;ang=math.atan2(y-v,x-u)
 q=[b,(x-13*math.cos(ang)+6*math.sin(ang),y-13*math.sin(ang)-6*math.cos(ang)),(x-13*math.cos(ang)-6*math.sin(ang),y-13*math.sin(ang)+6*math.cos(ang))]
 path(q,color,1,True,color)
def document(x,y,w=65,h=86,color=TEAL,check=False):
 path([(x,y),(x+w-18,y),(x+w,y+18),(x+w,y+h),(x,y+h),(x,y)],color,4,fill='#ffffff')
 path([(x+w-18,y),(x+w-18,y+18),(x+w,y+18)],color,3)
 for j in range(3):path([(x+13,y+32+j*16),(x+w-14,y+32+j*16)],color,3)
 if check:
  circle(x+w-3,y+h-4,20,GREEN,'#f0fbf7',3);path([(x+w-14,y+h-4),(x+w-6,y+h+4),(x+w+8,y+h-13)],GREEN,4)
def person(x,y,color=BLUE,small=False):
 r=17 if small else 20;circle(x,y,r,color,'#f7faff',4)
 path([(x-29,y+66),(x-29,y+44),(x-24,y+32),(x-12,y+26),(x+12,y+26),(x+24,y+32),(x+29,y+44),(x+29,y+66)],color,4,fill='#f3f8ff')
 path([(x-29,y+66),(x+29,y+66)],color,4)
def bot(x,y,color=TEAL):
 rect(x-43,y-29,86,67,'#f1fbfc',color,15,4);path([(x,y-30),(x,y-49)],color,4);circle(x,y-55,6,color,'#ffffff',3)
 circle(x-18,y-4,5,color,color,2);circle(x+18,y-4,5,color,color,2);path([(x-13,y+17),(x+13,y+17)],color,4)
 path([(x-49,y-8),(x-49,y+15)],color,5);path([(x+49,y-8),(x+49,y+15)],color,5)
def stack(x,y,color=BLUE):
 rect(x+12,y+15,98,94,'#f2f7ff',color,9,3);rect(x+5,y+7,98,94,'#ffffff',color,9,3);rect(x,y,98,94,'#ffffff',color,9,4)
 for j in range(3):path([(x+20,y+25+j*19),(x+76,y+25+j*19)],color,4)
def magnify(x,y):
 circle(x,y,43,BLUE,'#f4f8ff',5);circle(x,y,35,BLUE,'#ffffff',2)
 for j in range(3):path([(x-18,y-16+j*15),(x+18,y-16+j*15)],BLUE,4)
 path([(x+30,y+31),(x+57,y+61),(x+69,y+50),(x+42,y+23)],BLUE,4,True,'#d8e7ff')
def badge(x,y,s,color=GREEN):
 wid=pdfmetrics.stringWidth(s,'Arial',23)+36;rect(x-wid/2,y-25,wid,38,'#ffffff',color,17,1.5);text(x,y,s,23,color=color)

rect(0,0,W,HT,'#ffffff','#ffffff',0,0)
text(40,48,'Human annotation and LLM-assisted labeling',36,'HandBold',anchor='start')

# Historical human reference. The later agreement sample never feeds this lane.
text(45,99,'Historical human reference',27,'HandBold',GREEN,'start')
path([(472,91),(1557,91)],'#d8e8e1',2)
arrow((918,225),(1128,225))
text(485,235,'+',43,'HandBold',GREEN)
rect(40,122,405,201,'#fbfdfb','#90b6a5',16,2)
rect(525,122,395,201,'#fbfdfb','#90b6a5',16,2)
rect(1130,122,430,201,'#f6fbff',BLUE,16,2.5)
text(242,160,'Independent coding',28,'HandBold')
person(153,199,BLUE); document(195,184,55,70,TEAL)
person(305,199,TEAL); document(348,184,55,70,BLUE)
text(242,297,'50 sentences · adjudicated',26)
text(722,160,'Collaborative coding',28,'HandBold')
person(625,199,BLUE); person(682,187,TEAL)
document(757,165,69,87,TEAL,True)
text(722,297,'100 sentences · audited',26)
text(1345,160,'Human reference',29,'HandBold',BLUE)
stack(1293,169,BLUE)
circle(1412,250,23,GREEN,'#ffffff',3)
path([(1399,250),(1408,259),(1425,236)],GREEN,4)
text(1345,306,'150 sentences · frozen for scoring',25)
text(1024,264,'combine',23,'Hand',MUTED)

# Historical LLM-assisted supervision and review.
text(45,371,'LLM annotation and sampled review',27,'HandBold',ORANGE,'start')
path([(662,363),(1557,363)],'#f2ddc8',2)
for x in [360,760,1160]:
    arrow((x,511),(x+80,511),INK,x==1160)
for x in [40,440,840]:
    rect(x,397,320,229,'#fffcf8','#d4baa0',16,2)
rect(1240,397,320,229,'#f8fbff','#9aafd5',16,2)
text(200,437,'Initial review',28,'HandBold')
bot(143,516,TEAL); person(267,477,BLUE)
document(221,476,49,62,ORANGE,True)
text(200,585,'100 sentences',26)
text(200,614,'Human review',25,color=MUTED)
text(600,437,'Bulk annotation',28,'HandBold')
document(510,477,53,73,TEAL); bot(630,516,TEAL)
path([(571,513),(587,513)],INK,3)
text(600,597,'LLM-generated labels',26)
text(1000,437,'Expanded Silver',29,'HandBold',ORANGE)
stack(948,446,TEAL)
text(1000,586,'9,540 sentences',28)
text(1000,615,'Expanded Silver pool',25,color=MUTED)
text(1400,437,'Post-generation review',25,'HandBold')
magnify(1387,499)
text(1400,585,'100 original + 150 expanded',22)
text(1400,615,'Sampled quality check',25,color=MUTED)
text(1200,552,'sample',23,'Hand',MUTED)
rect(40,645,1520,48,'#f4f8fb','#d8e3ec',12,1.5)
text(800,677,'Historical coding and review: 500 unique sentences',28,color=INK)

# Separate final-handbook study. Coder preparation has its own arrow, so the
# graphic cannot imply that training removes 20 sentences from the formal 50.
text(45,747,'Final-handbook agreement study',28,'HandBold',PURPLE,'start')
path([(654,739),(1557,739)],'#e8def4',2)
rect(581,768,438,63,'#fcfaff','#b7a2d5',13,2)
text(800,794,'Coder preparation',26,'HandBold',PURPLE)
text(800,820,'5 learning + 15 practice sentences',25)
arrow((800,832),(800,857),PURPLE)

rect(40,860,425,246,'#fcfaff','#b7a2d5',16,2)
rect(583,860,434,246,'#fcfaff','#b7a2d5',16,2)
rect(1135,860,425,246,'#f7fbff','#9aafd5',16,2)
arrow((466,985),(581,985),PURPLE)
arrow((1018,985),(1133,985),PURPLE)

text(252,900,'Agreement sample',29,'HandBold',PURPLE)
stack(200,915,TEAL)
text(252,1060,'50 sentences',29)
text(252,1093,'Silver annotation pool',26,color=MUTED)

text(800,900,'Three independent coders',28,'HandBold',PURPLE)
for px,col in [(683,BLUE),(800,TEAL),(917,PURPLE)]:
    person(px,943,col)
# Vertical dividers illustrate isolated work without suggesting adjudication.
path([(742,925),(742,1018)],'#dbd0e9',2,dash=True)
path([(858,925),(858,1018)],'#dbd0e9',2,dash=True)
text(800,1039,'Machine and peer labels hidden',24)
text(800,1066,'Handbook consultation allowed',24)
text(800,1093,'Individual self-review allowed',24)

text(1347,900,'Agreement assessment',29,'HandBold',BLUE)
document(1312,926,69,88,BLUE,True)
text(1347,1060,'Span F1 · character α',28)
text(1347,1093,'After individual self-review',24,color=MUTED)

c.setTitle('Human annotation, assisted review, and independent blinded agreement')
c.save()
svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {HT}">'
     '<title>Human annotation, assisted review, and independent blinded agreement</title>'
     '<desc>The historical reference and review paths are separate from a final-handbook '
     'study of 50 sampled sentences. Three coders complete training and then work '
     'independently without model suggestions or shared annotations. Agreement is '
     'computed on the latest individual annotations after self-review. The five learning and fifteen practice sentences are excluded from agreement. Historical review covers 100 original-pool sentences and 150 later expanded-pool sentences.</desc>'+''.join(parts)+'</svg>')
(O/'Figure2_illustrated.svg').write_text(svg,encoding='utf-8')
(O/'Figure2_illustrated.html').write_text(
    '<!doctype html><meta charset="utf-8"><style>body{margin:20px;background:#fafafa}'
    'svg{width:100%;height:auto}</style>'+svg,encoding='utf-8')

# Preserve native text and geometry; no bitmap is embedded in these outputs.
import xml.etree.ElementTree as ET, json
root=ET.fromstring(svg)
assert not list(root.iter('{http://www.w3.org/2000/svg}image'))
(O/'design_notes.json').write_text(json.dumps({
 'source_style':'Fancy Figure 2, 2026-10-02',
 'vector_only':True,'historical_human_coverage':500,
 'historical_reference':150,'formal_agreement_sentences':50,
 'preparation_sentences':[5,15],'preparation_excluded_from_agreement':True,
 'formal_annotations':'Latest individual annotations after independent self-review',
 'blinding':'Machine suggestions and other annotators labels hidden',
 'formal_sample_not_model_test':True,
 'fonts':['Arial','Comic Sans MS'],
 'output_size':[W,HT]
},indent=2),encoding='utf-8')
print('Built editable SVG and native vector PDF:',O)
