#!/usr/bin/env python3

import functools
import logging
import pathlib
import string
import subprocess
import typing

import regex

from toolz.itertoolz import sliding_window

DEFAULT_PAGE_TEMPLATE_NAME = 'page_template.html'

PAGE_NUMBER_RE = regex.compile(r'page(?P<separator>\.|_)(?P<number>\d+)')

ARABIC_TO_ROMAN_MAPPING = {1: 'i', 2: 'ii', 3: 'iii', 4: 'iv', 5: 'v', 6: 'vi', 
                        7: 'vii', 8: 'viii', 9: 'ix', 10: 'x', 11: 'xi', 
                        12: 'xii', 13: 'xiii'}

def read_template_text(filename=DEFAULT_PAGE_TEMPLATE_NAME) -> str:
    with open(filename) as fp:
        return fp.read()

@functools.singledispatch
def extract_page_number(stem: str):
    m: regex.Match = PAGE_NUMBER_RE.search(stem)
    if m:
        separator = m['separator']
        number = int(m['number'])
        
        if separator == '.':
            return ARABIC_TO_ROMAN_MAPPING[number]
        else:
            return number

@extract_page_number.register
def _(p: pathlib.Path):
    return extract_page_number(p.stem)

def get_substitutions(prev: pathlib.Path, \
                      current: pathlib.Path, \
                      next_: pathlib.Path) \
        -> dict[str, str]:
    current_page_number = extract_page_number(current)
    return {
        "title": f'Page {current_page_number}',
        "current_page_number": current_page_number,
        "prev_page": f'{prev.stem}',
        "current_page": f'{current.stem}',
        "next_page": f'{next_.stem}'
    }

def _make_page(template: string.Template, \
        substitutions: dict[str, typing.Any]) -> str:
    return template.substitute(substitutions)

def _write_page(page_text: str, 
                dest_path: pathlib.Path, 
                page_stem: str) -> None:
    pathlib.Path(dest_path / pathlib.Path(f'{page_stem}.html')) \
        .write_text(page_text)

def configure_logging():

    logger = logging.getLogger('root')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
                    '%(asctime)s %(name)s - %(levelname)s - %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    fh = logging.FileHandler('make_html.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

def main():
    configure_logging()
    logger = logging.getLogger('root')
    template_text = read_template_text()
    page_template = string.Template(template_text)
    image_dir= pathlib.Path('~/Documents/scanned_documents/2023_02_24/jpg') \
                    .expanduser()

    jpg_files = sorted(image_dir.glob('*.jpg')) 

    for prev, current, next_ in sliding_window(3, jpg_files):
        filename = current.with_suffix('.html')
        if pathlib.Path(current.parent / filename).exists():
            logging.debug('skipping %s: already exists', filename)
            continue
        else:
            logging.info('will make html page %s', filename)

        substitutions = get_substitutions(prev, current, next_)
        page_text: str = page_template.substitute(substitutions)
        _write_page(page_text, dest_path=image_dir, page_stem=current.stem)

if __name__ == '__main__':
    main()

