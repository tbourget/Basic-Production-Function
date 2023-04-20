from decimal import *

def calculate_total_charge(state_abbrev: str, item_records: list[tuple]) -> float:
    print(f"Calculating total charge for item records (State: {state_abbrev.upper()})")
    total = 0

    # Parse the records for problematic values
    record_index = 0
    while record_index < len(item_records):
        # Negative values
        if item_records[record_index][1] < 0:
            print(f'{item_records[record_index][0]} cannot be processed, refunds/negative prices aren\'t accepted')
            del item_records[record_index]
            continue
        # Dollar float values instead of cent integers
        if isinstance((item_records[record_index][1]), float):
            print(f'{item_records[record_index][0]}\'s price was input as a decimal but it should be in cents. '
                  f'Assuming dollar value was input and converting to cents, please adjust input.')
            cent_value = (Decimal(item_records[record_index][1]) * Decimal(100)).quantize(Decimal('1'))
            cent_value = int(cent_value)
            revised_record = (item_records[record_index][0], cent_value, item_records[record_index][2])
            item_records[record_index] = revised_record

        record_index += 1

    # Calculate charge before taxes
    print("\n-------ORIGINAL CHARGE-------")
    for record in item_records:
        total += record[1]
        print(f'\t{record[0]}: {cents_to_dollars(record[1])}')
    print(f'Charge (before tax): ${cents_to_dollars(total)}')

    # Calculate charge after taxes
    if state_abbrev.lower() == 'de':
        total += calculate_DE_taxes(item_records)
    elif state_abbrev.lower() == 'nj':
        total += calculate_NJ_taxes(item_records)
    elif state_abbrev.lower() == 'pa':
        total += calculate_PA_taxes(item_records)
    else:
        print(f'No tax information stored for state abbreviation "{state_abbrev}"')
        return total

    print("\n--------GROSS CHARGE---------")
    print(f'Total Charge (after tax): ${cents_to_dollars(total)}\n')
    return total


def calculate_DE_taxes(item_records: list[tuple]) -> float:
    total_tax = 0.00

    print("\n----------TAXES--------------")
    print("\tDelaware has no sales tax!")
    print('Total Tax: ${:.02f}'.format(cents_to_dollars(total_tax)))
    return total_tax


def calculate_NJ_taxes(item_records: list[tuple]) -> float:
    tax_rate = 0.066
    total_tax = 0

    print("\n----------TAXES--------------")
    for record in item_records:
        # Statement to skip items that get tax exemptions
        if record[2].lower() == "wic eligible food":
            print(f'\t{record[0]} is exempt from taxes for being Wic Eligible Food')
            continue
        elif record[2].lower() == "clothing":
            if not clothing_item_is_fur(record):
                print(f'\t{record[0]} is exempt from taxes for being non-fur clothing')
                continue

        item_tax = (Decimal(record[1]) * Decimal(tax_rate)).quantize(Decimal('1'))
        print(f'\tTax for {record[0]}: ${cents_to_dollars(item_tax)}')
        total_tax += item_tax

    print('Total Tax: ${:.02f}'.format(cents_to_dollars(total_tax)))
    return total_tax


def calculate_PA_taxes(item_records: list[tuple]) -> float:
    tax_rate = 0.06
    total_tax = 0

    print("\n----------TAXES--------------")
    for record in item_records:
        # Statement to skip items that get tax exemptions
        if record[2].lower() == "wic eligible food":
            print(f'\t{record[0]} is exempt from taxes for being Wic Eligible Food')
            continue
        elif record[2].lower() == "clothing":
            print(f'\t{record[0]} is exempt from taxes for being clothing')
            continue

        item_tax = (Decimal(record[1]) * Decimal(tax_rate)).quantize(Decimal('1'))
        print(f'\tTax for {record[0]}: ${cents_to_dollars(item_tax)}')
        total_tax += item_tax

    print('Total Tax: ${:.02f}'.format(cents_to_dollars(total_tax)))
    return total_tax


def clothing_item_is_fur(item_record: tuple) -> bool:
    item_record_name_words = item_record[0].lower().split(" ")

    if "fur" in item_record_name_words:
        return True

    return False


def cents_to_dollars(cents: int) -> float:
    return cents / 100


if __name__ == '__main__':
    test_item_records = [
        ("Camera", 12.99, "Tech"),
        ("Shirt", 12.99, "Clothing"),
        ("Fur Hat", 16.99, "Clothing"),
        ("Eggs", 10.99, "WIC Eligible Food"),
        ("Peeps", 11.99, "Food"),
    ]
    charge = calculate_total_charge("nj", test_item_records)



