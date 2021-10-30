#!/bin/bash
npm test
browserify ktc/static/js/js/* -o ktc/static/js/bundle.js
coverage run -m pytest test/*.py -vv -x
coverage xml
codecov -F python -f coverage.xml -t d2d0d3db-98bd-4add-8ab8-782003116ae9
mypy ktc/*.py
python .pylintbadge ktc/
rm ktc.svg
mv ktc/.svg ktc.svg