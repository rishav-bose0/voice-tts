"""create_projects

Revision ID: db7ec438eabc
Revises: 5383085ed4f4
Create Date: 2023-10-25 11:31:15.125958

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import ForeignKey

# revision identifiers, used by Alembic.
revision: str = 'db7ec438eabc'
down_revision: Union[str, None] = '5383085ed4f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'project_details',
        sa.Column('id', sa.String(length=14), primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('user_id', sa.String(length=14), ForeignKey("user_details.id"), nullable=False),
        sa.Column('created_at', sa.Integer(), nullable=False),
        sa.Column('updated_at', sa.Integer(), nullable=False),
        sa.Column('deleted_at', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('project_details')
