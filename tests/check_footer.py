"""Footer gate for thejonmac.com: copyright year and social link alignment.

Usage: python -I tests/check_footer.py [SITE_DIR]   (default: the repo root)
(a) static: no html file has "Copyright 2025"; index.html has "Copyright 2027 Jon Mac".
(b) layout: YOUTUBE / INSTAGRAM / TWITTER text tops and centers differ by <= 2 px at 390, 1280, 1366, 1440, 1536 and 1920 wide.
    Browser runs on GPU2 (GPU1 hook forbids local headless browsers) via D:\gpu-queue\hf_gpu2.py exec + tests/measure_footer.js.
Exit 0 = pass, 1 = fail.
"""
import json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
site = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parent
fails = []
for f in sorted(site.glob('*.html')):
    if 'Copyright 2025' in f.read_text(encoding='utf-8', errors='replace'):
        fails.append(f'{f.name}: has "Copyright 2025"')
if 'Copyright 2027 Jon Mac' not in (site / 'index.html').read_text(encoding='utf-8', errors='replace'):
    fails.append('index.html: lacks "Copyright 2027 Jon Mac"')

r = subprocess.run([sys.executable, '-I', r'D:\gpu-queue\hf_gpu2.py', 'exec', '--in', str(site / 'index.html'), '--',
                    'node', str(HERE / 'measure_footer.js'), str(site / 'index.html')],
                   capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=900)
rows = [json.loads(m) for m in re.findall(r'^MEASURE (\{.*\})$', r.stdout, re.M)]
if len(rows) != 6:
    fails.append('layout: no measurement (' + (re.findall(r'MEASURE_ERROR.*', r.stdout) or [r.stderr.strip()[-200:]])[0] + ')')
for row in rows:
    spread_t = max(row['tops']) - min(row['tops']); spread_c = max(row['centers']) - min(row['centers'])
    ok = spread_t <= 2 and spread_c <= 2
    print(f"{row['width']}px: tops {row['tops']} spread {spread_t:.1f}px, centers spread {spread_c:.1f}px -> {'ok' if ok else 'FAIL'}")
    if not ok:
        fails.append(f"layout {row['width']}px: social links off by {max(spread_t, spread_c):.1f}px")
for f in fails:
    print('FAIL', f)
print('RESULT', 'FAIL' if fails else 'PASS', site)
sys.exit(1 if fails else 0)
