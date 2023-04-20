from main import *

def test_calculate_total_charge():
    # Regular data test (results were found with calculator and then tested)
    test_item_records = (
        ("Camera", 1299, "Tech"),
        ("Shirt", 1299, "Clothing"),
        ("Fur hat", 1699, "Clothing"),
        ("Eggs", 1099, "WIC Eligible Food"),
        ("Peeps", 1199, "Food"),
    )

    charge = calculate_total_charge("pa",test_item_records)
    assert charge == 6745
    charge = calculate_total_charge("nj",test_item_records)
    assert charge == 6872
    charge = calculate_total_charge("de",test_item_records)
    assert charge == 6595

    # Boundary tests
    # No item records
    test_item_records = ()
    charge = calculate_total_charge("pa", test_item_records)
    assert charge == 0
    charge = calculate_total_charge("nj", test_item_records)
    assert charge == 0
    charge = calculate_total_charge("de", test_item_records)
    assert charge == 0

    # Unexpected data tests
    # Negative number for price
    test_item_records = [
        ("Camera", -1299, "Tech"),
        ("Shirt", -1299, "Clothing"),
        ("Fur hat", -1699, "Clothing"),
        ("Eggs", -1099, "WIC Eligible Food"),
        ("Peeps", -1199, "Food"),
    ]
    charge = calculate_total_charge("nj", test_item_records)
    assert charge == 0

    # A word with the string "fur" in it that is not fur, but clothing
    test_item_records = [
        ("Camera", 1299, "Tech"),
        ("Minecraft Furnace Shirt", 1299, "Clothing"),
        ("Fur hat", 1699, "Clothing"),
        ("Eggs", 1099, "WIC Eligible Food"),
        ("Peeps", 1199, "Food"),
    ]
    charge = calculate_total_charge("nj", test_item_records)
    assert charge == 6872

    # Dollars instead of cents
    test_item_records = [
        ("Camera", 12.99, "Tech"),
        ("Shirt", 12.99, "Clothing"),
        ("Fur hat", 16.99, "Clothing"),
        ("Eggs", 10.99, "WIC Eligible Food"),
        ("Peeps", 11.99, "Food"),
    ]

    charge = calculate_total_charge("pa", test_item_records)
    assert charge == 6745
    charge = calculate_total_charge("nj", test_item_records)
    assert charge == 6872
    charge = calculate_total_charge("de", test_item_records)
    assert charge == 6595
