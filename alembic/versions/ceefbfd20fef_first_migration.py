"""first migration

Revision ID: ceefbfd20fef
Revises: 72e4744e9d96
Create Date: 2021-10-17 02:31:52.494648

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ceefbfd20fef'
down_revision = '72e4744e9d96'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'test_items', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'test_items', type_='unique')
    # ### end Alembic commands ###
