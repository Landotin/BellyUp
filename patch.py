import uuid
import re

file_path = r'C:\Users\Admin\Desktop\BellyUp\BellyUp.alp'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update existing max capacities
text = text.replace('<Code><![CDATA[180]]></Code>', '<Code><![CDATA[150]]></Code>', 1) # dimsumFoodMax (approx, will use safer regex)
