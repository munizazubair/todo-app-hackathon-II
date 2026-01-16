"""Add users table and user_id to todos

Revision ID: a3b4c5d6e7f8
Revises: 42f50583b788
Create Date: 2026-01-16

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a3b4c5d6e7f8'
down_revision: Union[str, Sequence[str], None] = '42f50583b788'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: Create users table and add user_id to todos."""
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create unique index on email
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # Add user_id column to todos (nullable initially for existing data)
    op.add_column(
        'todos',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True)
    )

    # Create index on user_id for efficient queries
    op.create_index('ix_todos_user_id', 'todos', ['user_id'], unique=False)

    # Add foreign key constraint
    op.create_foreign_key(
        'fk_todos_user_id',
        'todos',
        'users',
        ['user_id'],
        ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    """Downgrade schema: Remove users table and user_id from todos."""
    # Remove foreign key constraint
    op.drop_constraint('fk_todos_user_id', 'todos', type_='foreignkey')

    # Remove index on user_id
    op.drop_index('ix_todos_user_id', table_name='todos')

    # Remove user_id column from todos
    op.drop_column('todos', 'user_id')

    # Remove unique index on email
    op.drop_index('ix_users_email', table_name='users')

    # Drop users table
    op.drop_table('users')
