def replace_zero_with_na(book_data):
    modified_data = []
    for book_tuple in book_data:
        if book_tuple[-1] == 0.0:
            modified_tuple = book_tuple[:-1] + ("Non-Applicable",)
        else:
            modified_tuple = book_tuple
        modified_data.append(modified_tuple)
    return modified_data

def modify_late_fee_format(book_data):
    modified_data = []
    for book_tuple in book_data:
        if book_tuple[-1] != "Non-Applicable":
            formatted_price = '${:.1f}0'.format(float(book_tuple[-1]))
            modified_tuple = book_tuple[:-1] + (formatted_price,)
        else:
            modified_tuple = book_tuple
        modified_data.append(modified_tuple)
    return modified_data