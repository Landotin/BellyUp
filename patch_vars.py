import uuid

def generate_var(name, vtype, init_val, ptype="PlainVariable"):
    var_id = str(uuid.uuid4().int)[0:13]
    return f'''
				<Variable Class="{ptype}">
					<Id>{var_id}</Id>
					<Name><![CDATA[{name}]]></Name>
					<X>-115</X><Y>600</Y>
					<Label><X>10</X><Y>0</Y></Label>
					<PublicFlag>false</PublicFlag>
					<PresentationFlag>true</PresentationFlag>
					<ShowLabel>true</ShowLabel>
					<Properties SaveInSnapshot="true" Constant="false" AccessType="public" StaticVariable="false">
						<Type><![CDATA[{vtype}]]></Type>        
						<InitialValue Class="CodeValue">
							<Code><![CDATA[{init_val}]]></Code>
						</InitialValue>
					</Properties>
				</Variable>'''

vars = [
    # Maxes
    ('meatFoodMax', 'int', '150'),
    ('sushiFoodMax', 'int', '120'),
    ('candiesFoodMax', 'int', '100'),
    ('iceCreamFoodMax', 'int', '100'),
    # Levels
    ('meatFoodLevel', 'int', '150'),
    ('sushiFoodLevel', 'int', '120'),
    ('candiesFoodLevel', 'int', '100'),
    ('iceCreamFoodLevel', 'int', '100'),
    # Refilling flags
    ('meatRefilling', 'boolean', 'false'),
    ('sushiRefilling', 'boolean', 'false'),
    ('candiesRefilling', 'boolean', 'false'),
    ('iceCreamRefilling', 'boolean', 'false'),
    # Depletion
    ('meatDepletionCount', 'int', '0'),
    ('sushiDepletionCount', 'int', '0'),
    ('candiesDepletionCount', 'int', '0'),
    ('iceCreamDepletionCount', 'int', '0'),
    # Extra config
    ('totalFoodSelectionAttempts', 'int', '0'),
    ('pendingRefillStations', 'java.util.ArrayDeque&lt;Integer&gt;', 'new java.util.ArrayDeque&lt;&gt;()'),
    ('activeRefills', 'java.util.Map&lt;Agent, Integer&gt;', 'new java.util.HashMap&lt;&gt;()')
]

xml_inject = "".join([generate_var(*v) for v in vars])

file_path = r'C:\Users\Admin\Desktop\BellyUp\BellyUp.alp'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix max variables
text = text.replace('<Code><![CDATA[180]]></Code>', '<Code><![CDATA[150]]></Code>', 1) # dimsum
text = text.replace('<Code><![CDATA[180]]></Code>', '<Code><![CDATA[200]]></Code>', 1) # buffet
text = text.replace('<Code><![CDATA[220]]></Code>', '<Code><![CDATA[150]]></Code>', 1) # beverage

# Inject to variables
text = text.replace('			</Variables>', xml_inject + '\n			</Variables>', 1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Variables injected.")
