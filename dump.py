with open(r'C:\Users\Admin\Desktop\BellyUp\BellyUp.alp', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('<Name><![CDATA[chefs]]></Name>')
if idx != -1:
    print(text[idx:idx+2000])

