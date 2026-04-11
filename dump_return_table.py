with open(r'c:\Users\Admin\Desktop\BellyUp\BellyUp.alp', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('returnTableSink')
if idx != -1:
    print(text[idx-500:idx+2500])
