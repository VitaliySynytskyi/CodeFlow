"""empty message

Revision ID: d0fbea378879
Revises: 
Create Date: 2023-04-12 20:37:46.562528

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd0fbea378879'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('email', table_name='user')
    op.drop_index('pwd', table_name='user')
    op.drop_index('username', table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('username', mysql.VARCHAR(length=80), nullable=False),
    sa.Column('email', mysql.VARCHAR(length=120), nullable=False),
    sa.Column('pwd', mysql.VARCHAR(length=300), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_index('username', 'user', ['username'], unique=False)
    op.create_index('pwd', 'user', ['pwd'], unique=False)
    op.create_index('email', 'user', ['email'], unique=False)
    # ### end Alembic commands ###