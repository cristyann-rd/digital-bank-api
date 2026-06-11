"""Adição da tabela Transaction.

Revision ID: fa68ba36d13f
Revises: 34610e4ac669
Create Date: 2026-06-10 00:05:29.568613

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa68ba36d13f'
down_revision: Union[str, Sequence[str], None] = '34610e4ac669'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_primary_key(
    "pk_accounts",
    "accounts",
    ["account_id"]
)
    
    # ### end Alembic commands ###


