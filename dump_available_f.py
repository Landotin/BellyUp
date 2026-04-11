with open(r'c:\Users\Admin\Desktop\BellyUp\BellyUp.alp', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('<Name><![CDATA[availableFourSeaters]]>')
if idx != -1:
    print(text[idx-50:idx+3500])
else:
    print("Not found")

