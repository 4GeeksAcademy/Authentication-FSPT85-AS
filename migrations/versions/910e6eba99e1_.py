"""empty message

Revision ID: 910e6eba99e1
Revises: a5cffa318ac2
Create Date: 2025-01-22 18:32:26.132720

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '910e6eba99e1'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('birth_year', sa.String(length=80), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('skin_color', sa.String(length=20), nullable=True),
    sa.Column('eye_color', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=80),
               nullable=True)
        batch_op.alter_column('is_active',
               existing_type=sa.BOOLEAN(),
               nullable=True)
        batch_op.drop_constraint('user_email_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint('user_email_key', ['email'])
        batch_op.alter_column('is_active',
               existing_type=sa.BOOLEAN(),
               nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=80),
               nullable=False)

    op.drop_table('character')
    # ### end Alembic commands ###
