"""empty message

Revision ID: 091d4d8b8f3e
Revises: fc558313c12c
Create Date: 2024-09-11 11:49:32.328602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import fastapi_users_db_sqlalchemy



# revision identifiers, used by Alembic.
revision: str = '091d4d8b8f3e'
down_revision: Union[str, None] = 'fc558313c12c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accesstoken',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=43), nullable=False),
    sa.Column('created_at', fastapi_users_db_sqlalchemy.generics.TIMESTAMPAware(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('token')
    )
    op.create_index(op.f('ix_accesstoken_created_at'), 'accesstoken', ['created_at'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_accesstoken_created_at'), table_name='accesstoken')
    op.drop_table('accesstoken')
    # ### end Alembic commands ###
