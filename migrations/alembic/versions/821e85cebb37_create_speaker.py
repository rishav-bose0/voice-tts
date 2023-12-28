"""create_speaker

Revision ID: 821e85cebb37
Revises: 
Create Date: 2023-09-25 10:47:29.116964

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '821e85cebb37'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# emotions_type = 'emotions_type'
# EmotionEnum = ENUM('happy', 'sad', 'angry', 'neutral', name='emotion_enum')
# EmotionArray = ARRAY(EmotionEnum, dimensions=1)


def upgrade() -> None:
    op.create_table(
        'speaker_details',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('gender', sa.String(2), nullable=True),
        sa.Column('language', sa.String(100), nullable=True),
        sa.Column('country', sa.String(100), nullable=True),
        sa.Column('emotions', sa.ARRAY(sa.String(100))),
        sa.Column('model_name', sa.String(100), nullable=False),
        sa.Column('image_link', sa.String(300), nullable=False),
        sa.Column('voice_preview_link', sa.String(300), nullable=True),
        sa.Column('user_id', sa.String(14), nullable=True),
        sa.Column('clone_details', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('speaker_type', sa.Enum('public', 'clone', name='speaker_type'), nullable=False),
        sa.Column('created_at', sa.Integer(), nullable=False),
        sa.Column('updated_at', sa.Integer(), nullable=False),
        sa.Column('deleted_at', sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('speaker_details')
