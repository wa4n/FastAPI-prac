"""add last few columns to posts table

Revision ID: bdff0bfb9c6f
Revises: 30193dbec4d5
Create Date: 2023-10-16 13:40:32.345258

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bdff0bfb9c6f'
down_revision: Union[str, None] = '30193dbec4d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column(
        "published", sa.Boolean(), nullable=False,
        server_default='TRUE')
    )
    op.add_column("posts", sa.Column(
        "created_at", sa.TIMESTAMP(timezone=True), nullable=False,
        server_default=sa.text('NOW()'))
    )
    pass



def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    
    pass
