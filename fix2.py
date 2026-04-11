import re

file_path = r'C:\Users\Admin\Desktop\BellyUp\BellyUp.alp'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

old_dest = '''<Parameter>
							<Name><![CDATA[destinationNode]]></Name>
							<Value Class="CodeValue">
								<Code><![CDATA[int index = activeRefills.getOrDefault(agent, 0);
switch(index) {
    case 0: return seafood;
    case 1: return dimsum;
    case 2: return all_kitchen;
    case 3: return beverage;
    case 4: return meat_kitchen;
    case 5: return plate;
    case 6: return candies;
    case 7: return candies;
    default: return seafood;
}]]></Code>
							</Value>
						</Parameter>'''

new_dest = '''<Parameter>
							<Name><![CDATA[destinationNode]]></Name>
							<Value Class="CodeValue">
								<Code><![CDATA[new com.anylogic.engine.markup.INode[]{seafood, dimsum, all_kitchen, beverage, meat_kitchen, plate, candies, candies}[activeRefills.containsKey(agent) ? activeRefills.get(agent) : 0]]]></Code>
							</Value>
						</Parameter>'''

if old_dest in text:
    text = text.replace(old_dest, new_dest)
    print("walkToBuffet updated successfully.")
else:
    print("WARNING: Could not find old_dest in file. It might have different formatting.")
    # attempt regex matching to be sure
    pattern = r'<Name><\!\[CDATA\[destinationNode\]\]>\s*<Value Class="CodeValue">\s*<Code><\!\[CDATA\[int index = activeRefills.*?\}\]\]></Code>\s*</Value>\s*</Parameter>'
    if re.search(pattern, text, re.DOTALL):
        text = re.sub(pattern, new_dest, text, count=1, flags=re.DOTALL)
        print("walkToBuffet updated via regex.")
    else:
        print("Regex also failed.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

