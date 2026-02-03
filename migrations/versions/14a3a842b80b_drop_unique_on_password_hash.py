"""drop unique on password_hash

Revision ID: 14a3a842b80b
Revises: 67355bf1e881
Create Date: 2026-02-03 13:14:51.395238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14a3a842b80b'
down_revision = '67355bf1e881'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('USER') as batch_op:
        batch_op.drop_constraint('uq_USER_password_hash', type_='unique')

def downgrade():
    with op.batch_alter_table('USER') as batch_op:
        batch_op.create_unique_constraint('uq_USER_password_hash', ['password_hash'])
