"""
创建积分相关表
Revision ID: 003
Revises: 002
Create Date: 2026-01-20
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """创建积分相关表"""

    # 创建积分套餐表
    op.create_table(
        't_package',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='套餐ID'),
        sa.Column('name', sa.String(length=100), nullable=False, comment='套餐名称'),
        sa.Column('price', sa.BigInteger(), nullable=False, comment='价格(分)'),
        sa.Column('points', sa.Integer(), nullable=False, comment='积分数量'),
        sa.Column('bonus_points', sa.Integer(), nullable=False, server_default='0', comment='赠送积分'),
        sa.Column('description', sa.String(length=500), nullable=True, comment='描述'),
        sa.Column('status', sa.String(length=1), nullable=False, server_default='1', comment='状态'),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0', comment='排序'),
        sa.PrimaryKeyConstraint('id'),
        comment='积分套餐表'
    )

    # 创建充值订单表
    op.create_table(
        't_order',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='订单ID'),
        sa.Column('order_no', sa.String(length=50), nullable=False, comment='订单号'),
        sa.Column('user_id', sa.Integer(), nullable=False, comment='用户ID'),
        sa.Column('package_id', sa.Integer(), nullable=False, comment='套餐ID'),
        sa.Column('amount', sa.BigInteger(), nullable=False, comment='金额(分)'),
        sa.Column('points', sa.Integer(), nullable=False, comment='积分数量'),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='pending', comment='状态'),
        sa.Column('pay_channel', sa.String(length=50), nullable=True, comment='支付渠道'),
        sa.Column('paid_at', sa.DateTime(), nullable=True, comment='支付时间'),
        sa.Column('created_at', sa.DateTime(), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), nullable=False, comment='更新时间'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('order_no', name='uq_order_no'),
        comment='充值订单表'
    )
    op.create_index('ix_t_order_order_no', 't_order', ['order_no'])
    op.create_index('ix_t_order_user_id', 't_order', ['user_id'])

    # 创建积分流水表
    op.create_table(
        't_point_log',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='流水ID'),
        sa.Column('user_id', sa.Integer(), nullable=False, comment='用户ID'),
        sa.Column('type', sa.String(length=20), nullable=False, comment='类型'),
        sa.Column('amount', sa.Integer(), nullable=False, comment='变动数量'),
        sa.Column('balance', sa.Integer(), nullable=False, comment='变动后余额'),
        sa.Column('reason', sa.String(length=200), nullable=True, comment='变动原因'),
        sa.Column('related_id', sa.String(length=100), nullable=True, comment='关联ID'),
        sa.Column('created_at', sa.DateTime(), nullable=False, comment='创建时间'),
        sa.PrimaryKeyConstraint('id'),
        comment='积分流水表'
    )
    op.create_index('ix_t_point_log_user_id', 't_point_log', ['user_id'])


def downgrade() -> None:
    """删除积分相关表"""
    op.drop_index('ix_t_point_log_user_id', table_name='t_point_log')
    op.drop_table('t_point_log')
    op.drop_index('ix_t_order_user_id', table_name='t_order')
    op.drop_index('ix_t_order_order_no', table_name='t_order')
    op.drop_table('t_order')
    op.drop_table('t_package')
