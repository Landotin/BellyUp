import sys

file_path = r'C:\Users\Admin\Desktop\BellyUp\BellyUp.alp'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. triggerRefill
# We need to find triggerRefill and add an onExit action.
# Let's do a regex replacement or safe python replace.

old_on_exit_trigger = '''<Parameter>
							<Name><![CDATA[onExit]]></Name>
						</Parameter>'''

# Let's verify triggerRefill is the only one we replace by finding it specifically:
import re
match = re.search(r'<Name><\!\[CDATA\[triggerRefill\]\]>.*?</EmbeddedObject>', text, re.DOTALL)
if match:
    obj = match.group(0)
    new_obj = obj.replace('<Parameter>\n\t\t\t\t\t\t\t<Name><![CDATA[onExit]]></Name>\n\t\t\t\t\t\t</Parameter>', 
                          '<Parameter>\n\t\t\t\t\t\t\t<Name><![CDATA[onExit]]></Name>\n\t\t\t\t\t\t\t<Value Class="CodeValue">\n\t\t\t\t\t\t\t\t<Code><![CDATA[activeRefills.put(agent, pendingRefillStations.poll());]]></Code>\n\t\t\t\t\t\t\t</Value>\n\t\t\t\t\t\t</Parameter>')
    text = text.replace(obj, new_obj)

# 2. walkToBuffet
old_dest = '''<Parameter>
							<Name><![CDATA[destinationNode]]></Name>
							<Value Class="CodeValue">
								<Code><![CDATA[seafood]]></Code>
							</Value>
						</Parameter>'''

new_dest = '''<Parameter>
							<Name><![CDATA[destinationNode]]></Name>
							<Value Class="CodeValue">
								<Code><![CDATA[int index = activeRefills.getOrDefault(agent, 0);
switch(index) {
    case 0: return seafood;
    case 1: return dimsum;
    case 2: return all_kitchen;
    case 3: return beverage_station;
    case 4: return meat_kitchen;
    case 5: return plate;
    case 6: return candies;
    case 7: return candies;
    default: return seafood;
}]]></Code>
							</Value>
						</Parameter>'''

text = text.replace(old_dest, new_dest)

# 3. refillTray onExit
old_refill = '''<Code><![CDATA[if (seaFoodRefilling) { seaFoodLevel = seaFoodMax; seaFoodRefilling = false; }
else if (dimsumRefilling) { dimsumFoodLevel = dimsumFoodMax; dimsumRefilling = false; }
else if (buffetRefilling) { buffetFoodLevel = buffetFoodMax; buffetRefilling = false; }
else if (beverageRefilling) { beverageFoodLevel = beverageFoodMax; beverageRefilling = false; }
]]></Code>'''

new_refill = '''<Code><![CDATA[int idx = activeRefills.getOrDefault(agent, 0);
activeRefills.remove(agent);
switch(idx) {
    case 0: seaFoodLevel = seaFoodMax; seaFoodRefilling = false; break;
    case 1: dimsumFoodLevel = dimsumFoodMax; dimsumRefilling = false; break;
    case 2: buffetFoodLevel = buffetFoodMax; buffetRefilling = false; break;
    case 3: beverageFoodLevel = beverageFoodMax; beverageRefilling = false; break;
    case 4: meatFoodLevel = meatFoodMax; meatRefilling = false; break;
    case 5: sushiFoodLevel = sushiFoodMax; sushiRefilling = false; break;
    case 6: candiesFoodLevel = candiesFoodMax; candiesRefilling = false; break;
    case 7: iceCreamFoodLevel = iceCreamFoodMax; iceCreamRefilling = false; break;
}]]></Code>'''

text = text.replace(old_refill, new_refill)

