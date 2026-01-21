"""
创建用户表
Revision ID: 001
Revises:
Create Date: 2026-01-20
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """创建用户表"""
    op.create_table(
        't_user',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='用户ID'),
        sa.Column('email', sa.String(length=255), nullable=False, comment='邮箱'),
        sa.Column('hashed_password', sa.String(length=255), nullable=False, comment='密码哈希'),
        sa.Column('nickname', sa.String(length=100), nullable=True, comment='昵称'),
        sa.Column('avatar', sa.String(length=500), nullable=True, comment='头像URL'),
        sa.Column('points', sa.Integer(), nullable=False, server_default='0', comment='积分余额'),
        sa.Column('total_recharged', sa.Integer(), nullable=False, server_default='0', comment='累计充值积分'),
        sa.Column('total_consumed', sa.Integer(), nullable=False, server_default='0', comment='累计消费积分'),
        sa.Column('leetcode_username', sa.String(length=100), nullable=True, comment='LeetCode用户名'),
        sa.Column('ability_score', sa.Integer(), nullable=False, server_default='0', comment='能力评分'),
        sa.Column('status', sa.String(length=1), nullable=False, server_default='1', comment='状态(0禁用 1正常)'),
        sa.Column('role', sa.String(length=20), nullable=False, server_default='user', comment='角色(user/admin)'),
        sa.Column('created_at', sa.DateTime(), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), nullable=False, comment='更新时间'),
        sa.Column('last_login_at', sa.DateTime(), nullable=True, comment='最后登录时间'),
        sa.PrimaryKeyConstraint('id'),
        comment='用户表'
    )
    op.create_index('ix_t_user_id', 't_user', ['id'])
    op.create_index('ix_t_user_email', 't_user', ['email'], unique=True)


def downgrade() -> None:
    """删除用户表"""
    op.drop_index('ix_t_user_email', table_name='t_user')
    op.drop_index('ix_t_user_id', table_name='t_user')
    op.drop_table('t_user')
