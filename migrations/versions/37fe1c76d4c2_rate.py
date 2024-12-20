"""Rate

Revision ID: 37fe1c76d4c2
Revises: 001
Create Date: 2024-12-14 22:48:57.893383

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '37fe1c76d4c2'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dataset_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dataset_id'], ['data_set.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('webhook')
    with op.batch_alter_table('data_set', schema=None) as batch_op:
        batch_op.add_column(sa.Column('numRatings', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('totalRatings', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('avgRating', sa.Float(), nullable=True))

    with op.batch_alter_table('ds_meta_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ds_meta_data', schema=None) as batch_op:
        batch_op.drop_column('rating')

    with op.batch_alter_table('data_set', schema=None) as batch_op:
        batch_op.drop_column('avgRating')
        batch_op.drop_column('totalRatings')
        batch_op.drop_column('numRatings')

    op.create_table('webhook',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('rate')
    # ### end Alembic commands ###
