"""added paid field to Record

Revision ID: 5240f0622582
Revises: 7e365d8da21f
Create Date: 2022-06-15 14:45:48.734628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5240f0622582'
down_revision = '7e365d8da21f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('record', sa.Column('paid', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('record', 'paid')
    # ### end Alembic commands ###
