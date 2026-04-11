with open(r'c:\Users\Admin\Desktop\BellyUp\BellyUp.alp', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.finditer(r'availableFourSeaters\.add', text)
for m in matches:
    start = max(0, m.start()-100)
    end = min(len(text), m.end()+100)
    print("Match context:\n" + text[start:end])

