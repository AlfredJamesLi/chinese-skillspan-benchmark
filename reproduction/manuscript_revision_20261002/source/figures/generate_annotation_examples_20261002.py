"""Editable vector presentation of the eight current-handbook examples.

Run with Python and reportlab. Fonts are embedded in the PDF. Optional font
environment variables CNSS_CN_FONT, CNSS_EN_FONT and CNSS_EN_BOLD may point
to equivalent Unicode TrueType fonts on non-Windows systems. Highlights
apply only to Chinese source spans. English is explanatory, not annotation.
"""
from pathlib import Path
import json,os,re
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor,white

ROOT=Path(__file__).resolve().parent
PDF=ROOT/'annotation_examples_highlighted_20261002.pdf'
JSON=ROOT/'annotation_examples_highlighted_20261002.json'
pdfmetrics.registerFont(TTFont('CN',os.getenv('CNSS_CN_FONT','C:/Windows/Fonts/simsun.ttc'),subfontIndex=0))
pdfmetrics.registerFont(TTFont('EN',os.getenv('CNSS_EN_FONT','C:/Windows/Fonts/arial.ttf')))
pdfmetrics.registerFont(TTFont('ENB',os.getenv('CNSS_EN_BOLD','C:/Windows/Fonts/arialbd.ttf')))
EXAMPLES=[
 {'title':'Complete boundary','parts':[('熟悉',None),('支持服务','S')],'explanation':'Support services: retain the complete term. Familiarity supplies context.'},
 {'title':'Separate activities','parts':[('维护','S'),('和',None),('支持服务','S')],'explanation':'Maintenance and support services: two independently meaningful activities.'},
 {'title':'Shared action','parts':[('优化曝光与转化率','S')],'explanation':'Optimize exposure and conversion rate: retain one action with both objects.'},
 {'title':'Contextual type','parts':[('使用',None),('SQL','S'),('; ',None),('SQL原理','K')],'explanation':'Using SQL denotes skill; SQL principles denote knowledge.'},
 {'title':'Omitted referent','parts':[('熟悉',None),('Linux基本操作','S'),('和',None),('原理','K')],'explanation':'Basic Linux operations and principles: the second span refers back to Linux without copying it (case 130).'},
 {'title':'Colloquial capability','parts':[('会聊天','T')],'explanation':'Being good at conversation: retain the modal within the capability expression.'},
 {'title':'Experience scope','parts':[('大项目售前','S'),('经验; ',None),('机器人竞赛经验','S')],'explanation':'Presales activities stand without the experience qualifier; robotics-competition experience retains it.'},
 {'title':'Transversal or technical','parts':[('客户汇报','T'),('; ',None),('接口对接','S')],'explanation':'Client reporting is communication (T); interface integration is a technical operation (S).'}
]
FILL={'K':'#B9EEF0','S':'#FAED99','T':'#C6EBCB'}
EDGE={'K':'#167E87','S':'#987500','T':'#278846'}
W=510.;GAP=12.;CW=(W-GAP)/2.;PAD=10.;TEXT=CW-2*PAD
CNFS=14.;ENFS=11.;LEAD=14.;CNL=21.
def width(t,f,s):return pdfmetrics.stringWidth(t,f,s)
def wrap(t,maxw):
 lines=[];line=''
 for word in t.split():
  test=(line+' '+word).strip()
  if width(test,'EN',ENFS)>maxw and line:lines.append(line);line=word
  else:line=test
 if line:lines.append(line)
 return lines
def layout(parts):
 placed=[];x=0.;row=0
 for txt,label in parts:
  words=[txt] if label else re.findall(r'[A-Za-z]+|[^A-Za-z]',txt)
  for word in words:
   if not word:continue
   base=width(word,'CN',CNFS);boxw=base+(12 if label else 0)
   if x and x+boxw>TEXT:row+=1;x=0.
   assert boxw<=TEXT,(word,boxw)
   placed.append((x,row,word,label,base));x+=boxw
 return placed,row+1
for ex in EXAMPLES:
 ex['layout'],ex['cn_lines']=layout(ex['parts']);ex['en_lines']=wrap(ex['explanation'],TEXT)
 ex['height']=27+ex['cn_lines']*CNL+7+len(ex['en_lines'])*LEAD+10
heights=[max(EXAMPLES[i]['height'],EXAMPLES[i+1]['height']) for i in range(0,8,2)]
H=sum(heights)+3*8+29
c=canvas.Canvas(str(PDF),pagesize=(W,H),pageCompression=1)
c.setTitle('Chinese annotation boundaries and contextual types')
c.setAuthor('Chinese-SkillSpan authors')
def text(x,y,t,font='EN',fs=11,color='#202C39'):
 c.setFillColor(HexColor(color));c.setFont(font,fs);c.drawString(x,y,t)
legend=[('K','Knowledge'),('S','Occupational skill'),('T','Transversal competence')]
x=5
for code,label in legend:
 c.setFillColor(HexColor(FILL[code]));c.roundRect(x,H-17,14,14,2,fill=1,stroke=0)
 text(x+3,H-14,code,'ENB',10);text(x+20,H-14,label,'EN',10.6)
 x+=width(label,'EN',10.6)+48
top=H-29
for row,rh in enumerate(heights):
 for col in range(2):
  i=row*2+col;ex=EXAMPLES[i];x=col*(CW+GAP);bottom=top-rh
  c.setFillColor(white);c.setStrokeColor(HexColor('#CBD7E3'));c.setLineWidth(.75);c.roundRect(x+.5,bottom+.5,CW-1,rh-1,5,fill=1,stroke=1)
  text(x+PAD,top-17,chr(97+i)+') '+ex['title'],'ENB',11.4)
  basey=top-39
  for dx,line,word,label,tw in ex['layout']:
   xx=x+PAD+dx;yy=basey-line*CNL
   if label:
    c.setFillColor(HexColor(FILL[label]));c.roundRect(xx-1,yy-2,tw+2,CNFS+3,1.5,fill=1,stroke=0)
    c.setStrokeColor(HexColor(EDGE[label]));c.setLineWidth(.65);c.line(xx,yy-2,xx+tw,yy-2)
   text(xx,yy,word,'CN',CNFS,'#111820')
   if label:text(xx+tw+2,yy+3,label,'ENB',8,EDGE[label])
  y=basey-(ex['cn_lines']-1)*CNL-22
  for line in ex['en_lines']:text(x+PAD,y,line,'EN',ENFS);y-=LEAD
  assert y+LEAD>=bottom+9,(ex['title'],y,bottom)
 top-=rh+8
c.showPage();c.save()
out=[]
for ex in EXAMPLES:
 source=''.join(t for t,k in ex['parts']);offset=0;spans=[]
 for t,k in ex['parts']:
  if k:spans.append({'start':offset,'end':offset+len(t),'type':k,'text':t})
  offset+=len(t)
 out.append({'decision':ex['title'],'source':source,'spans':spans,'english_explanation':ex['explanation']})
JSON.write_text(json.dumps({'purpose':'Illustrative current-handbook examples, not newly labeled study records','types_shown':['K','S','T'],'examples':out,'page_size_pt':[W,H]},ensure_ascii=False,indent=2),encoding='utf-8')
print('Vector figure generated:',W,H,'pt;',len(out),'examples')
