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


def upgrade() -> None:
       # Create the user table
    op.create_table(
        'user',
        sa.Column('email', sa.String, primary_key=True),
        sa.Column('hash_pwd', sa.String),
        sa.Column('name', sa.String)
    )

    # Create the design table
    op.create_table(
        'design',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),  
        sa.Column('description', sa.Text, nullable=True),  
        sa.Column('user_email', sa.String, sa.ForeignKey('user.email'), nullable=False)
    )

    # Create the comment table
    op.create_table(
        'comment',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('content', sa.Text, nullable=False),  
        sa.Column('design_id', sa.Integer, sa.ForeignKey('design.id'), nullable=False),
        sa.Column('user_email', sa.String, sa.ForeignKey('user.email'), nullable=False)
    )


def downgrade() -> None:
        op.drop_table('user')
        op.drop_table('design')
        op.drop_table('comment')    
