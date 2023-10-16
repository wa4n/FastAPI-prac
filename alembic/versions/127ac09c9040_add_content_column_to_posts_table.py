"""add content column to posts table

Revision ID: 127ac09c9040
Revises: 28694ba01599
Create Date: 2023-10-15 17:27:09.532294

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '127ac09c9040'
down_revision: Union[str, None] = '28694ba01599'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass

def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
