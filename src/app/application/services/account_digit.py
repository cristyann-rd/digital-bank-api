def calculate_account_digit(
    account_number: str
) -> str:

    total = sum(
        int(digit)
        for digit in str(account_number)
        if digit.isdigit()
    )

    return str(total % 10)
