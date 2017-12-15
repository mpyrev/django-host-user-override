#!/bin/bash
pandoc --from=markdown --to=rst --output=README.rst README.md
python setup.py bdist
python setup.py bdist_wheel --universal
