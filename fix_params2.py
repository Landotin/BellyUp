import re

file_path = r'C:\Users\Admin\Desktop\BellyUp\BellyUp.alp'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

def update_val(obj_name, target_prop, old_val, new_val):
    global text
    idx = text.find(f'<Name><![CDATA[{obj_name}]]></Name>')
    if idx == -1: return False
    
    # Extract the block of next 3000 chars
    block = text[idx:idx+3000]
    
    # look for the target_prop
    prop_idx = block.find(f'<Name><![CDATA[{target_prop}]]></Name>')
    if prop_idx == -1: return False
    
    # replace the exact code inside that prop area
    prop_block = block[prop_idx:prop_idx+200]
    new_prop_block = prop_block.replace(f'<Code><![CDATA[{old_val}]]></Code>', f'<Code><![CDATA[{new_val}]]></Code>')
    
    if prop_block == new_prop_block: return False
    
    new_block = block[:prop_idx] + new_prop_block + block[prop_idx+200:]
    text = text[:idx] + new_block + text[idx+3000:]
    return True

r1 = update_val('chefs', 'capacity', '4', '6')
r2 = update_val('waiters', 'capacity', '4', '6')
# Busboys was already 8? Let's check codegen: self.capacity = 8;
r3 = update_val('busboys', 'capacity', '4', '8') # might fail if already 8
if not r3:
    r3b = update_val('busboys', 'capacity', '8', '8')

r4 = update_val('cookingTime', 'delayTime', 'triangular(8, 12, 15) * 60', 'triangular(10, 15, 20) * 60')
r5 = update_val('cleanTable', 'delayTime', 'triangular(2, 3, 5) * 60', 'triangular(3, 5, 8) * 60')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print(f"Updates: Chefs={r1}, Waiters={r2}, Busboys={r3}, cookingTime={r4}, cleanTable={r5}")
