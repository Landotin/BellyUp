import re

file_path = r'C:\Users\Admin\Desktop\BellyUp\BellyUp.alp'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('<Name><![CDATA[beverageFoodHistory]]></Name>')
if start != -1:
    xml_start = text.rfind('<DataSet>', 0, start)
    xml_end = text.find('</DataSet>', start) + len('</DataSet>')
    beverage_block = text[xml_start:xml_end]
    
    new_blocks = []
    names = ['meatFoodHistory', 'sushiFoodHistory', 'candiesFoodHistory', 'iceCreamFoodHistory']
    
    id1 = re.search(r'<Id>(\d+)</Id>', beverage_block).group(1)
    id2 = re.findall(r'<Id>(\d+)</Id>', beverage_block)[1]
    
    for i, name in enumerate(names):
        block = beverage_block
        block = block.replace(f'<Id>{id1}</Id>', f'<Id>8774627192{i}1</Id>')
        block = block.replace(f'<Id>{id2}</Id>', f'<Id>8774627192{i}2</Id>')
        block = block.replace('<Name><![CDATA[beverageFoodHistory]]></Name>', f'<Name><![CDATA[{name}]]></Name>')
        block = block.replace('<Y>530</Y>', f'<Y>{560 + i*30}</Y>')
        new_blocks.append(block)
        
    combined_new_blocks = '\n'.join(new_blocks)
    
    if '<Name><![CDATA[meatFoodHistory]]></Name>' not in text:
        text = text[:xml_end] + '\n' + combined_new_blocks + text[xml_end:]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print("DataSets added successfully!")
    else:
        print("DataSets already exist.")

