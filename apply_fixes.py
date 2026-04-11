import re

file_path = r'C:\Users\Admin\Desktop\BellyUp\BellyUp.alp'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update executeTableAssignment
idx_func = text.find('<Name><![CDATA[executeTableAssignment]]></Name>')
if idx_func != -1:
    body_idx = text.find('<Body><![CDATA[', idx_func)
    end_body = text.find(']]></Body>', body_idx)
    body = text[body_idx:end_body]
    if 'occupiedSeats += leader.groupSize;' not in body:
        new_body = body.replace(' leader.groupSize = 1;\n}', ' leader.groupSize = 1;\n}\n\noccupiedSeats += leader.groupSize;')
        text = text[:body_idx] + new_body + text[end_body:]

# 2. Update pedSink1_onEnter
idx_sink = text.find('if (ped.assignedTable != null) {')
if idx_sink != -1:
    if 'occupiedSeats -= 1;' not in text[idx_sink:idx_sink+300]:
        new_sink = 'if (ped.assignedTable != null) {\n    occupiedSeats -= 1;'
        text = text.replace('if (ped.assignedTable != null) {', new_sink, 1)

# 3. Update event action
idx_event = text.find('beverageFoodHistory.add(time(), beverageFoodLevel);')
if idx_event != -1:
    if 'meatFoodHistory.add' not in text[idx_event:idx_event+200]:
        new_history = ('beverageFoodHistory.add(time(), beverageFoodLevel);\n'
                       'meatFoodHistory.add(time(), meatFoodLevel);\n'
                       'sushiFoodHistory.add(time(), sushiFoodLevel);\n'
                       'candiesFoodHistory.add(time(), candiesFoodLevel);\n'
                       'iceCreamFoodHistory.add(time(), iceCreamFoodLevel);')
        text = text.replace('beverageFoodHistory.add(time(), beverageFoodLevel);', new_history)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updates applied.")
