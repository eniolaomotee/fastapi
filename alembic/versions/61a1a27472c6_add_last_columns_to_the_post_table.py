"""add last columns to the post table

Revision ID: 61a1a27472c6
Revises: 3a6972380139
Create Date: 2024-11-08 08:49:34.081784

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61a1a27472c6'
down_revision: Union[str, None] = '3a6972380139'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published',sa.Boolean(),nullable=False,server_default='True'),)
    
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')),)              
    
    pass

#   op.add_column('posts',sa.Column('content',sa.String(),nullable=False))

def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