# 4. foodSelectionWaiting onAtExit
old_on_at_exit = '''<Code><![CDATA[double r = uniform(0, 1);
int firstChoice;
if (r < 0.40)      firstChoice = 0;  // Seafood: 40%
else if (r < 0.65) firstChoice = 1;  // Dimsum: 25%
else if (r < 0.85) firstChoice = 2;  // Buffet: 20%
else               firstChoice = 3;  // Beverage: 15%

double[] levels = { seaFoodLevel, dimsumFoodLevel, 
                    buffetFoodLevel, beverageFoodLevel };

if (levels[firstChoice] > 0) {
    ped.foodChoice = firstChoice;
} else {
    // Build shuffled list of alternatives
    java.util.ArrayList<Integer> alternatives = new java.util.ArrayList<>();
    for (int i = 0; i < 4; i++) {
        if (i != firstChoice) alternatives.add(i);
    }
    java.util.Collections.shuffle(alternatives, 
        new java.util.Random((long)(time() * 1000)));
    
    boolean found = false;
    for (int alt : alternatives) {
        if (levels[alt] > 0) {
            ped.foodChoice = alt;
            totalStationSkips++;
            found = true;
            break;
        }
    }
    if (!found) ped.foodChoice = firstChoice; // all empty
}]]></Code>'''

new_on_at_exit = '''<Code><![CDATA[totalFoodSelectionAttempts++;

double r = uniform(0, 1);
int firstChoice;
if      (r < 0.20) firstChoice = 0;  // Seafood: 20%
else if (r < 0.40) firstChoice = 1;  // Dimsum: 20%
else if (r < 0.55) firstChoice = 2;  // Buffet: 15%
else if (r < 0.67) firstChoice = 3;  // Beverage: 12%
else if (r < 0.82) firstChoice = 4;  // Meat: 15%
else if (r < 0.90) firstChoice = 5;  // Sushi: 8%
else if (r < 0.95) firstChoice = 6;  // Candies: 5%
else               firstChoice = 7;  // Ice Cream: 5%

double[] levels = { seaFoodLevel, dimsumFoodLevel, 
                    buffetFoodLevel, beverageFoodLevel,
                    meatFoodLevel, sushiFoodLevel, 
                    candiesFoodLevel, iceCreamFoodLevel };

if (levels[firstChoice] > 0) {
    ped.foodChoice = firstChoice;
} else {
    // Build shuffled list of alternatives
    java.util.ArrayList<Integer> alternatives = new java.util.ArrayList<>();
    for (int i = 0; i < 8; i++) {
        if (i != firstChoice) alternatives.add(i);
    }
    java.util.Collections.shuffle(alternatives, 
        new java.util.Random((long)(time() * 1000)));
    
    boolean found = false;
    for (int alt : alternatives) {
        if (levels[alt] > 0) {
            ped.foodChoice = alt;
            totalStationSkips++;
            found = true;
            break;
        }
    }
    if (!found) ped.foodChoice = firstChoice; // all empty
}]]></Code>'''

text = text.replace(old_on_at_exit, new_on_at_exit)

# 5. foodSelectionWaiting onExit
old_on_exit = '''<Code><![CDATA[// Deduct food from chosen station
if (ped.foodChoice == 0) 
    seaFoodLevel = Math.max(0, (int)seaFoodLevel - 1);
else if (ped.foodChoice == 1) 
    dimsumFoodLevel = Math.max(0, dimsumFoodLevel - 1);
else if (ped.foodChoice == 2) 
    buffetFoodLevel = Math.max(0, buffetFoodLevel - 1);
else if (ped.foodChoice == 3) 
    beverageFoodLevel = Math.max(0, beverageFoodLevel - 1);

// Count depletion only at the moment of transition to zero
if (ped.foodChoice == 0 && seaFoodLevel == 0) seaFoodDepletionCount++;
if (ped.foodChoice == 1 && dimsumFoodLevel == 0) dimsumDepletionCount++;
if (ped.foodChoice == 2 && buffetFoodLevel == 0) buffetDepletionCount++;
if (ped.foodChoice == 3 && beverageFoodLevel == 0) beverageDepletionCount++;

// Independent refill triggers at 30% threshold
if (seaFoodLevel <= (seaFoodMax * 0.30) && !seaFoodRefilling) {
    seaFoodRefilling = true;
    refillStationIndex = 0;
    triggerRefill.inject(1);
}
if (dimsumFoodLevel <= (dimsumFoodMax * 0.30) && !dimsumRefilling) {
    dimsumRefilling = true;
    refillStationIndex = 1;
    triggerRefill.inject(1);
}
if (buffetFoodLevel <= (buffetFoodMax * 0.30) && !buffetRefilling) {
    buffetRefilling = true;
    refillStationIndex = 2;
    triggerRefill.inject(1);
}
if (beverageFoodLevel <= (beverageFoodMax * 0.30) && !beverageRefilling) {
    beverageRefilling = true;
    refillStationIndex = 3;
    triggerRefill.inject(1);
}]]></Code>'''

