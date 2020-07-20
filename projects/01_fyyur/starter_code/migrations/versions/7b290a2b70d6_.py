"""empty message

Revision ID: 7b290a2b70d6
Revises: c5aeffdd2150
Create Date: 2020-07-19 23:58:27.570603

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b290a2b70d6'
down_revision = 'c5aeffdd2150'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Shows', 'start_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Shows', sa.Column('start_time', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
