import re

file_path = r'C:\Users\Admin\Desktop\BellyUp\BellyUp.alp'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix HTML Entities inside CDATA blocks!
text = text.replace('java.util.ArrayDeque&lt;Integer&gt;', 'java.util.ArrayDeque<Integer>')
text = text.replace('new java.util.ArrayDeque&lt;&gt;()', 'new java.util.ArrayDeque<>()')
text = text.replace('java.util.Map&lt;Agent, Integer&gt;', 'java.util.Map<Agent, Integer>')
text = text.replace('new java.util.HashMap&lt;&gt;()', 'new java.util.HashMap<>()')

# Fix Node name
text = text.replace('return beverage_station;', 'return beverage;')

# Wait, everage_station might have been saved as everage_station; inside the XML. Let's make sure.
text = text.replace('beverage_station', 'beverage')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixes applied.")
