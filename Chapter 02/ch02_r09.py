"""Python Cookbook

Chapter 2, recipe 9
"""

from pathlib import Path
import shutil
import os

def version1(source_file_path, target_file_path):
    shutil.copy( str(source_file_path), str(target_file_path) )

def version2(source_file_path, target_file_path):
    try:
        shutil.copy( str(source_file_path), str(target_file_path) )
    except FileNotFoundError:
        os.makedirs( str(target_file_path.parent) )
        shutil.copy( str(source_file_path), str(target_file_path) )
    except OSError as ex:
        print( ex )

if __name__ == "__main__":
    source_path = Path(os.path.expanduser(
       '~/Documents/Writing/Python Cookbook/source'))
    target_path = Path(os.path.expanduser(
       '~/Dropbox/B05442/demo/'))
    for source_file_path in source_path.glob('*/*.rst'):
        source_file_detail = source_file_path.relative_to(source_path)
        target_file_path = target_path / source_file_detail
        version2( source_file_path, target_file_path )
