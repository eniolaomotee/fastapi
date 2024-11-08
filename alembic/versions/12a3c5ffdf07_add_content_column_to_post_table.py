"""add content column to post table

Revision ID: 12a3c5ffdf07
Revises: c0dd6c6f2dc7
Create Date: 2024-11-08 08:13:54.751606

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12a3c5ffdf07'
down_revision: Union[str, None] = 'c0dd6c6f2dc7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
