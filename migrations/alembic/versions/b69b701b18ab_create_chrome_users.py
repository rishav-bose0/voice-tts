"""create_chrome_users

Revision ID: b69b701b18ab
Revises: 9148cbb0a198
Create Date: 2024-01-02 12:53:53.792430

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b69b701b18ab'
down_revision: Union[str, None] = '9148cbb0a198'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'extensions_user_details',
        sa.Column('id', sa.String(length=14), primary_key=True),
        sa.Column('email', sa.String(100), nullable=False),
        sa.Column('email_id', sa.String(100), nullable=False),
        sa.Column('created_at', sa.Integer(), nullable=False),
        sa.Column('updated_at', sa.Integer(), nullable=False),
        sa.Column('deleted_at', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email', name='e_uq_email')
    )


def downgrade() -> None:
    op.drop_table('extensions_user_details')
