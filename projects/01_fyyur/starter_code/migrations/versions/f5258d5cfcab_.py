"""empty message

Revision ID: f5258d5cfcab
Revises: 506d5697ff2c
Create Date: 2022-05-29 17:13:39.206068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5258d5cfcab'
down_revision = '506d5697ff2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_description', sa.Text(), nullable=True))
    op.drop_column('Artist', 'seeking_describtion')
    op.add_column('Venue', sa.Column('seeking_description', sa.Text(), nullable=True))
    op.drop_column('Venue', 'seeking_describtion')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('seeking_describtion', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_column('Venue', 'seeking_description')
    op.add_column('Artist', sa.Column('seeking_describtion', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_column('Artist', 'seeking_description')
    # ### end Alembic commands ###
