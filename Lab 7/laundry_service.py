
def parse_order(text):
    if not isinstance(text, str) or ':' not in text:
        raise ValueError("Invalid order format. Use garment:weight")

    parts = text.split(':')
    if len(parts) != 2:
        raise ValueError("Enter exactly one ':' separator")

    garment, kg = parts
    garment = garment.strip()

    if not garment:
        raise ValueError("Garment name cannot be empty")

    try:
        kg = float(kg)
    except (ValueError, TypeError):
        raise ValueError("Weight must be a valid number")

    if not kg > 0 or not kg < float('inf'):
        raise ValueError("Weight must be a positive finite number")

    return garment.title(), kg


def weight_average(weights_csv):
    if not isinstance(weights_csv, str) or not weights_csv.strip():
        raise ValueError("Weights cannot be empty")

    try:
        values = [int(r.strip()) for r in weights_csv.split(',')]
    except ValueError:
        raise ValueError("All weights must be integers")

    if not values:
        raise ValueError("At least one weight is required")

    if any(value < 0 for value in values):
        raise ValueError("Weights cannot be negative")

    return sum(values) // len(values)


def payable_charge(text):
    if not isinstance(text, str) or '|' not in text:
        raise ValueError("Invalid format. Use charge|discount")

    parts = text.split('|')
    if len(parts) != 2:
        raise ValueError("Enter exactly one '|' separator")

    charge, discount = parts

    try:
        charge = float(charge)
        discount = float(discount)
    except ValueError:
        raise ValueError("Charge and discount must be valid numbers")

    if not (0 <= charge < float('inf')) or not (0 <= discount < float('inf')):
        raise ValueError("Charge and discount must be non-negative finite numbers")

    total = charge * 1.18 - discount
    return max(total, 0)


def main():
    print("==== Running parse_order ====")
    user_input = input("Enter garment:weight in kg (e.g. regular:6): ")
    try:
        result = parse_order(user_input)
        print("Garment and Weight:", result)
    except ValueError as e:
        print("Error:", e)

    print("\n==== Running weight_average ====")
    user_input = input("Enter garment weights as CSV (e.g. 3,5,8): ")
    try:
        result = weight_average(user_input)
        print("Average Weight:", result)
    except ValueError as e:
        print("Error:", e)

    print("\n==== Running payable_charge ====")
    user_input = input("Enter charge|discount (e.g. 300|40): ")
    try:
        result = payable_charge(user_input)
        print("Payable Charge:", result)
    except ValueError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
