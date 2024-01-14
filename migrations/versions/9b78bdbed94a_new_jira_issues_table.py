"""new jira_issues table

Revision ID: 9b78bdbed94a
Revises: 
Create Date: 2024-01-14 20:16:10.727214

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b78bdbed94a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('jira_issues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(length=16), nullable=False),
    sa.Column('issue_type', sa.String(length=16), nullable=False),
    sa.Column('labels', sa.JSON(), nullable=False),
    sa.Column('title', sa.String(length=1024), nullable=False),
    sa.Column('description', sa.TEXT(), nullable=False),
    sa.Column('priority', sa.String(length=16), nullable=False),
    sa.Column('sprint', sa.String(length=1024), nullable=True),
    sa.Column('release', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('jira_issues')
    # ### end Alembic commands ###