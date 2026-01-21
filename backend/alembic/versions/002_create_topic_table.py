"""
创建知识点表
Revision ID: 002
Revises: 001
Create Date: 2026-01-20
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """创建知识点表"""
    op.create_table(
        't_topic',
        sa.Column('id', sa.String(length=100), nullable=False, comment='知识点ID'),
        sa.Column('name', sa.String(length=100), nullable=False, comment='名称'),
        sa.Column('name_en', sa.String(length=100), nullable=False, comment='英文名'),
        sa.Column('category', sa.String(length=50), nullable=False, comment='分类'),
        sa.Column('difficulty', sa.Integer(), nullable=False, server_default='1', comment='难度(1-5)'),
        sa.Column('importance', sa.Integer(), nullable=False, server_default='1', comment='重要性(1-5)'),
        sa.Column('prerequisites', sa.JSON(), nullable=True, comment='前置知识点ID列表'),
        sa.Column('related', sa.JSON(), nullable=True, comment='相关知识点ID列表'),
        sa.Column('description', sa.Text(), nullable=True, comment='描述'),
        sa.Column('estimated_hours', sa.Integer(), nullable=False, server_default='0', comment='预计学习时长(小时)'),
        sa.Column('status', sa.String(length=1), nullable=False, server_default='1', comment='状态(0禁用 1正常)'),
        sa.Column('created_at', sa.String(length=50), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.String(length=50), nullable=False, comment='更新时间'),
        sa.PrimaryKeyConstraint('id'),
        comment='知识点表'
    )
    op.create_index('ix_t_topic_category', 't_topic', ['category'])


def downgrade() -> None:
    """删除知识点表"""
    op.drop_index('ix_t_topic_category', table_name='t_topic')
    op.drop_table('t_topic')
