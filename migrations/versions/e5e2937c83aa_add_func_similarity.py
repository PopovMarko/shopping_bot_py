"""Add func.similarity

Revision ID: e5e2937c83aa
Revises: 98ec12ba3f84
Create Date: 2026-09-11 12:30:06.632298

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e5e2937c83aa"
down_revision: Union[str, Sequence[str], None] = "98ec12ba3f84"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    op.execute(
        "CREATE INDEX ix_products_name_trgm ON products USING gin (name gin_trgm_ops)"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP INDEX IF EXISTS ix_products_name_trgm")
    op.execute("DROP EXTENSION IF EXISTS pg_trgm")
