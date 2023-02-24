import functools
import pathlib
import string
import subprocess
import typing

import regex

DEFAULT_PAGE_TEMPLATE_NAME = f'{pathlib.Path(__file__).parent}/page_template.html'
IMAGE_FOLDER_PATH = './images/'

SCANNED_PAGE_REGEX = regex.compile(r'(?<=Scan\s*)\d+')
PAGE_FILENAME_FORMAT = 'page_{:03}.jpg'

def read_template_text(filename=DEFAULT_PAGE_TEMPLATE_NAME):
    with open(filename) as fp:
        template_text = fp.read()

def get_substitutions(current_page_number: int) -> dict[str, str]:
    return {
        "title": f'page {current_page_number}',
        "image_dir": IMAGE_FOLDER_PATH,
        "current_page_number": f'{current_page_number:003}',
        "prev_page_number": f'{(current_page_number - 1):003}',
        "next_page_number": f'{(current_page_number + 1):003}'
    }

@functools.cache
@functools.singledispatch
def get_page_number_from_scanned_filename(filename: str) -> int:
    m = SCANNED_PAGE_REGEX.search(filename)
    if not m:
        raise ValueError(f'The filename "{filename}" is not in the correct '
                          'format.')
    return int(m[0])

@get_page_number_from_scanned_filename.register
def _(p: pathlib.Path) -> int:
    return get_page_number_from_scanned_filename(p.name)

def get_page_name_stem_from_page_number(page_number: int) -> str:
    return PAGE_FILENAME_FORMAT.format(page_number)

def _make_page(template: string.Template, page_number: int) -> str:
    return template.substitute(get_substitutions(page_number))

def _write_page(make_page: typing.Callable, page_number: int) -> None:
    page_text: str = make_page(page_number=page_number) 
    pathlib.Path(f'page_{page_number:03}.html').write_text(page_text)

def convert_image_to_jpg(src_filename: str, dest_filename: str, rotate180=True):
    if rotate180:
        return subprocess.run(['convert', 
                               src_filename,
                              '-monochrome', 
                              '-affine', 
                              '-1,0,0,-1,0,0',
                              '-transform',
                              dest_filename])
    else:
        return subprocess.run(['convert', 
                               src_filename,
                              '-monochrome', 
                              dest_filename])

def is_tiff_filename(p: pathlib.Path):
    return p.is_file() and p.suffix.lower() == '.tiff'

def get_tiff_files(parent_dir=pathlib.Path.cwd()) -> list[pathlib.Path]:
    if not parent_dir.is_dir():
        raise ValueError("parent_dir must reference a directory")
    return sorted ((p for p in parent_dir.iterdir() if is_tiff_filename(p)), 
                   key=get_page_number_from_scanned_filename)

def main():
    template_text = read_template_text()
    make_page = functools.partial(_make_page, template=template_text)
    write_page = functools.partial(_make_page, make_page=make_page)
    
    for src_filename in get_tiff_files(
            pathlib.Path('~/Documents/scanned_documents').expanduser()):
        page_number = get_page_number_from_scanned_filename(src_filename)
        dest_filename_stem = get_page_name_stem_from_page_number(page_number)
        convert_image_to_jpg(src_filename, f'{dest_filename_stem}.jpg')


if __name__ == '__main__':
    main()



    
