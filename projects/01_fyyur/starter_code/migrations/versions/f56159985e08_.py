"""empty message

Revision ID: f56159985e08
Revises: e769a70c8666
Create Date: 2022-05-30 13:38:33.229465

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f56159985e08'
down_revision = 'e769a70c8666'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('website_link', sa.String(), nullable=True))
    op.drop_column('Artist', 'website')
    op.add_column('Venue', sa.Column('website_link', sa.String(), nullable=True))
    op.drop_column('Venue', 'website')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('website', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('Venue', 'website_link')
    op.add_column('Artist', sa.Column('website', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('Artist', 'website_link')
    # ### end Alembic commands ###