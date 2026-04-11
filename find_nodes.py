import re
with open(r'C:\Users\Admin\Desktop\BellyUp\BellyUp.alp', 'r', encoding='utf-8') as f:
    text = f.read()

nodes = re.findall(r'<Name><\!\[CDATA\[(.*?)\]\]></Name>\s*<X>.*?</X><Y>.*?</Y>.*?<ClassName><\!\[CDATA\[RectangularNode\]\]></ClassName>', text, re.DOTALL)
print("Rectangular Nodes:", nodes)
