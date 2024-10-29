"""Init revision

Revision ID: 5c4cb89bd87e
Revises: 
Create Date: 2024-10-29 16:19:00.691221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c4cb89bd87e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pictures_info',
    sa.Column('picture_title', sa.String(), nullable=False),
    sa.Column('path_to_file', sa.String(), nullable=False),
    sa.Column('upload_date', sa.Date(), nullable=False),
    sa.Column('resolution', sa.String(), nullable=False),
    sa.Column('size', sa.Float(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pictures_info')
    # ### end Alembic commands ###
