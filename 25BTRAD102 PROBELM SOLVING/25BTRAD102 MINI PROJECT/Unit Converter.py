print("--- Quick Unit Converter ---")
print("1.Distance\n2.Temeperature\n3.Weight")

choice = input("What are we converting today? (1-3): ").strip()  
if choice == "1":    
    val = float(input("Enter distance: "))    
    unit = input("Is that in m, km, or mi?: ").strip().lower()     
    # Convert everything to meters first, then to target    
    meters = {"m": val, "km": val * 1000, "mi": val * 1609.34}.get(unit, val)    
    target = input("Convert to (m/km/mi): ").strip().lower()    
    if target == "km":        
        result = meters / 1000    
    elif target == "mi":        
        result = meters / 1609.34    
    else:        
        result = meters     
        print(f"{val} {unit} is roughly {round(result, 2)} {target}")  
elif choice == "2":    
    val = float(input("Enter temperature: "))    
    unit = input("Is that C or F?: ").strip().upper()     
    if unit == "C":        
        converted = (val * 9 / 5) + 32        
        print(f"{val}°C is {round(converted, 1)}°F")    
    else:        
        converted = (val - 32) * 5 / 9        
        print(f"{val}°F is {round(converted, 1)}°C")  
elif choice == "3":    
    val = float(input("Enter weight: "))    
    unit = input("Is that kg or lb?: ").strip().lower()     
    if unit == "kg": 
        print(f"{val} kg is about {round(val * 2.205, 2)} lbs") 
    else: 
        print(f"{val} lbs is about {round(val / 2.205, 2)} kg") 
else: print("Oops! Pick a valid option next time.") 

