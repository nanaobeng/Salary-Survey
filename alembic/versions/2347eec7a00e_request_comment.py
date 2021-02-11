"""request_comment

Revision ID: 2347eec7a00e
Revises: f3787fa495a0
Create Date: 2021-02-09 09:29:24.440009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2347eec7a00e'
down_revision = '0f117f5ed721'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'request_comment',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('comment', sa.String(100)),
        sa.Column('service_id', sa.Integer),
    )


def downgrade():
    op.drop_table('request_comment')