import re
import time

def scan_inline():
    skill_pattern = re.compile(r'/[a-z][a-z0-9]*(-[a-z0-9]+)*')
    list(skill_pattern.finditer("some string /summarize /gaia-curate"))

skill_pattern_global = re.compile(r'/[a-z][a-z0-9]*(-[a-z0-9]+)*')
def scan_global():
    list(skill_pattern_global.finditer("some string /summarize /gaia-curate"))

start = time.time()
for _ in range(100000):
    scan_inline()
print(f"Inline: {time.time() - start}")

start = time.time()
for _ in range(100000):
    scan_global()
print(f"Global: {time.time() - start}")
