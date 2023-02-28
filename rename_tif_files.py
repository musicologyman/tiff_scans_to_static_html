#!/usr/bin/env python3

import argparse
import logging

from collections.abc import Iterable
from pathlib import Path
from typing import Tuple

def get_IMG_files(suffix:str='.tif'):
    return sorted(p for p in Path.cwd().iterdir() 
                  if p.is_file() 
                  and p.suffix == suffix
                  and p.stem.startswith('IMG'))

def get_new_stem(p: Path, adjustment: int) -> str:
    page_number = int(p.stem[-2:]) + adjustment
    return p.with_stem(f'page_{page_number:03}')
    
def get_rename_spec(files: Iterable[Path], adjustment: int) \
        -> Iterable[Tuple[Path, str]]:
    return sorted((p, get_new_stem(p, adjustment)) 
                  for p in files)

def setup_logging():
    logger = logging.getLogger('root')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
                    '%(asctime)s %(name)s - %(levelname)s - %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    log_filename = Path(__file__).with_suffix('.log').name

    fh = logging.FileHandler(log_filename)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


def setup():
    parser = argparse.ArgumentParser()
    parser.add_argument('startpage', type=int, dest='startpage')
    parser.add_argument('suffix', required=False, type=str, dest='suffix', 
                        default='.tif')
    parser.add_argument('--dryrun', action='store_true')
    return parser.parse_args()

def main():
    args = setup()
    adjustment = args.startpage - 1
    suffix = args.suffix
    dryrun = args.dryrun

    logger = setup_logging()
    
    files = get_IMG_files()
    rename_spec = get_rename_spec(files, adjustment)

    if dryrun:
        for p, new_name in rename_spec:
            print(f'renaming {p.name} to {new_name}')
    else:
        for p, new_name in rename_spec:
            logger.debug(f'renaming {p.name} to {new_name}')
            p.rename(new_name)
    
if __name__ == '__main__':
    main()

