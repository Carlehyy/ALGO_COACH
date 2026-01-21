"""
Alembic迁移 - 创建资源表
Revision ID: 004
Revises: 003
Create Date: 2026-01-20
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """创建资源表"""
    op.create_table(
        't_resource',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='资源ID'),
        sa.Column('type', sa.String(length=20), nullable=False, comment='类型'),
        sa.Column('title', sa.String(length=200), nullable=False, comment='标题'),
        sa.Column('url', sa.String(length=500), nullable=True, comment='原始URL'),
        sa.Column('file_path', sa.String(length=500), nullable=True, comment='MinIO文件路径'),
        sa.Column('file_size', sa.BigInteger(), nullable=True, comment='文件大小'),
        sa.Column('process_status', sa.String(length=20), nullable=False, server_default='pending', comment='处理状态'),
        sa.Column('review_status', sa.String(length=20), nullable=False, server_default='pending', comment='审核状态'),
        sa.Column('uploader_id', sa.Integer(), nullable=False, comment='上传者ID'),
        sa.Column('metadata', sa.Text(), nullable=True, comment='元数据'),
        sa.Column('parse_result', sa.Text(), nullable=True, comment='解析结果'),
        sa.Column('created_at', sa.DateTime(), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), nullable=False, comment='更新时间'),
        sa.Column('processed_at', sa.DateTime(), nullable=True, comment='处理完成时间'),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_t_resource_type'),
        sa.Index('ix_t_resource_uploader_id'),
        comment='资源表'
    )


def downgrade() -> None:
    """删除资源表"""
    op.drop_table('t_resource')
