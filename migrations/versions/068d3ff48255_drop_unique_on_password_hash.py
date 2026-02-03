"""drop unique on password_hash

Revision ID: 068d3ff48255
Revises: 14a3a842b80b
Create Date: 2026-02-03 13:19:24.930159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '068d3ff48255'
down_revision = '14a3a842b80b'
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
