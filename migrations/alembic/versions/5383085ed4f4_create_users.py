"""create_users

Revision ID: 5383085ed4f4
Revises: 821e85cebb37
Create Date: 2023-09-25 11:03:01.329715

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '5383085ed4f4'
down_revision: Union[str, None] = '821e85cebb37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user_details',
        sa.Column('id', sa.String(length=14), primary_key=True),
        sa.Column('first_name', sa.String(50), nullable=False),
        sa.Column('last_name', sa.String(50), nullable=False),
        sa.Column('password', sa.String(50), nullable=True),
        sa.Column('email', sa.String(50), nullable=False),
        sa.Column('privilege_type', sa.Enum('free', 'subscribed', name='privilege_type'), nullable=False),
        sa.Column('token', sa.String(2000), nullable=False),
        sa.Column('created_at', sa.Integer(), nullable=False),
        sa.Column('updated_at', sa.Integer(), nullable=False),
        sa.Column('deleted_at', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email', name='uq_email')
    )


def downgrade() -> None:
    op.drop_table('user_details')
