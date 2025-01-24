"""empty message

Revision ID: 0028c96049a0
Revises: 33d4499c6859
Create Date: 2025-01-24 18:19:59.566775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0028c96049a0'
down_revision = '33d4499c6859'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('vehicle_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'vehicles', ['vehicle_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('vehicle_id')

    # ### end Alembic commands ###
