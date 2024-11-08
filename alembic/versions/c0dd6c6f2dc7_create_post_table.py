"""create post table

Revision ID: c0dd6c6f2dc7
Revises: 
Create Date: 2024-11-08 01:09:05.140165

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0dd6c6f2dc7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# When we run this,it runs this and makes the changes here under this function
def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True), sa.Column('title',sa.String(),nullable=False))
    pass


# If we want to rollback we'd use this function to rollback the changes
def downgrade() -> None:
    op.drop_table('posts')
    pass
