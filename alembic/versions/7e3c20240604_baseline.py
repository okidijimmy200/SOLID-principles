"""baseline

Revision ID: 7e3c20240604
Revises: 
Create Date: 2022-08-27 12:06:00.696505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e3c20240604'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'image',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('body', sa.String(100), nullable=False),)


def downgrade() -> None:
    op.drop_table('image')
