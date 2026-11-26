# Builds husk.html (the single-file offline copy) from src/husk-source.html. Run: python3 build/build_standalone.py
import re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(os.path.join(ROOT, 'src', 'husk-source.html'), encoding='utf-8').read()

def rep(old, new):
    global s
    assert s.count(old) == 1, old[:60]
    s = s.replace(old, new)

rep('var LOCAL_DOWNLOADS = false;', 'var LOCAL_DOWNLOADS = true;')
rep('<title>Husk</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n', '<title>Husk</title>\n')
rep('* { box-sizing: border-box; }', '* { box-sizing: border-box; }\nbody { margin: 0; }')
csp = "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src blob: data:; media-src blob:; connect-src 'none'; object-src 'none'; frame-src 'none'; worker-src 'none'; form-action 'none'; base-uri 'none'"
FAV = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Cpath d='M20 4H38L60 26V44C60 53.4 53.4 60 44 60H20C10.6 60 4 53.4 4 44V20C4 10.6 10.6 4 20 4Z' fill='%230E7A5A'/%3E%3Cpath d='M38 4V18C38 22.4 41.6 26 46 26H60Z' fill='%237FD9B6'/%3E%3Ccircle cx='22' cy='26' r='5' fill='%23fff'/%3E%3Cpath d='M12 50L26 33L35 43L41 37L52 50Z' fill='%23fff'/%3E%3C/svg%3E"
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta http-equiv="Content-Security-Policy" content="' + csp + '">\n'
        '<meta name="referrer" content="no-referrer">\n'
        '<link rel="icon" href="' + FAV + '">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n')
s = head + s.replace('<div class="wrap">', '</head>\n<body>\n<div class="wrap">', 1) + '\n</body>\n</html>\n'
open(os.path.join(ROOT, 'husk.html'), 'w', encoding='utf-8').write(s)
blocks = re.findall(r'<script>([\s\S]*?)</script>', s)
for bad in ['googleapis', 'gstatic', 'cdnjs', 'jsdelivr', 'unpkg', 'fetch(', 'XMLHttpRequest', 'WebSocket', 'sendBeacon', 'src="http']:
    print(f'{bad:16}', s.count(bad))
print('size', len(s))
