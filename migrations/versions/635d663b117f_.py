"""empty message

Revision ID: 635d663b117f
Revises: 
Create Date: 2021-01-27 14:34:17.526073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '635d663b117f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), server_default='', nullable=False),
    sa.Column('short_desc', sa.String(length=255), server_default='', nullable=False),
    sa.Column('long_desc', sa.Text(), server_default='', nullable=False),
    sa.Column('live_anchor', sa.String(length=150), server_default='', nullable=False),
    sa.Column('github_anchor', sa.String(length=150), server_default='', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('github_anchor'),
    sa.UniqueConstraint('live_anchor'),
    sa.UniqueConstraint('name')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), server_default='', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('login', sa.Unicode(length=50), server_default='', nullable=False),
    sa.Column('password', sa.String(length=255), server_default='', nullable=False),
    sa.Column('active', sa.Boolean(), server_default='0', nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_roles')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('project')
    # ### end Alembic commands ###
