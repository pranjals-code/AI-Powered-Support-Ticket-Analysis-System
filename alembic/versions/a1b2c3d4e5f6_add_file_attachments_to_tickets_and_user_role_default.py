"""add file attachments to tickets and user role default

Revision ID: a1b2c3d4e5f6
Revises: 81e0edb1ef3d
Create Date: 2026-01-16 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '81e0edb1ef3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - add file attachment columns to tickets."""
    # Add the USER enum value to the userrole enum type if it doesn't exist
    op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'USER'")
    
    # PostgreSQL requires a commit between adding enum value and using it
    op.execute("COMMIT")
    op.execute("BEGIN")
    
    # Add photo column (max 6 MB)
    op.add_column('tickets', sa.Column('photo', sa.LargeBinary(), nullable=True))
    # Add photo filename
    op.add_column('tickets', sa.Column('photo_filename', sa.String(length=255), nullable=True))
    # Add file column (max 10 MB)
    op.add_column('tickets', sa.Column('file', sa.LargeBinary(), nullable=True))
    # Add file filename
    op.add_column('tickets', sa.Column('file_filename', sa.String(length=255), nullable=True))
    
    # Alter users.role column to add default value
    op.alter_column('users', 'role',
               nullable=False,
               server_default='USER')


def downgrade() -> None:
    """Downgrade schema - remove file attachment columns from tickets."""
    # Remove file columns from tickets
    op.drop_column('tickets', 'file_filename')
    op.drop_column('tickets', 'file')
    op.drop_column('tickets', 'photo_filename')
    op.drop_column('tickets', 'photo')
    
    # Remove default from users.role
    op.alter_column('users', 'role',
               existing_type=sa.Enum('ADMIN', 'AGENT', 'MANAGER', 'USER', name='userrole'),
               nullable=False,
               server_default=None)
