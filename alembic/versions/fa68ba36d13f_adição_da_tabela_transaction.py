"""Mantem a cadeia historica sem repetir a chave primaria de accounts.

Revision ID: fa68ba36d13f
Revises: 34610e4ac669
Create Date: 2026-06-10 00:05:29.568613
"""

from typing import Sequence, Union


revision: str = "fa68ba36d13f"
down_revision: Union[str, Sequence[str], None] = "34610e4ac669"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
