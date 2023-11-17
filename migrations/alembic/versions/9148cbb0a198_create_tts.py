"""create_tts

Revision ID: 9148cbb0a198
Revises: db7ec438eabc
Create Date: 2023-10-25 19:00:37.607324

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import ForeignKey
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9148cbb0a198'
down_revision: Union[str, None] = 'db7ec438eabc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tts_details',
        sa.Column('id', sa.String(length=14), primary_key=True),
        sa.Column('project_id', sa.String(length=14), ForeignKey("project_details.id"), nullable=False),
        sa.Column('text', sa.Text, nullable=False),
        sa.Column('language', sa.String(50), nullable=False),
        # sa.Column('speaker_id', sa.String(length=14), nullable=False),
        sa.Column('duration', sa.String(50), nullable=True),
        sa.Column('speech_s3_link', sa.String(400), nullable=True),
        sa.Column('speech_metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('block_number', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.Integer(), nullable=False),
        sa.Column('updated_at', sa.Integer(), nullable=False),
        sa.Column('deleted_at', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('tts_details')
