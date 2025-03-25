"""Add HNSW index on embedded_vector

Revision ID: 9c1bda219651
Revises: 
Create Date: 2025-03-24 19:22:52.356764

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from pgvector.sqlalchemy.vector import Vector

# revision identifiers, used by Alembic.
revision: str = '9c1bda219651'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_qa_history_qa_id', table_name='qa_history')
    op.drop_table('qa_history')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('qa_history',
    sa.Column('qa_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('input_text', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('embedded_vector', Vector(1536), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('qa_id', name='qa_history_pkey')
    )
    op.create_index('ix_qa_history_qa_id', 'qa_history', ['qa_id'], unique=False)
    # ### end Alembic commands ###
