"""empty message

Revision ID: 0369a028f800
Revises: 995a315cb6b7
Create Date: 2021-08-11 16:20:05.158834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0369a028f800'
down_revision = '995a315cb6b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('article_type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('type_name', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('article', sa.Column('type_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'article', 'article_type', ['type_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'article', type_='foreignkey')
    op.drop_column('article', 'type_id')
    op.drop_table('article_type')
    # ### end Alembic commands ###
