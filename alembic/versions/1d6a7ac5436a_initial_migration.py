"""Initial migration

Revision ID: 1d6a7ac5436a
Revises: 
Create Date: 2024-08-07 15:32:10.067012

"""
import sqlalchemy as sa
from typing import Sequence, Union
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '1d6a7ac5436a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Enum type definition
snake_type_enum = postgresql.ENUM('python', 'cobra', 'viper', name='snaketype')

def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('email', sa.String, primary_key=True),
        sa.Column('hash_pwd', sa.String),
        sa.Column('name', sa.String)
    )

    op.create_table(
        'tank',
        sa.Column('id', sa.Integer, primary_key=True)
    )

    op.create_table(
        'snake',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('type', sa.Enum('python', 'cobra', 'viper', name='snaketype'), nullable=False),
        sa.Column('tank_id', sa.Integer, sa.ForeignKey('tank.id'), nullable=False)
    )


def downgrade() -> None:
        op.drop_table('user')
        op.drop_table('tank')
        op.drop_table('snakes')    
        snake_type_enum.drop(op.get_bind())
