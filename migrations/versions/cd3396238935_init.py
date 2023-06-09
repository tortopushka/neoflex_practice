"""init

Revision ID: cd3396238935
Revises: 
Create Date: 2023-04-24 17:05:06.378750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd3396238935'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cache',
    sa.Column('id_cache', sa.Integer(), nullable=False),
    sa.Column('date_of_activity', sa.DateTime(), nullable=True),
    sa.Column('text_of_message', sa.Text(), nullable=True),
    sa.Column('language_code', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id_cache')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cache')
    # ### end Alembic commands ###
