"""add_catalog_and_generations_tables

Revision ID: a1b2c3d4e5f6
Revises: 1465b46ba027
Create Date: 2026-02-13 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '1465b46ba027'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    # === 1. Создаём таблицу catalog_items (общий каталог) ===
    op.create_table(
        'catalog_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('id_item', sa.String(length=36), nullable=False),
        sa.Column('uid', sa.String(length=36), nullable=True),
        sa.Column('sid', sa.String(length=36), nullable=True),
        sa.Column('name', sa.String(length=300), nullable=False),
        sa.Column('slug', sa.String(length=200), nullable=False),
        sa.Column('stuff', sa.String(length=100), nullable=True),
        sa.Column('category_id', sa.String(length=36), nullable=True),
        sa.Column('photoUrl', sa.String(length=500), nullable=True),
        sa.Column('image_title', sa.String(length=150), nullable=True),
        sa.Column('raw_description', sa.Text(), nullable=True),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('balance', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id_item')
    )
    op.create_index(op.f('ix_catalog_items_id'), 'catalog_items', ['id'], unique=False)
    op.create_index(op.f('ix_catalog_items_id_item'), 'catalog_items', ['id_item'], unique=True)
    op.create_index(op.f('ix_catalog_items_name'), 'catalog_items', ['name'], unique=False)
    op.create_index(op.f('ix_catalog_items_slug'), 'catalog_items', ['slug'], unique=False)
    
    # === 2. Создаём таблицу user_generations (AI-генерации пользователей) ===
    op.create_table(
        'user_generations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('catalog_item_id', sa.Integer(), nullable=False),
        sa.Column('generation_name', sa.String(length=100), nullable=True),
        sa.Column('ai_description', sa.Text(), nullable=True),
        sa.Column('ai_keywords', sa.Text(), nullable=True),
        sa.Column('ai_prompt_version', sa.String(length=50), nullable=True),
        sa.Column('excel_exported', sa.String(length=20), nullable=True),
        sa.Column('export_count', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['catalog_item_id'], ['catalog_items.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_generations_id'), 'user_generations', ['id'], unique=False)
    op.create_index(op.f('ix_user_generations_user_id'), 'user_generations', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_generations_catalog_item_id'), 'user_generations', ['catalog_item_id'], unique=False)
    
    # === 3. Добавляем user_id в таблицу log ===
    from sqlalchemy import inspect
    
    conn = op.get_bind()
    inspector = inspect(conn)
    log_columns = [col['name'] for col in inspector.get_columns('log')]
    
    if 'user_id' not in log_columns:
        # Используем batch mode для SQLite
        with op.batch_alter_table('log', schema=None) as batch_op:
            batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
            batch_op.create_index('ix_log_user_id', ['user_id'], unique=False)
            batch_op.create_foreign_key('fk_log_user_id', 'users', ['user_id'], ['id'], ondelete='SET NULL')


def downgrade() -> None:
    """Downgrade schema."""
    
    # Откатываем user_id в log (используем batch mode для SQLite)
    with op.batch_alter_table('log', schema=None) as batch_op:
        batch_op.drop_constraint('fk_log_user_id', type_='foreignkey')
        batch_op.drop_index('ix_log_user_id')
        batch_op.drop_column('user_id')
    
    # Удаляем user_generations
    op.drop_index(op.f('ix_user_generations_catalog_item_id'), table_name='user_generations')
    op.drop_index(op.f('ix_user_generations_user_id'), table_name='user_generations')
    op.drop_index(op.f('ix_user_generations_id'), table_name='user_generations')
    op.drop_table('user_generations')
    
    # Удаляем catalog_items
    op.drop_index(op.f('ix_catalog_items_slug'), table_name='catalog_items')
    op.drop_index(op.f('ix_catalog_items_name'), table_name='catalog_items')
    op.drop_index(op.f('ix_catalog_items_id_item'), table_name='catalog_items')
    op.drop_index(op.f('ix_catalog_items_id'), table_name='catalog_items')
    op.drop_table('catalog_items')
