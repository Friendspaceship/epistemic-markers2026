from pathlib import Path
import subprocess,os,json
P=Path(__file__).resolve().parent; O=P/'rendered'; O.mkdir(exist_ok=True)
env=dict(os.environ)
settings=[('Stepping_into_a_Fireplace','Preprint candidate',['3. Results','3.4.3 Hogwarts: what distinction is being required?','5. Conclusion']),('technical_companion','Technical companion',['2. Results','2.2 Dimensional Pattern and Historical Sign Summary']),('selected_case_appendix','Selected case appendix',[])]
for token,label,breaks in settings:
 src=next(p for p in P.glob('*.md') if token in p.name)
 cmd=['python3',str(P/'20261116_render_preprint.py'),'--source',str(src),'--output-dir',str(O),'--version','25.31','--date','16 November 2026','--label',label,'--body-font-size','10.2','--table-padding','1','--flow-figures']
 for h in breaks:cmd+=['--page-break-before',h]
 if token=='technical_companion':cmd+=['--page-break-before-paragraph','Nineteen configurations have positive mean Compression Signals']
 subprocess.run(cmd,env=env,check=True,stdout=subprocess.DEVNULL)
 print(label,'rendered',flush=True)
