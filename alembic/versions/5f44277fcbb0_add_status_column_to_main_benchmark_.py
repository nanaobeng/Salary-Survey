"""add status column to main benchmark table

Revision ID: 5f44277fcbb0
Revises: 0f117f5ed721
Create Date: 2021-02-11 15:26:01.368239

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f44277fcbb0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('main_benchmark_job', sa.Column('status', sa.String(50)))


def downgrade():
    op.drop_column('main_benchmark_job', 'status')
