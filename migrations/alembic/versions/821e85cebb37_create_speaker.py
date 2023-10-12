"""create_speaker

Revision ID: 821e85cebb37
Revises: 
Create Date: 2023-09-25 10:47:29.116964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM, ARRAY

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
        sa.Column('id', sa.String(length=14), primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('gender', sa.String(2), nullable=False),
        sa.Column('language', sa.String(100), nullable=False),
        sa.Column('emotions', sa.ARRAY(sa.String(100))),
        sa.Column('model_name', sa.String(100), nullable=False),
        sa.Column('created_at', sa.Integer(), nullable=False),
        sa.Column('updated_at', sa.Integer(), nullable=False),
        sa.Column('deleted_at', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('speaker_details')
