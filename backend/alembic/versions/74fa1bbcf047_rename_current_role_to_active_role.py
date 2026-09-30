"""rename current_role to active_role

Revision ID: 74fa1bbcf047
Revises: 39e2e5b5b691
Create Date: 2026-09-30 10:48:48.401683

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74fa1bbcf047'
down_revision: Union[str, Sequence[str], None] = '39e2e5b5b691'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('users', 'current_role', new_column_name='active_role')


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('users', 'active_role', new_column_name='current_role')