"""empty message

Revision ID: 0799430e54ae
Revises: 
Create Date: 2019-12-05 23:54:42.752916

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0799430e54ae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=15), nullable=True),
    sa.Column('name', sa.String(length=15), nullable=True),
    sa.Column('email', sa.String(length=15), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('university', sa.String(length=15), nullable=True),
    sa.Column('password', sa.String(length=15), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('friends',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('friend_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['friend_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id', 'friend_id')
    )
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid_receiver', sa.Integer(), nullable=True),
    sa.Column('sender', sa.String(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('message', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['uid_receiver'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('message', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    op.drop_table('message')
    op.drop_table('friends')
    op.drop_table('user')
    # ### end Alembic commands ###