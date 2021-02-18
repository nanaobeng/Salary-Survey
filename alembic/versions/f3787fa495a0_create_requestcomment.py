"""create RequestComment

Revision ID: f3787fa495a0
Revises: bdbe9cbad60d
Create Date: 2021-02-09 09:07:36.402885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3787fa495a0'
down_revision = 'bdbe9cbad60d'
branch_labels = None
depends_on = None


def upgrade():
  
    op.create_table(
        'RequestComment',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('comment', sa.String(100)),
        sa.Column('service_id', sa.Integer),
    )

def downgrade():
    op.drop_table('RequestComment')
