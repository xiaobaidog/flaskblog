"""empty message

Revision ID: 995a315cb6b7
Revises: 6aa77eb23aeb
Create Date: 2021-08-11 16:12:13.496552

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '995a315cb6b7'
down_revision = '6aa77eb23aeb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('comment', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.Column('cdatetime', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    # ### end Alembic commands ###