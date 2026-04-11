with open(r'c:\Users\Admin\Desktop\BellyUp\BellyUp.alp', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('table10seaters2')
if idx != -1:
    print("table10seaters2 FOUND in text!")
else:
    print("table10seaters2 NOT found!")

import re
m = re.search(r'<Name><\!\[CDATA\[table10seaters2\]\]></Name>', text)
if m:
    print("Found as an exact node Name!")
