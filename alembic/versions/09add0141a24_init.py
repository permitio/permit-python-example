"""Init

Revision ID: 09add0141a24
Revises: 1d6a7ac5436a
Create Date: 2024-08-11 18:04:26.645406

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09add0141a24'
down_revision: Union[str, None] = '1d6a7ac5436a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