new_on_exit = '''<Code><![CDATA[// Deduct food from chosen station
if (ped.foodChoice == 0) seaFoodLevel = Math.max(0, (int)seaFoodLevel - 1);
else if (ped.foodChoice == 1) dimsumFoodLevel = Math.max(0, dimsumFoodLevel - 1);
else if (ped.foodChoice == 2) buffetFoodLevel = Math.max(0, buffetFoodLevel - 1);
else if (ped.foodChoice == 3) beverageFoodLevel = Math.max(0, beverageFoodLevel - 1);
else if (ped.foodChoice == 4) meatFoodLevel = Math.max(0, meatFoodLevel - 1);
else if (ped.foodChoice == 5) sushiFoodLevel = Math.max(0, sushiFoodLevel - 1);
else if (ped.foodChoice == 6) candiesFoodLevel = Math.max(0, candiesFoodLevel - 1);
else if (ped.foodChoice == 7) iceCreamFoodLevel = Math.max(0, iceCreamFoodLevel - 1);

// Count depletion only at the moment of transition to zero
if (ped.foodChoice == 0 && seaFoodLevel == 0) seaFoodDepletionCount++;
if (ped.foodChoice == 1 && dimsumFoodLevel == 0) dimsumDepletionCount++;
if (ped.foodChoice == 2 && buffetFoodLevel == 0) buffetDepletionCount++;
if (ped.foodChoice == 3 && beverageFoodLevel == 0) beverageDepletionCount++;
if (ped.foodChoice == 4 && meatFoodLevel == 0) meatDepletionCount++;
if (ped.foodChoice == 5 && sushiFoodLevel == 0) sushiDepletionCount++;
if (ped.foodChoice == 6 && candiesFoodLevel == 0) candiesDepletionCount++;
if (ped.foodChoice == 7 && iceCreamFoodLevel == 0) iceCreamDepletionCount++;

// Independent refill triggers at 30% threshold
if (seaFoodLevel <= (seaFoodMax * 0.30) && !seaFoodRefilling) { seaFoodRefilling = true; pendingRefillStations.add(0); triggerRefill.inject(1); }
if (dimsumFoodLevel <= (dimsumFoodMax * 0.30) && !dimsumRefilling) { dimsumRefilling = true; pendingRefillStations.add(1); triggerRefill.inject(1); }
if (buffetFoodLevel <= (buffetFoodMax * 0.30) && !buffetRefilling) { buffetRefilling = true; pendingRefillStations.add(2); triggerRefill.inject(1); }
if (beverageFoodLevel <= (beverageFoodMax * 0.30) && !beverageRefilling) { beverageRefilling = true; pendingRefillStations.add(3); triggerRefill.inject(1); }
if (meatFoodLevel <= (meatFoodMax * 0.30) && !meatRefilling) { meatRefilling = true; pendingRefillStations.add(4); triggerRefill.inject(1); }
if (sushiFoodLevel <= (sushiFoodMax * 0.30) && !sushiRefilling) { sushiRefilling = true; pendingRefillStations.add(5); triggerRefill.inject(1); }
if (candiesFoodLevel <= (candiesFoodMax * 0.30) && !candiesRefilling) { candiesRefilling = true; pendingRefillStations.add(6); triggerRefill.inject(1); }
if (iceCreamFoodLevel <= (iceCreamFoodMax * 0.30) && !iceCreamRefilling) { iceCreamRefilling = true; pendingRefillStations.add(7); triggerRefill.inject(1); }
]]></Code>'''

text = text.replace(old_on_exit, new_on_exit)


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Logic parts injected.")
