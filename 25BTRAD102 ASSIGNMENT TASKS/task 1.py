#Task 1
s=input("Enter Name,Department, College\n")
print("\n")
#Task 2
for i in range(3):
    print("*" * 7, end="\n" if i<2 else "")
print("\n")
#Task 3
print("Python is Easy")
print("\n")
#Task 4
for i in range(1,6):
    for j in range(1, i+1):
        print(j, end="")
    print()
print("\n")
#Task 5
print("\n")
print("Computer\nScience\nEngineering")
print("\n")
#Task 6
print("Sathwik\t19\tBLR")
print("\n")
#Task 7
# Calculate the approximate escape velocity of Earth in km/s
gravity = 9.8 
radius_meters = 6371000

escape_velocity = ((2 * gravity * radius_meters) ** 0.5) / 1000
print(f"Earth's escape velocity is approximately {escape_velocity:.2f} km/s")
print("\n")
#Task 8
"""
This program calculates the gravitational force between Earth and the Moon.
It uses Newton's law of universal gravitation: F = G * (m1 * m2) / r^2
G represents the gravitational constant.
"""

G = 6.67430e-11
mass_earth = 5.972e24 
mass_moon = 7.348e22  
distance = 384400000  

force = G * (mass_earth * mass_moon) / (distance ** 2)
print(f"The gravitational force is {force:.2e} Newtons")


