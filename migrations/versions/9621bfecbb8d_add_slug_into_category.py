"""Add slug into category

Revision ID: 9621bfecbb8d
Revises: bf21abc258f3
Create Date: 2024-03-12 19:27:55.222620

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9621bfecbb8d'
down_revision = 'bf21abc258f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_slug', sa.String(length=50), nullable=True))
        batch_op.drop_index('slug')
        batch_op.create_unique_constraint(None, ['category_slug'])
        batch_op.drop_column('slug')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.add_column(sa.Column('slug', mysql.VARCHAR(length=50), nullable=True))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_index('slug', ['slug'], unique=True)
        batch_op.drop_column('category_slug')

    # ### end Alembic commands ###
