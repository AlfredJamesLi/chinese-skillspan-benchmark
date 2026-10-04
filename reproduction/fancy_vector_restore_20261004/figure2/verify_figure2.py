"""Render and structurally verify the native-vector Figure 2 PDF/SVG. Requires PyMuPDF."""
from pathlib import Path
import fitz,json,hashlib,xml.etree.ElementTree as E
p=Path(__file__).resolve().parent
d=fitz.open(str(p/'Figure2_illustrated.pdf'));x=d[0]
x.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).save(str(p/'Figure2_illustrated.png'))
t=x.get_text();s=E.parse(str(p/'Figure2_illustrated.svg'));ns='{http://www.w3.org/2000/svg}'
r={'pdf_pages':len(d),'pdf_embedded_images':len(x.get_images(full=True)),'pdf_vector_drawings':len(x.get_drawings()),'pdf_text_chars':len(t),'svg_images':len(list(s.iter(ns+'image'))),'svg_paths':len(list(s.iter(ns+'path'))),'svg_text_nodes':len(list(s.iter(ns+'text'))),'latest_self_review_present':'After individual self-review' in t,'svg_description_updated':'before discussion' not in (p/'Figure2_illustrated.svg').read_text(encoding='utf-8'),'contains_obsolete_terms':any(v in t for v in ['Silver-plus','Random sampling','Frozen annotations','Silver teacher pool']),'visual_inspection_complete':False,'sha256':{z.name:hashlib.sha256(z.read_bytes()).hexdigest() for z in p.iterdir() if z.suffix in ['.pdf','.svg','.png','.py']}}
assert r['pdf_embedded_images']==r['svg_images']==0
assert not r['contains_obsolete_terms']
assert r['latest_self_review_present'] and r['svg_description_updated']
(p/'validation.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
(p/'extracted_text.txt').write_text(t,encoding='utf-8')
print(json.dumps(r,indent=2))
