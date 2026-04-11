import re

file_path = r'C:\Users\Admin\Desktop\BellyUp\BellyUp.alp'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Helper to find and replace
def update_capacity(pool_name, new_val):
    global text
    # The pool object starts with <Name><![CDATA[chefs]]></Name>
    # then somewhere there is <Name><![CDATA[capacity]]></Name>
    
    # We can split the file by block
    # or use a very localized regex
    pattern = r'(<Name><\!\[CDATA\[' + pool_name + r'\]\]>.*?</GenericParameterSubstitute>.*?<Name><\!\[CDATA\[capacity\]\]>\s*<Value Class="CodeValue">\s*<Code><\!\[CDATA\[).*?(\]\]></Code>)'
    if re.search(pattern, text, re.DOTALL):
        text = re.sub(pattern, r'\g<1>' + str(new_val) + r'\g<2>', text, count=1, flags=re.DOTALL)
        print(f"Updated capacity for {pool_name} to {new_val}.")
    else:
        # maybe it's missing GenericParameterSubstitute
        pattern2 = r'(<Name><\!\[CDATA\[' + pool_name + r'\]\]>.*?<Name><\!\[CDATA\[capacity\]\]>\s*<Value Class="CodeValue">\s*<Code><\!\[CDATA\[).*?(\]\]></Code>)'
        if re.search(pattern2, text, re.DOTALL):
            text = re.sub(pattern2, r'\g<1>' + str(new_val) + r'\g<2>', text, count=1, flags=re.DOTALL)
            print(f"Updated capacity for {pool_name} (fallback) to {new_val}.")
        else:
            print(f"FAILED to find capacity block for {pool_name}")

def update_delay(delay_name, new_val):
    global text
    pattern = r'(<Name><\!\[CDATA\[' + delay_name + r'\]\]>.*?<Name><\!\[CDATA\[delayTime\]\]>\s*<Value Class=".*?">\s*<Code><\!\[CDATA\[).*?(\]\]></Code>)'
    if re.search(pattern, text, re.DOTALL):
        text = re.sub(pattern, r'\g<1>' + str(new_val) + r'\g<2>', text, count=1, flags=re.DOTALL)
        print(f"Updated delay for {delay_name} to {new_val}.")
    else:
        print(f"FAILED to find delay block for {delay_name}")

update_capacity('chefs', 6)
update_capacity('waiters', 6)
update_capacity('busboys', 8)

update_delay('cookingTime', 'triangular(10, 15, 20) * 60')
update_delay('cleanTable', 'triangular(3, 5, 8) * 60')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

