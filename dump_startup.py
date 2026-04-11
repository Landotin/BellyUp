with open(r'c:\Users\Admin\Desktop\BellyUp\BellyUp.alp', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('<StartupCode>')
if idx != -1:
    print("Found StartupCode:")
    print(text[idx:idx+1500])
else:
    print("StartupCode Not found!")

