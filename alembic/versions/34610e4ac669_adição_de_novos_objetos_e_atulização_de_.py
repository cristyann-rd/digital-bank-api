"""Atualiza a chave primaria e o tipo monetario de accounts.

Revision ID: 34610e4ac669
Revises: 21f0e465068c
Create Date: 2026-06-09 22:36:03.065997
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "34610e4ac669"
down_revision: Union[str, Sequence[str], None] = "21f0e465068c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "accounts",
        sa.Column("account_id", sa.UUID(), nullable=True),
    )
    op.execute(
        "UPDATE accounts "
        "SET account_id = gen_random_uuid() "
        "WHERE account_id IS NULL"
    )
    op.alter_column("accounts", "account_id", nullable=False)
    op.alter_column(
        "accounts",
        "balance",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        type_=sa.Numeric(precision=18, scale=2),
        existing_nullable=False,
    )
    op.drop_constraint("accounts_pkey", "accounts", type_="primary")
    op.drop_column("accounts", "id")
    op.create_primary_key("pk_accounts", "accounts", ["account_id"])


def downgrade() -> None:
    op.add_column(
        "accounts",
        sa.Column("id", sa.Integer(), nullable=True),
    )
    op.execute("CREATE SEQUENCE IF NOT EXISTS accounts_id_seq")
    op.execute(
        "UPDATE accounts "
        "SET id = nextval('accounts_id_seq') "
        "WHERE id IS NULL"
    )
    op.alter_column("accounts", "id", nullable=False)
    op.drop_constraint("pk_accounts", "accounts", type_="primary")
    op.create_primary_key("accounts_pkey", "accounts", ["id"])
    op.drop_column("accounts", "account_id")
    op.alter_column(
        "accounts",
        "balance",
        existing_type=sa.Numeric(precision=18, scale=2),
        type_=sa.DOUBLE_PRECISION(precision=53),
        existing_nullable=False,
    )
