"""add_indexes_for_filtering

Revision ID: 42f50583b788
Revises: 1c9524c327d2
Create Date: 2026-01-01 14:59:04.220685

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42f50583b788'
down_revision: Union[str, Sequence[str], None] = '1c9524c327d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: Add indexes for efficient filtering."""
    # Create composite index on (status, due_date) for filtered queries
    op.create_index(
        'ix_todos_status_due_date',
        'todos',
        ['status', 'due_date'],
        unique=False
    )

    # Create index on category column for category filtering
    op.create_index(
        'ix_todos_category',
        'todos',
        ['category'],
        unique=False
    )


def downgrade() -> None:
    """Downgrade schema: Remove indexes."""
    op.drop_index('ix_todos_category', table_name='todos')
    op.drop_index('ix_todos_status_due_date', table_name='todos')
