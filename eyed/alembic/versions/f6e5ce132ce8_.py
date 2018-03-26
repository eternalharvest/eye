"""empty message

Revision ID: f6e5ce132ce8
Revises: 
Create Date: 2018-03-26 11:49:02.169465

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6e5ce132ce8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('M_BACNET_EMULATION_LOG',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('OBJECT_ID', sa.Integer(), nullable=True),
    sa.Column('INSTACNE_ID', sa.Integer(), nullable=True),
    sa.Column('PROPERTY_ID', sa.Integer(), nullable=True),
    sa.Column('VALUE', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('M_BACNET_EMULATION_OBJECT',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('NAME', sa.String(), nullable=True),
    sa.Column('OBJECT_ID', sa.Integer(), nullable=True),
    sa.Column('INSTACNE_ID', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('M_CONFIG',
    sa.Column('KEY', sa.String(), nullable=False),
    sa.Column('VALUE', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('KEY')
    )
    op.create_table('M_PROXY_POINT',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('DES_DEVICE_ID', sa.Integer(), nullable=True),
    sa.Column('DES_OBJECT_ID', sa.Integer(), nullable=True),
    sa.Column('DES_INSTANCE_ID', sa.Integer(), nullable=True),
    sa.Column('DES_PROPERTY_ID', sa.Integer(), nullable=True),
    sa.Column('SRC_DEVICE_ID', sa.Integer(), nullable=True),
    sa.Column('SRC_OBJECT_ID', sa.Integer(), nullable=True),
    sa.Column('SRC_INSTANCE_ID', sa.Integer(), nullable=True),
    sa.Column('SRC_PROPERTY_ID', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('M_TASK_GROUP',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('NAME', sa.String(), nullable=True),
    sa.Column('INTERVAL', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('M_BACNET_EMULATION_PROPERTY',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('PROPERTY_ID', sa.Integer(), nullable=True),
    sa.Column('EMULATION_POINT_ID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['EMULATION_POINT_ID'], ['M_BACNET_EMULATION_OBJECT.ID'], ),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('M_BACNET_TASK',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('DEVICE_ID', sa.Integer(), nullable=True),
    sa.Column('OBJECT_ID', sa.Integer(), nullable=True),
    sa.Column('INSTANCE_ID', sa.Integer(), nullable=True),
    sa.Column('PROPERTY_ID', sa.Integer(), nullable=True),
    sa.Column('M_TASK_GROUP_ID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['M_TASK_GROUP_ID'], ['M_TASK_GROUP.ID'], ),
    sa.PrimaryKeyConstraint('ID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('M_BACNET_TASK')
    op.drop_table('M_BACNET_EMULATION_PROPERTY')
    op.drop_table('M_TASK_GROUP')
    op.drop_table('M_PROXY_POINT')
    op.drop_table('M_CONFIG')
    op.drop_table('M_BACNET_EMULATION_OBJECT')
    op.drop_table('M_BACNET_EMULATION_LOG')
    # ### end Alembic commands ###