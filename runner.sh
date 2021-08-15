npm test
browserify ktc/static/js/main.js -o ktc/static/js/bundle.js 
coverage run -m pytest test/*.py
mypy ktc