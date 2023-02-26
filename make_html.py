#!/usr/bin/env python3

import functools
import logging
import pathlib
import string
import subprocess
import typing

DEFAULT_PAGE_TEMPLATE_NAME = 'page_template.html'

def read_template_text(filename=DEFAULT_PAGE_TEMPLATE_NAME) -> str:
    with open(filename) as fp:
        return fp.read()

def get_substitutions(current_page_number: int) -> dict[str, str]:
    return {
        "title": f'page {current_page_number}',
        "current_page_number": f'{current_page_number:003}',
        "prev_page_number": f'{(current_page_number - 1):003}',
        "next_page_number": f'{(current_page_number + 1):003}'
    }

def _make_page(template: string.Template, page_number: int) -> str:
    substitutions: dict[str, str] = get_substitutions(page_number)
    return template.substitute(substitutions)

def _write_page(page_text: str, 
                dest_path: pathlib.Path, 
                page_number: int) -> None:
    pathlib.Path(dest_path / f'page_{page_number:03}.html') \
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

    for p in sorted(image_dir.glob('*.jpg')):
        page_number: int = int(p.name[5:8])
        filename = f'page_{page_number:03}.html'
        if pathlib.Path(p.parent / filename).exists():
            logging.debug('skipping %s: already exists', filename)
            continue
        else:
            logging.info('will make html page %s', filename)

        page_text: str = _make_page(page_template, page_number)
        _write_page(page_text, dest_path=image_dir, page_number=page_number)

if __name__ == '__main__':
    main()

