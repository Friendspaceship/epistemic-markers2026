from pathlib import Path
import json,html,hashlib,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'20261116_aggregate_results.json'
OUT=ROOT/'figures'
DIMS=['reality','knowledge','goal','visibility','agency','self_reflexivity','boundary']
NAMES=['Reality','Knowledge','Goal','Visibility','Agency','Self-Reflexivity','Boundary']
def build():
 rows=json.loads(SOURCE.read_text())['configurations'];assert len(rows)==21
 OUT.mkdir(parents=True,exist_ok=True);records=[]
 def start(w,h,title,sub):return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{html.escape(title)}</title><desc>{html.escape(sub)}</desc><rect width="100%" height="100%" fill="white"/>']
 def text(a,x,y,s,size=17,anchor='start',fill='#202832',weight='normal'):a.append(f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" text-anchor="{anchor}" fill="{fill}" font-weight="{weight}">{html.escape(str(s))}</text>')
 def line(a,x1,y1,x2,y2,color='#d6dce2'):a.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}"/>')
 def color(v):
  base=(38,102,156) if v>=0 else (183,71,34);t=min(abs(v)/2,1)
  return '#'+''.join(f'{round(255+(c-255)*t):02x}' for c in base)
 def save(a,name,values):
  a.append('</svg>');p=OUT/name;p.write_text('\n'.join(a)+'\n')
  root=ET.parse(p).getroot();parsed=[float(e.attrib['data-value']) for e in root.iter() if 'data-value' in e.attrib]
  assert parsed==values
  for e in root.iter():
   if e.tag.endswith('rect'):assert float(str(e.attrib.get('width',0)).rstrip('%'))>=0 and float(str(e.attrib.get('height',0)).rstrip('%'))>=0
  records.append({'file':name,'values':parsed,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 foot=133+36*len(rows)+36
 a=start(1120,foot+117,'Seven-dimensional score differences','Twenty-one configurations; GPT-4o minus reference, original0–2scale.')
 text(a,24,35,'Seven-dimensional score differences',25,weight='bold');text(a,24,64,'GPT-4o minus reference mean score · original 0–2 scale',18)
 text(a,24,105,'Evaluator configuration',17,weight='bold');text(a,274,105,'N',17,anchor='end',weight='bold')
 for j,n in enumerate(NAMES):
  if n=='Self-Reflexivity':text(a,347+116*j,95,'Self-',16,'middle');text(a,347+116*j,116,'Reflexivity',16,'middle')
  else:text(a,347+116*j,108,n,16,'middle')
 values=[]
 for i,r in enumerate(rows):
  y=133+36*i;mark=' ‡' if r['panel_role']=='later_extension' else ''
  text(a,24,y+24,r['label']+mark,17);text(a,274,y+24,r['n'],16,'end')
  for j,d in enumerate(DIMS):
   v=r['gaps'][d];x=290+116*j
   a.append(f'<rect x="{x}" y="{y}" width="112" height="33" fill="{color(v)}" data-value="{v}"/>')
   text(a,x+56,y+23,f'{v:+.3f}',17,'middle','white' if abs(v)>1.4 else '#162532');values.append(v)
 text(a,24,foot,'‡ Six extensions beyond the historical fifteen.',17);text(a,24,foot+26,'Ordered by mean Compression Signal; differing execution conditions are retained.',17)
 for i in range(200):a.append(f'<rect x="{290+2.8*i}" y="{foot+47}" width="3" height="17" fill="{color(-2+4*i/199)}"/>')
 for v in [-2,-1,0,1,2]:text(a,290+(v+2)*140,foot+88,f'{v:+d}' if v else '0',16,'middle')
 text(a,24,foot+65,'Color scale',16);save(a,'20261116_dimension_gaps21.svg',values)
 bottom=97+36*len(rows)
 a=start(1120,bottom+115,'Mean Compression Signal','Nineteen positive and two negative mean contrasts in21configurations.')
 text(a,24,35,'Mean Compression Signal',25,weight='bold');text(a,24,64,'GPT-4o minus reference Awareness Index · normalized 0–1 indices',18)
 x=lambda v:310+(v+.1)/.8*720
 for tick in range(-1,8):
  v=tick/10;line(a,x(v),90,x(v),bottom+8,'#666' if tick==0 else '#d6dce2');text(a,x(v),bottom+38,f'{v:+.1f}',16,'middle')
 values=[]
 for i,r in enumerate(rows):
  y=97+36*i;v=r['CS'];text(a,24,y+22,r['label'],17)
  a.append(f'<rect x="{min(x(0),x(v))}" y="{y}" width="{abs(x(v)-x(0))}" height="26" fill="{("#376d96" if v>=0 else "#b74722")}" data-value="{v}"/>')
  text(a,x(v)+(9 if v>=0 else -9),y+21,f'{v:+.3f}',17,'start' if v>=0 else 'end');values.append(v)
 text(a,24,bottom+82,'Ordered descriptive contrasts, not a ranking of evaluator quality.',17)
 save(a,'20261116_compression_signal21.svg',values)
 selected=[next(r for r in rows if r['key']==k) for k in ['sol','sol61','astra']]
 colors=['#376d96','#b74722','#76549a'];a=start(1140,680,'Earlier Sol and new Sol/Astra dimensional profiles','Each817pairs; old/newexecutionconditionsdiffer; newSol/Astrarequestsmatchexceptmodel.')
 text(a,24,35,'Earlier Sol and new Sol/Astra: dimensional profiles',25,weight='bold');text(a,24,64,'GPT-4o minus reference mean score · original 0–2 scale · 817 pairs per run',18)
 for i,(r,col) in enumerate(zip(selected,colors)):
  xx=260+i*260;a.append(f'<rect x="{xx}" y="85" width="16" height="16" fill="{col}"/>');text(a,xx+24,99,r['label'],16)
 x=lambda v:660+v*900
 for v in [-.4,-.2,0,.2,.4]:line(a,x(v),120,x(v),604,'#666' if v==0 else '#d6dce2');text(a,x(v),634,f'{v:+.1f}',16,'middle')
 values=[]
 for i,(dim,name) in enumerate(zip(DIMS,NAMES)):
  y=128+67*i;text(a,24,y+30,name,18)
  for j,(r,col) in enumerate(zip(selected,colors)):
   v=r['gaps'][dim];yy=y+16*j
   a.append(f'<rect x="{min(x(0),x(v))}" y="{yy}" width="{abs(x(v)-x(0))}" height="13" fill="{col}" data-value="{v}"/>');text(a,1090,yy+12,f'{v:+.3f}',13,'end',col);values.append(v)
 text(a,24,666,'Historical comparison is descriptive; model and execution settings differ.',16)
 save(a,'20261116_sol_astra_profiles.svg',values)
 (OUT/'20261116_figure_values.json').write_text(json.dumps(records,indent=2)+'\n')
 print(json.dumps({'figures':len(records),'marks':[len(r['values']) for r in records]}))
if __name__=='__main__':build()
