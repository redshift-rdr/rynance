"""updated Item

Revision ID: dc81651179a9
Revises: aa512b0c8c27
Create Date: 2022-03-21 21:48:21.882381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc81651179a9'
down_revision = 'aa512b0c8c27'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('repeat_end', sa.Date(), nullable=True))
    op.add_column('transaction', sa.Column('date', sa.Date(), nullable=True))
    op.create_index(op.f('ix_transaction_date'), 'transaction', ['date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transaction_date'), table_name='transaction')
    op.drop_column('transaction', 'date')
    op.drop_column('item', 'repeat_end')
    # ### end Alembic commands ###
