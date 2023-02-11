import functools
import pathlib
import strings
import subprocess

import regex

DEFAULT_PAGE_TEMPLATE_NAME = 'page_template.html'
IMAGE_FOLDER_PATH = './images/'

SCANNED_PAGE_REGEX = r'(?<=Scan\s*)\d\+'

def read_template_text(filename=DEFAULT_PAGE_TEMPLATE_NAME):
    with open(filename) as fp:
        template_text = fp.read()

def get_substitutions(page_number: int) -> dict[str, str]:
    return {
        "title": f'page {current_page_number}',
        "image_dir": IMAGE_FOLDER_PATH,
        "current_page_number": f'{current_page_number:003}',
        "prev_page_number": f'{(current_page_number - 1):003}',
        "next_page_number": f'{(current_page_number + 1):003}'
    }

@functools.cache
def get_page_number_from_scanned_filename(filename: str) -> int:
    m = SCANNED_PAGE_REGEX.search(filename)
    if not m:
        raise ValueError(f'The filename "{filename}" is not in the correct format.')
    return int(m[0])

def make_page_from_template(template: string.Template, page_number: int) -> str:
    return template.substitute(get_substitutions(page_number))

make_page = functools.partial(make_page_from_template, 
                              template=Template(read_template_text()))

def write_page(page_number: int) -> None:
    page_text: str = make_page(page_number=page_number) 
    pathlib.Path(f'page_{page_number:03}.html').write_text(page_text)

def convert_image_to_jpg(src_filename: str, dest_filename: str, rotate180=True):
    if rotate180:
        return subprocess.run(['convert', 
                              '-monochrome', 
                              '-affine', 
                              '-1,0,0,-1,0,0',
                              '-transform',
                              dest_filename])
    else:
        return subprocess.run(['convert', 
                              '-monochrome', 
                              dest_filename])

def is_tiff_filename(p: pathlib.Path):
    return p.is_file() and p.suffix.lower() == '.tiff'

def get_tiff_files(parent_dir=pathlib.Path.cwd()) -> list[pathlib.Path]:
    if not parent_dir.is_dir():
        raise ValueError("parent_dir must reference a directory")
    return sorted((p for p in parent.iterdir() if is_tiff_filename(p), 
                   key=get_page_number_from_scanned_filename))

def main():
    for src_file in get_tiff_files():
        dest_filename = 


    

if __name__ == '__main__':
    main()



    
