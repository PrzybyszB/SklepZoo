"""change adress to address

Revision ID: a30112c0623d
Revises: ae736be1a299
Create Date: 2024-03-12 18:13:02.046999

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a30112c0623d'
down_revision = 'ae736be1a299'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address', sa.String(length=120), nullable=False))
        batch_op.drop_column('adress')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address', sa.String(length=120), nullable=True))
        batch_op.drop_column('adress')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('adress', mysql.VARCHAR(length=120), nullable=True))
        batch_op.drop_column('address')

    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('adress', mysql.VARCHAR(length=120), nullable=False))
        batch_op.drop_column('address')

    # ### end Alembic commands ###
