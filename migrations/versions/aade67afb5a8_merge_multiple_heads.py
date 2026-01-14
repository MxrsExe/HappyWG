"""merge multiple heads

Revision ID: aade67afb5a8
Revises: 245d562ad608, 26bf635acc9e, 6c557be03476
Create Date: 2026-01-12 18:46:08.523149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aade67afb5a8'
down_revision = ('245d562ad608', '26bf635acc9e', '6c557be03476')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
