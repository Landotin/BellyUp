with open(r'c:\Users\Admin\Desktop\BellyUp\BellyUp.alp', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('<Name><![CDATA[beverageFoodHistory]]></Name>')
if start != -1:
    xml_start = text.rfind('<DataSet>', 0, start)
    xml_end = text.find('</DataSet>', start) + len('</DataSet>')
    print(text[xml_start:xml_end])
else:
    print("Not found")
