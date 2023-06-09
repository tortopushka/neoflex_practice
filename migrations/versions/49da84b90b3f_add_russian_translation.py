"""add_russian_translation

Revision ID: 49da84b90b3f
Revises: cd3396238935
Create Date: 2023-04-27 13:37:44.996771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49da84b90b3f'
down_revision = 'cd3396238935'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cache', sa.Column('russian_translation', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cache', 'russian_translation')
    # ### end Alembic commands ###
