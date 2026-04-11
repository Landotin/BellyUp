with open(r'c:\Users\Admin\Desktop\BellyUp\BellyUp.alp', 'r', encoding='utf-8') as f:
    text = f.read()

print("--- executeTableAssignment ---")
idx1 = text.find('void executeTableAssignment')
print(text[idx1-200:idx1+800])

print("\n--- pedSink1 ---")
idx2 = text.find('if (ped.assignedTable != null) {')
print(text[idx2-200:idx2+600])

print("\n--- event ---")
idx3 = text.find('seaFoodHistory.add(time(), seaFoodLevel);')
print(text[idx3-200:idx3+600])

