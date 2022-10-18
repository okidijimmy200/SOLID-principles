"""baseline

Revision ID: 9260d79e4682
Revises: 
Create Date: 2022-09-27 11:05:22.061438

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9260d79e4682'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'phonebook',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('body', sa.String(100), nullable=False),)


def downgrade() -> None:
    op.drop_table('phonebook')
