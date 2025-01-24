"""empty message

Revision ID: 9e05a7b8db68
Revises: 0786e8e3fdc2
Create Date: 2025-01-22 18:43:19.338594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e05a7b8db68'
down_revision = '0786e8e3fdc2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('birth_year', sa.String(length=80), nullable=True),
    sa.Column('height', sa.Numeric(precision=4, scale=2), nullable=True),
    sa.Column('skin_color', sa.String(length=20), nullable=True),
    sa.Column('eye_color', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('characters')
    # ### end Alembic commands ###
