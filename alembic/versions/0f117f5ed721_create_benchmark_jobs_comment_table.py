"""Create benchmark jobs comment table

Revision ID: 0f117f5ed721
Revises: 2347eec7a00e
Create Date: 2021-02-10 08:41:21.107386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f117f5ed721'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'main_benchmark_job_comment',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('comment', sa.Text, nullable=False),
        sa.Column('timestamp', sa.DateTime, nullable=False),
        sa.Column('main_benchmark_job_id', sa.Integer, sa.ForeignKey('department.id')),
    )


def downgrade():
    op.drop_table('main_benchmark_job_comment')
