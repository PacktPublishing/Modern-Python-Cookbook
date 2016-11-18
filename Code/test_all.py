"""
Test all of the code modules that can be tested with doctest.

There are several passes.

1.  Doctest most of the examples.

2.  For a few files, run them as separate modules because they
    have an explicit requirement for the test cases to be run as the top-level
    __main__ module.

3.  Locate all of the files with unittest, and run those with :mod:`runpy`.
    These must all have exit=False so that the overall script runs.

Note that `unittest.mock.call` breaks doctest's discovery. We have two choices.

1.  Choose wisely what to discover.
2.  Don't use ``from unittest.mock import call``.

We opt for the second option, and run the unittest modules with :mod:`runpy`.
"""

import doctest
from pathlib import Path
import os
import importlib
import sys
import runpy
import unittest

code = Path('.')

# 1. Run all the doctest examples. With two sets of exceptions.
runner = doctest.DocTestRunner()
noisy_doctest_finder = doctest.DocTestFinder(verbose=True)

# Exclude these modules becaues they assume that they're run
# as __main__.
name_exclude = ['ch07_r02', 'ch07_r06a', 'ch09_r03', 'ch13_r02']

# Exclude these because the flask decorators break doctest.
flask_exclude = ['ch12_r02', 'ch12_r03', 'ch12_r05_server',
    'ch12_r06_server', 'ch12_r07_server']

for chapter_file in Path('.').glob('*.py'):
    if chapter_file.name.startswith('_'): continue
    if chapter_file.name == 'test_all.py': continue
    if chapter_file.stem in name_exclude: continue
    if chapter_file.stem in flask_exclude: continue
    print(chapter_file)
    sys.stdout.flush()
    module = importlib.import_module(chapter_file.stem)
    for test in noisy_doctest_finder.find(module):
        runner.run(test)
runner.summarize(verbose=1)

# 2. Execute a few exceptional doctests that must be run
# as __main__.
for name in name_exclude:
    print("Running", name)
    sys.stdout.flush()
    runpy.run_module(name, run_name='__main__')

# 3. Locate and run all the modules with `unittest.main()` in them.
for chapter_file in Path('.').glob('*.py'):
    if chapter_file.name == 'test_all.py': continue
    text = chapter_file.read_text(encoding='utf-8')
    if 'unittest.main' in text:
        print(chapter_file)
        sys.stdout.flush()
        runpy.run_module(chapter_file.stem, run_name='__main__')
