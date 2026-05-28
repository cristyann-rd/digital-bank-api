from sqlalchemy import Sequence

account_number_seq = Sequence(
    "account_number_seq",
    start=10000000
)