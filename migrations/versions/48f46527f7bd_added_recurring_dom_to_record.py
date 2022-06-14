"""added recurring_dom to record

Revision ID: 48f46527f7bd
Revises: 20d742ca3ed0
Create Date: 2022-06-04 10:41:14.321823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48f46527f7bd'
down_revision = '20d742ca3ed0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('record', sa.Column('recurring_dom', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('record', 'recurring_dom')
    # ### end Alembic commands ###