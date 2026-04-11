with open(r'c:\Users\Admin\Desktop\BellyUp\BellyUp.alp', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('table28')
if idx != -1:
    start = text.rfind('<RectangularNode>', 0, idx)
    end = text.find('</RectangularNode>', idx)
    print("Found table28 XML definition:")
    print(text[start:end+20])
else:
    print("table28 Not found!")

