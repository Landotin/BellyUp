import re

file_path = r'C:\Users\Admin\Desktop\BellyUp\BellyUp.alp'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the CDATA literal escaping bug
text = text.replace('java.util.ArrayDeque&lt;Integer&gt;', 'java.util.ArrayDeque<Integer>')
text = text.replace('new java.util.ArrayDeque&lt;&gt;()', 'new java.util.ArrayDeque<Integer>()')
text = text.replace('java.util.Map&lt;Agent, Integer&gt;', 'java.util.Map<Agent, Integer>')
text = text.replace('new java.util.HashMap&lt;&gt;()', 'new java.util.HashMap<Agent, Integer>()')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Escaping fixed.")
