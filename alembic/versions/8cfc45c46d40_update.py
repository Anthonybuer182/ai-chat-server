"""update

Revision ID: 8cfc45c46d40
Revises: 7d2e4691a87d
Create Date: 2025-01-15 14:44:59.585018

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cfc45c46d40'
down_revision = '7d2e4691a87d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('characters', sa.Column('style', sa.String(length=15), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('characters', 'style')
    # ### end Alembic commands ###
