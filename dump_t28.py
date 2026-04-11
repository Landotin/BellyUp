with open(r'c:\Users\Admin\Desktop\BellyUp\BellyUp.alp', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('table28')
if idx != -1:
    print(text[max(0, idx-200):idx+500])

