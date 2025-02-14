"""empty message

Revision ID: 406c2d3edb56
Revises: 4a3cbd33f796
Create Date: 2025-01-22 18:50:46.239320

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '406c2d3edb56'
down_revision = '4a3cbd33f796'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vehicles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('model', sa.String(length=80), nullable=True),
    sa.Column('cargo_capacity', sa.Integer(), nullable=True),
    sa.Column('length', sa.Numeric(scale=2), nullable=True),
    sa.Column('passengers', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vehicles')
    # ### end Alembic commands ###
