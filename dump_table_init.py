with open(r'c:\Users\Admin\Desktop\BellyUp\BellyUp.alp', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('availableTenSeaters.add')
if idx != -1:
    print("Found availableTenSeaters initialization!")
    print(text[max(0, idx-1000):idx+1000])
else:
    print("availableTenSeaters.add Not found!")

