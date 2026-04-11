import re

file_path = r'C:\Users\Admin\Desktop\BellyUp\BellyUp.alp'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('<Name><![CDATA[beverageFoodHistory]]></Name>')
if start != -1:
    xml_start = text.rfind('<DataSet>', 0, start)
    xml_end = text.find('</DataSet>', start) + len('</DataSet>')
    beverage_block = text[xml_start:xml_end]
    
    # We will clone and modify beverage_block
    new_blocks = []
    names = ['meatFoodHistory', 'sushiFoodHistory', 'candiesFoodHistory', 'iceCreamFoodHistory']
    
    for i, name in enumerate(names):
        block = beverage_block
        # Replace ID
        block = re.sub(r'<Id>\d+</Id>', f'<Id>18846271923{i}5</Id>', block)
        # Replace Recurrence ID
        block = re.sub(r'<Id>\d+</Id>', f'<Id>18846271923{i}3</Id>', block, count=1) 
        # Actually the above hits the first ID again if we use sub, let's fix
        block = re.sub(r'<Id>\d+</Id>', lambda m, c={'cnt':0}: f'<Id>18846271923{i}{[5,3][c["cnt"]]}tmp</Id>' if c.update({'cnt': c['cnt']+1}) or True else '', block)
        block = block.replace('tmp', '')
        
        # Replace Name
        block = block.replace('<Name><![CDATA[beverageFoodHistory]]></Name>', f'<Name><![CDATA[{name}]]></Name>')
        # Replace Y
        block = re.sub(r'<Y>530</Y>', f'<Y>{560 + i*30}</Y>', block)
        
        new_blocks.append(block)
        
    combined_new_blocks = '\n'.join(new_blocks)
    
    if 'meatFoodHistory' not in text:
        text = text[:xml_end] + '\n' + combined_new_blocks + text[xml_end:]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print("DataSets added successfully!")
    else:
        print("DataSets already exist.")

