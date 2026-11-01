"""
USN: 25BTRAD102
MINI PROJECT 1: QUICK UNIT CONVERTER

Convert distance (m, km, mi), temperature (C, F), and weight (kg, lb).
The program validates units and numeric input and displays clear results.
"""

DISTANCE_TO_METERS = {"m": 1.0, "km": 1000.0, "mi": 1609.344}
WEIGHT_TO_KG = {"kg": 1.0, "lb": 0.45359237}


def read_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def convert_distance():
    value = read_number("Enter distance: ")
    source = input("Convert from (m/km/mi): ").strip().lower()
    target = input("Convert to (m/km/mi): ").strip().lower()
    if source not in DISTANCE_TO_METERS or target not in DISTANCE_TO_METERS:
        print("Invalid distance unit. Use m, km, or mi.")
        return
    meters = value * DISTANCE_TO_METERS[source]
    result = meters / DISTANCE_TO_METERS[target]
    print(f"{value:g} {source} = {result:.4f} {target}")


def convert_temperature():
    value = read_number("Enter temperature: ")
    source = input("Convert from (C/F): ").strip().upper()
    target = input("Convert to (C/F): ").strip().upper()
    if source not in {"C", "F"} or target not in {"C", "F"}:
        print("Invalid temperature unit. Use C or F.")
        return
    celsius_value = value if source == "C" else (value - 32) * 5 / 9
    if celsius_value < -273.15:
        print("Temperature cannot be below absolute zero (-273.15 C).")
        return
    if source == target:
        result = value
    elif source == "C":
        result = (value * 9 / 5) + 32
    else:
        result = (value - 32) * 5 / 9
    print(f"{value:g} degrees {source} = {result:.2f} degrees {target}")


def convert_weight():
    value = read_number("Enter weight: ")
    source = input("Convert from (kg/lb): ").strip().lower()
    target = input("Convert to (kg/lb): ").strip().lower()
    if source not in WEIGHT_TO_KG or target not in WEIGHT_TO_KG:
        print("Invalid weight unit. Use kg or lb.")
        return
    if value < 0:
        print("Weight cannot be negative.")
        return
    kilograms = value * WEIGHT_TO_KG[source]
    result = kilograms / WEIGHT_TO_KG[target]
    print(f"{value:g} {source} = {result:.4f} {target}")


def main():
    while True:
        print("\n--- QUICK UNIT CONVERTER ---")
        print("1. Distance (m, km, mi)")
        print("2. Temperature (C, F)")
        print("3. Weight (kg, lb)")
        print("4. Exit")
        choice = input("What are we converting today? (1-4): ").strip()
        if choice == "1":
            convert_distance()
        elif choice == "2":
            convert_temperature()
        elif choice == "3":
            convert_weight()
        elif choice == "4":
            print("Exiting unit converter.")
            break
        else:
            print("Invalid option. Pick a number from 1 to 4.")


if __name__ == "__main__":
    main()
