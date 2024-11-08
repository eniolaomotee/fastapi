"""add foreign key to posts table

Revision ID: 3a6972380139
Revises: 30eb942482dd
Create Date: 2024-11-08 08:39:56.861383

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a6972380139'
down_revision: Union[str, None] = '30eb942482dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# so in creating a relationship between our users and posts tables we'd need to create an FK between them using alembic, First we'd add a colum with the name of the coulm we want to create on which table, then we create the foreign key by setting the name as well as the source and referent table and the linkage on the table which is the owner id and users' id.
def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk',source_table="posts",referent_table="users" ,local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk',table_name="posts")
    op.drop_column('posts','owner_id')
    pass
