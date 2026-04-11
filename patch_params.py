import re

file_path = r'C:\Users\Admin\Desktop\BellyUp\BellyUp.alp'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# cookingTime delay: triangular(10, 15, 20) * 60
text = re.sub(r'(<Name><\!\[CDATA\[cookingTime\]\]>.*?</GenericParameterSubstitute>.*?<Name><\!\[CDATA\[delayTime\]\]>\s*<Value Class="CodeUnitValue">\s*<Code><\!\[CDATA\[).*?(\]\]></Code>)', 
              r'\g<1>triangular(10, 15, 20) * 60\g<2>', text, count=1, flags=re.DOTALL)

# cleanTable delay: triangular(3, 5, 8) * 60
text = re.sub(r'(<Name><\!\[CDATA\[cleanTable\]\]>.*?</GenericParameterSubstitute>.*?<Name><\!\[CDATA\[delayTime\]\]>\s*<Value Class="CodeUnitValue">\s*<Code><\!\[CDATA\[).*?(\]\]></Code>)', 
              r'\g<1>triangular(3, 5, 8) * 60\g<2>', text, count=1, flags=re.DOTALL)

# Capacity fixes
text = re.sub(r'(<Name><\!\[CDATA\[chefs\]\]>.*?</GenericParameterSubstitute>.*?<Name><\!\[CDATA\[capacity\]\]>\s*<Value Class="CodeValue">\s*<Code><\!\[CDATA\[).*?(\]\]></Code>)',
              r'\g<1>6\g<2>', text, count=1, flags=re.DOTALL)
text = re.sub(r'(<Name><\!\[CDATA\[waiters\]\]>.*?</GenericParameterSubstitute>.*?<Name><\!\[CDATA\[capacity\]\]>\s*<Value Class="CodeValue">\s*<Code><\!\[CDATA\[).*?(\]\]></Code>)',
              r'\g<1>6\g<2>', text, count=1, flags=re.DOTALL)
text = re.sub(r'(<Name><\!\[CDATA\[busboys\]\]>.*?</GenericParameterSubstitute>.*?<Name><\!\[CDATA\[capacity\]\]>\s*<Value Class="CodeValue">\s*<Code><\!\[CDATA\[).*?(\]\]></Code>)',
              r'\g<1>8\g<2>', text, count=1, flags=re.DOTALL)

# Delete cookingTime1
text = re.sub(r'<EmbeddedObject>\s*<Id>[0-9]+</Id>\s*<Name><\!\[CDATA\[cookingTime1\]\]>.*?</EmbeddedObject>', '', text, count=1, flags=re.DOTALL)


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Params updated successfully.")

