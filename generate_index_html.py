#!/usr/bin/env python3

from functools import partial
from io import StringIO
from pathlib import Path


STYLE_BLOCK = """.toc {
    font-family: Arial, Helvetica, Sans-Serif;
    width: 30%;
    margin: auto;
}
.toc-entry {
    float: left;
    width: 10%;
}
a:link, a:visited {
    color: navy;
}
"""

def get_html_files(parent: Path=Path.cwd()):
    return sorted(p.name for p in parent.iterdir() 
                    if p.is_file() and p.suffix=='.html')

def extract_page_number(filename):
    try:
        return int(filename[5:8])
    except ValueError:
        return -1
        
def get_max_page_number(html_files):
    return max(extract_page_number(filename) for filename in html_files)

def get_toc_entries(max_page_number):
    for i in range(1, max_page_number + 1):
        filename = f'page_{i:03}.html'
        if Path(filename).exists():
            yield f'<a href="{filename}">{i}</a>'
        else:
            yield str(i)

def build_toc_entries(max_page_number):
    with StringIO() as sp:
        prints = partial(print, file=sp)
        for i, entry in enumerate(get_toc_entries(max_page_number)):
            prints(f'<div class="toc-entry">{entry}</div>')
            if i % 10 == 9:
                prints('<br>')
        return sp.getvalue().rstrip()

def build_toc(max_page_number):
    with StringIO() as sp:
        prints = partial(print, file=sp)
        prints(f'<div class="toc">')
        prints(build_toc_entries(max_page_number))
        prints(f'</div>', file=sp)
        return sp.getvalue().rstrip()

def write_body(content):
    with StringIO() as sp:
        prints = partial(print, file=sp)
        prints('<body>')
        prints(content)
        prints('</body>')
        return sp.getvalue().rstrip()

def write_head(title, styles=None):
    with StringIO() as sp:
        prints = partial(print, file=sp)
        prints('<head>')
        prints('<meta http-equiv="cache-control" content="no-cache">')
        prints(f'<title>{title}</title>')
        if styles:
            prints('<style>')
            prints(styles)
            prints('</style>')
        prints('<head>')
        return sp.getvalue().rstrip()

def write_index_file(filename='index.html'):
    with open(filename, mode='w') as fp:
        printf = partial(print, file=fp)
        printf('<html>')
        printf(write_head('Page Images', styles=STYLE_BLOCK))
        files = get_html_files()
        max_page_number = get_max_page_number(files)
        body_content = build_toc(max_page_number)
        printf(write_body(body_content))
        printf('</html>')

def main():
    write_index_file()

if __name__ == '__main__':
    main()
    

