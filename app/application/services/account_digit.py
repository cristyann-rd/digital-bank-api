def calculate_account_digit(
    account_number: int
) -> str:

    total = sum(
        int(digit)
        for digit in str(account_number)
    )

    return str(total % 10)