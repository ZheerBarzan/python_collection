def celsius_to_fahrenheit(celsius):
    return celsius * 9/5 + 32

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

def celsius_to_kelvin(celsius):
    return celsius + 273.15

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def fahrenheit_to_kelvin(fahrenheit):
    return celsius_to_kelvin(fahrenheit_to_celsius(fahrenheit))

def kelvin_to_fahrenheit(kelvin):
    return celsius_to_fahrenheit(kelvin_to_celsius(kelvin))

def convert_temperature(value, from_unit, to_unit):
    if from_unit == 'c':
        if to_unit == 'f':
            return celsius_to_fahrenheit(value), "°F"
        elif to_unit == 'k':
            return celsius_to_kelvin(value), "K"
    elif from_unit == 'f':
        if to_unit == 'c':
            return fahrenheit_to_celsius(value), "°C"
        elif to_unit == 'k':
            return fahrenheit_to_kelvin(value), "K"
    elif from_unit == 'k':
        if to_unit == 'c':
            return kelvin_to_celsius(value), "°C"
        elif to_unit == 'f':
            return kelvin_to_fahrenheit(value), "°F"
    return None, None  # Invalid conversion

# Main Program
try:
    temperature = float(input("Enter the temperature you want to convert: "))
    from_unit = input("Enter 'c' for Celsius, 'f' for Fahrenheit, or 'k' for Kelvin: ").lower()
    to_unit = input("Enter the unit to convert to ('c', 'f', or 'k'): ").lower()

    result, unit_label = convert_temperature(temperature, from_unit, to_unit)

    if result is not None:
        print(f"{temperature}{from_unit.upper()} is equal to {result:.2f}{unit_label}")
    else:
        print("Invalid conversion units provided.")
except ValueError:
    print("Invalid temperature value entered. Please enter a numeric value.")
