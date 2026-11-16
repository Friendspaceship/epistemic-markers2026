"""Render this manuscript's Markdown subset to standalone HTML and linked PDF.

Uses installed PyMuPDF, without network calls or package installation. Refuses
unknown block syntax rather than silently dropping text. Source is never edited.
"""
from pathlib import Path
import argparse
import base64
import hashlib
import html
import json
import re
import unicodedata
import xml.etree.ElementTree as ET
import pymupdf


def inline(text):
    protected = []
    def hold(value):
        protected.append(value)
        return f'ZZINLINE{len(protected)-1}ZZ'
    text = re.sub(r'`([^`]+)`', lambda m: hold('<code>'+html.escape(m[1])+'</code>'), text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: hold('<a href="'+html.escape(m[2], quote=True)+'">'+inline(m[1])+'</a>'), text)
    text = re.sub(r'\[\^([^\]]+)\]', lambda m: hold('<sup><a href="#footnote-'+m[1]+'">1</a></sup>'), text)
    text = html.escape(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', text)
    # Permit line breaks in long plain reference URLs without changing visible text.
    text = re.sub(r'https?://[^\s<]+', lambda m: '<span class="url">'+m[0].replace('/', '/\u200b').replace('_', '_\u200b')+'</span>', text)
    for i, value in enumerate(protected):
        text = text.replace(f'ZZINLINE{i}ZZ', value)
    return text


def convert(markdown, source_dir, archive_dir):
    lines = markdown.splitlines()
    blocks, images = [], []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1; continue
        if line.startswith('```'):
            code = []; i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(lines[i]); i += 1
            assert i < len(lines), 'Unclosed code fence'
            blocks.append('<pre>'+html.escape('\n'.join(code))+'</pre>'); i += 1; continue
        if line.startswith('#'):
            m = re.fullmatch(r'(#{1,6}) (.+)', line); assert m, line
            n = len(m[1]); blocks.append(f'<h{n}>'+inline(m[2])+f'</h{n}>'); i += 1; continue
        if line == '>' or line.startswith('> '):
            quote = []
            while i < len(lines) and (lines[i] == '>' or lines[i].startswith('> ')):
                quote.append(inline(lines[i][2:]) if lines[i] != '>' else ''); i += 1
            blocks.append('<blockquote>'+'<br>'.join(quote)+'</blockquote>'); continue
        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                cells = [x.strip() for x in lines[i].strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', x) for x in cells):
                    rows.append(cells)
                i += 1
            assert len({len(row) for row in rows}) == 1
            table = '<table><thead><tr>'+''.join('<th>'+inline(x)+'</th>' for x in rows[0])+'</tr></thead><tbody>'
            for row in rows[1:]:
                table += '<tr>'+''.join('<td>'+inline(x)+'</td>' for x in row)+'</tr>'
            blocks.append(table+'</tbody></table>'); continue
        image = re.fullmatch(r'!\[([^\]]*)\]\(([^)]+)\)', line)
        if image:
            path = (source_dir / image[2]).resolve(); assert path.is_file(), path
            data = path.read_bytes(); mime = 'image/svg+xml' if path.suffix == '.svg' else 'image/png'
            asset = archive_dir / path.name
            asset.write_bytes(data)
            figure = '<div class="figure"><img src="'+asset.name+'" alt="'+html.escape(image[1], quote=True)+'">'
            next_line = i + 1
            while next_line < len(lines) and not lines[next_line].strip():
                next_line += 1
            if next_line < len(lines) and lines[next_line].startswith('**Figure '):
                figure += '<p>'+inline(lines[next_line])+'</p>'
                i = next_line
            blocks.append(figure+'</div>')
            images.append({'filename':asset.name,'mime':mime,'data':data,'source':str(path),'sha256':hashlib.sha256(data).hexdigest()})
            i += 1; continue
        if line.startswith('- '):
            items = []
            while i < len(lines) and lines[i].startswith('- '):
                items.append('<li>'+inline(lines[i][2:])+'</li>'); i += 1
            blocks.append('<ul>'+''.join(items)+'</ul>'); continue
        footnote = re.fullmatch(r'\[\^([^\]]+)\]: (.+)', line)
        if footnote:
            blocks.append('<p class="footnote" id="footnote-'+footnote[1]+'"><sup>1</sup> '+inline(footnote[2])+'</p>')
            i += 1; continue
        para = [line]; i += 1
        while i < len(lines) and lines[i].strip():
            assert not lines[i].startswith(('#','```','|','> ','- ','![')), lines[i]
            para.append(lines[i]); i += 1
        # Author metadata uses explicit line breaks; prose paragraphs wrap normally.
        separator = '<br>' if para[0].startswith('**by ') else ' '
        blocks.append('<p>'+separator.join(inline(x) for x in para)+'</p>')
    return '\n'.join(blocks), images


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--version', default='25.6')
    parser.add_argument('--date', default='9 October 2026')
    parser.add_argument('--label', default='CPT preview')
    parser.add_argument('--body-font-size', type=float, default=10.5)
    parser.add_argument('--page-break-before', action='append', default=[])
    parser.add_argument('--page-break-before-paragraph', action='append', default=[])
    parser.add_argument('--table-padding', type=float, default=2.5)
    parser.add_argument('--flow-figures', action='store_true')
    parser.add_argument('--output-dir', required=True, type=Path)
    args = parser.parse_args()
    assert 9 <= args.body_font_size <= 12, 'Body font must remain within readable manuscript sizes'
    source = args.source.resolve(); out = args.output_dir.resolve(); out.mkdir(parents=True, exist_ok=True)
    assets = out / 'assets'; assets.mkdir(exist_ok=True)
    markdown = source.read_text()
    body, images = convert(markdown, source.parent, assets)
    # Companion Markdown links point to their rendered PDFs in an export bundle.
    body = re.sub(r'href="([^":]+)\.md"', r'href="\1.pdf"', body)
    css = '''
        body { font-family: serif; font-size: 10.5pt; line-height: 1.28; color: #171717; }
        h1 { font-size: 17pt; line-height: 1.14; margin-bottom: 12pt; }
        h2 { font-size: 13pt; margin-top: 15pt; margin-bottom: 6pt; }
        h3 { font-size: 11.5pt; margin-top: 11pt; margin-bottom: 5pt; }
        h1, h2, h3 { page-break-after: avoid; }
        p { margin: 0 0 8pt 0; }
        a { color: #174d74; text-decoration: none; }
        blockquote { margin: 9pt 18pt 12pt; font-style: italic; }
        table { page-break-inside: avoid; width: 100%; border-collapse: collapse; margin: 9pt 0; font-size: 8pt; }
        th, td { border-bottom: 0.5pt solid #c9c9c9; padding: 2.5pt 3pt; vertical-align: top; }
        th { text-align: left; font-weight: bold; }
        tr { page-break-inside: avoid; }
        .figure { margin: 12pt 0 5pt; page-break-before: always; page-break-inside: avoid; }
        img { width: 100%; }
        .footnote { font-size: 8pt; line-height: 1.2; }
        .url { font-size: 8pt; }
        ul { padding-left: 17pt; margin: 0 0 8pt; }
        li { margin-bottom: 5pt; }
        code { font-family: monospace; font-size: 8.2pt; }
        pre { font-family: monospace; font-size: 8pt; line-height: 1.2; white-space: pre-wrap; margin: 8pt 0; }
    '''
    if args.flow_figures:
        css = css.replace('page-break-before: always; page-break-inside: avoid;', 'page-break-inside: avoid;')
    assert 1 <= args.table_padding <= 4
    css = css.replace('padding: 2.5pt 3pt;', f'padding: {args.table_padding}pt 3pt;')
    css = css.replace('font-size: 10.5pt;', f'font-size: {args.body_font_size}pt;', 1)
    pdf_name = source.stem + '.pdf'
    html_name = source.stem + '.html'
    title = markdown.splitlines()[0].removeprefix('# ')
    standalone = body
    for image in images:
        encoded = base64.b64encode(image['data']).decode()
        standalone = standalone.replace('src="'+image['filename']+'"', 'src="data:'+image['mime']+';base64,'+encoded+'"')
    document = '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>'+html.escape(title)+'</title><style>'+css+'body {max-width: 850px; margin: 40px auto; padding: 0 24px;} @media print { body {max-width:none; margin:0;} }</style></head><body>'+standalone+'</body></html>'
    (out / html_name).write_text(document)
    pdf_body = body
    for prefix in args.page_break_before_paragraph:
        token = '<p>' + inline(prefix)
        assert pdf_body.count(token) == 1, ('Paragraph prefix must match exactly once', prefix)
        pdf_body = pdf_body.replace(token, '<p style="page-break-before:always">' + inline(prefix), 1)
    for heading in args.page_break_before:
        tokens = [f"<h{level}>"+inline(heading)+f"</h{level}>" for level in range(1, 7)]
        matches = [token for token in tokens if token in pdf_body]
        assert len(matches)==1 and pdf_body.count(matches[0])==1, heading
        token = matches[0]
        opening = token[:token.index(">")+1]
        pdf_body = pdf_body.replace(token, token.replace(opening, opening[:-1]+' style="page-break-before:always">', 1))
    for image in images:
        if image['mime'] == 'image/svg+xml':
            # Story does not display SVG <img> reliably. Render the unchanged SVG
            # locally at print resolution for PDF; standalone HTML retains SVG.
            # MuPDF SVG rendering can ignore class-based text styles. Resolve
            # this figure's simple CSS rules into equivalent SVG attributes.
            tree = ET.fromstring(image['data'])
            rules = []
            for style in tree.iter('{http://www.w3.org/2000/svg}style'):
                for selector, declarations in re.findall(r'([^{}]+)\{([^{}]+)\}',style.text or ''):
                    attrs = dict(part.strip().split(':',1) for part in declarations.split(';') if part.strip())
                    rules.append((selector.strip(),attrs))
            for element in tree.iter():
                tag = element.tag.rsplit('}',1)[-1]
                classes = element.get('class','').split()
                for selector,attrs in rules:
                    if selector==tag or (selector.startswith('.') and selector[1:] in classes):
                        for key,value in attrs.items():
                            element.set(key,value.removesuffix('px') if key=='font-size' else value)
            svg = pymupdf.open(stream=ET.tostring(tree), filetype='svg')
            raster_name = Path(image['filename']).stem + '_pdf.png'
            svg[0].get_pixmap(matrix=pymupdf.Matrix(2,2),alpha=False).save(assets / raster_name)
            pdf_body = pdf_body.replace('src="'+image['filename']+'"','src="'+raster_name+'"')
    page = pymupdf.Rect(0,0,595.28,841.89)
    content = pymupdf.Rect(48,42,547.28,793.89)
    def rectfn(rect_num, filled):
        assert rect_num < 100, 'Unexpected pagination runaway'
        return page, content, None
    headings = {html.unescape(re.sub('<[^>]+>', '', m[2])):m[0] for m in re.finditer(r'<h([1-6])>(.*?)</h\1>',pdf_body)}
    moved_headings = []
    for attempt in range(4):
        story = pymupdf.Story(html=pdf_body, user_css=css, archive=pymupdf.Archive(str(assets)))
        pdf = story.write_with_links(rectfn)
        orphaned = []
        for rendered_page in pdf:
            text_lines = rendered_page.get_text().strip().splitlines()
            if text_lines:
                last = unicodedata.normalize('NFKC',text_lines[-1]).strip()
                if last in headings:
                    orphaned.append(last)
        if not orphaned:
            break
        assert attempt < 3, 'Unresolved orphan section headings'
        for heading in orphaned:
            old = headings[heading]
            assert old in pdf_body and heading not in moved_headings, heading
            pdf_body = pdf_body.replace(old,old.replace('>', ' style="page-break-before:always">',1))
            moved_headings.append(heading)
        pdf.close()
    pdf.set_metadata({'title':title,'author':'Daniel Fenge','subject':args.label+', Version '+args.version+', '+args.date,'keywords':'TruthfulQA, CPT, Anchor-5, preprint candidate'})
    for n, p in enumerate(pdf):
        p.insert_text((48,817), args.label+' | Version '+args.version+' | '+args.date, fontsize=8, color=(0.35,0.35,0.35))
        p.insert_text((520,817), str(n+1), fontsize=8, color=(0.35,0.35,0.35))
    pdf.save(out / pdf_name, garbage=4, deflate=True)
    record = {'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'html':str(out/html_name),'pdf':str(out/pdf_name),'pages':len(pdf),'figures':[{k:v for k,v in item.items() if k!='data'} for item in images],'renderer':'installed PyMuPDF Story '+pymupdf.VersionBind,'headings_moved_to_avoid_orphans':moved_headings,'requested_page_breaks':args.page_break_before,'network_calls':0}
    record['body_font_size_pt'] = args.body_font_size
    record['table_padding_pt'] = args.table_padding
    record['flow_figures'] = args.flow_figures
    record['requested_paragraph_breaks'] = args.page_break_before_paragraph
    (out / (source.stem + '_render_record.json')).write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k!='figures'},indent=2))


if __name__ == '__main__':
    main()
