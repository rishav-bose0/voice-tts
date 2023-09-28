"""create_tts

Revision ID: affe3a5fdfa1
Revises: 5383085ed4f4
Create Date: 2023-09-25 11:06:47.151184

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'affe3a5fdfa1'
down_revision: Union[str, None] = '5383085ed4f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tts_details',
        sa.Column('id', sa.String(length=14), primary_key=True),
        sa.Column('user_id', sa.String(length=14), nullable=False),
        sa.Column('text', sa.Text, nullable=False),
        sa.Column('language', sa.String(50), nullable=False),
        sa.Column('speaker_id', sa.String(length=14), nullable=False),
        sa.Column('duration', sa.String(50), nullable=True),
        sa.Column('speech_metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.Integer(), nullable=False),
        sa.Column('updated_at', sa.Integer(), nullable=False),
        sa.Column('deleted_at', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('tts_details')
