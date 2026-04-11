with open(r'c:\Users\Admin\Desktop\BellyUp\BellyUp.alp', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('<TimePlot>')
if idx != -1:
    end = text.find('</TimePlot>', idx)
    print("TimePlot block length:", end - idx)
    print(text[idx:idx+1500])

idxbar = text.find('<BarChart>')
if idxbar != -1:
    endbar = text.find('</BarChart>', idxbar)
    print("BarChart block length:", endbar - idxbar)
