"""added payment_method to Record

Revision ID: 7e365d8da21f
Revises: 33694891ec90
Create Date: 2022-06-15 14:32:27.905671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e365d8da21f'
down_revision = '33694891ec90'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('record', sa.Column('payment_method', sa.String(length=12), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('record', 'payment_method')
    # ### end Alembic commands ###