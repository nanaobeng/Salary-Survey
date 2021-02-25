"""create benchmark job pool

Revision ID: 6e44fb977767
Revises: 2347eec7a00e
Create Date: 2021-02-23 22:36:25.741882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e44fb977767'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'benchmark_job_pool',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('job_title', sa.String(100)),
        sa.Column('grade', sa.String(50)),
        sa.Column('department_id', sa.Integer, sa.ForeignKey('department.id')),
        sa.Column('area_id', sa.Integer, sa.ForeignKey('area.id')),
        sa.Column('reporting_relationship',sa.String(100)),
        sa.Column('job_description', sa.String(1000)),
        sa.Column('duties_and_responsibility', sa.String(1000)),
        sa.Column('financial_responsibilities', sa.String(1000)),
        sa.Column('technical_qualification', sa.String(1000)),
        sa.Column('minimum_years_of_experience', sa.String(1000)),
        sa.Column('status', sa.String(100)),
        sa.Column('timestamp', sa.DateTime, nullable=False)
    )


def downgrade():
    op.drop_table('benchmark_job_pool')
    
