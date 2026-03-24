import re
import sys

def patch_alp(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix seize4 onSeizeUnit
    old_seize = "agent.assignedTable = availableFourSeaters.remove(0);"
    new_seize = "agent.assignedTable = availableFourSeaters.remove(uniform_discr(0, availableFourSeaters.size() - 1));"
    
    if old_seize in content:
        content = content.replace(old_seize, new_seize)
        print("Successfully patched seize4 onSeizeUnit.")
    else:
        print("WARNING: Could not find old seize4 onSeizeUnit code.")

    # 2. Fix table4seater parameters. We need to find the AreaNodeDescriptor inside <RectangleNode> elements
    # where the Name starts with "table4seater" and remove the access restricted parameters.
    # It's safer to just replace the whole `<Value Class="CodeValue">\n<Code><![CDATA[true]]></Code>\n</Value>` 
    # and capacity `0` but ONLY within the AreaNodeDescriptor.
    
    # Actually, the simplest approach is to remove the specific <Value> tags for those parameters across all AreaNodeDescriptors 
    # because they were uniformly applied by the previous agent patch for Bug #1.
    
    # 2a. accessRestricted
    p_access = re.compile(r'(<Parameter>\s*<Name><!\[CDATA\[accessRestricted\]\]></Name>\s*)<Value Class="CodeValue">\s*<Code><!\[CDATA\[true\]\]></Code>\s*</Value>(\s*</Parameter>)', re.MULTILINE)
    content, count_access = p_access.subn(r'\1\2', content)
    print(f"Removed accessRestricted=true from {count_access} places.")

    # 2b. capacity
    p_cap = re.compile(r'(<Parameter>\s*<Name><!\[CDATA\[capacity\]\]></Name>\s*)<Value Class="CodeValue">\s*<Code><!\[CDATA\[0\]\]></Code>\s*</Value>(\s*</Parameter>)', re.MULTILINE)
    content, count_cap = p_cap.subn(r'\1\2', content)
    print(f"Removed capacity=0 from {count_cap} places.")

    # 2c. avoidedIfClosed
    p_avoid = re.compile(r'(<Parameter>\s*<Name><!\[CDATA\[avoidedIfClosed\]\]></Name>\s*)<Value Class="CodeValue">\s*<Code><!\[CDATA\[true\]\]></Code>\s*</Value>(\s*</Parameter>)', re.MULTILINE)
    content, count_avoid = p_avoid.subn(r'\1\2', content)
    print(f"Removed avoidedIfClosed=true from {count_avoid} places.")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
if __name__ == '__main__':
    alp_file = r'c:\Users\Admin\Desktop\BellyUp\BellyUp.alp'
    patch_alp(alp_file)
