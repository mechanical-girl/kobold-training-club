#!/bin/bash
npm test
cd ktc/static/js
browserify element_lister.js encounter-manager.js improved-initiative-service.js jquery.js main.js party-manager.js sources-manager.js updater-button.js -v -o bundle.js
cd ../../../
coverage run -m pytest test/*.py -vv -x
coverage xml
codecov -F python -f coverage.xml -t d2d0d3db-98bd-4add-8ab8-782003116ae9
mypy ktc/*.py
python .pylintbadge ktc/
rm ktc.svg
mv ktc/.svg ktc.svg