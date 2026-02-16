"""add_user_id_to_items

Revision ID: 1465b46ba027
Revises: bd8e54574c26
Create Date: 2026-02-12 06:18:04.604869

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1465b46ba027'
down_revision: Union[str, Sequence[str], None] = 'bd8e54574c26'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    from sqlalchemy import inspect
    from alembic import context
    
    # Проверяем, существует ли уже колонка
    conn = op.get_bind()
    inspector = inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('item')]
    
    if 'user_id' not in columns:
        # Добавляем колонку только если её нет
        with op.batch_alter_table('item', schema=None) as batch_op:
            batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
    
    # Заполняем существующие записи (назначаем первому администратору)
    op.execute("UPDATE item SET user_id = 1 WHERE user_id IS NULL")
    
    # Проверяем индексы и constraints
    indexes = [idx['name'] for idx in inspector.get_indexes('item')]
    foreign_keys = [fk['name'] for fk in inspector.get_foreign_keys('item')]
    
    with op.batch_alter_table('item', schema=None) as batch_op:
        # Делаем колонку NOT NULL
        batch_op.alter_column('user_id', nullable=False)
        
        # Создаём индекс если его нет
        if 'ix_item_user_id' not in indexes:
            batch_op.create_index('ix_item_user_id', ['user_id'], unique=False)
        
        # Создаём foreign key если его нет
        if 'fk_item_user_id' not in foreign_keys:
            batch_op.create_foreign_key('fk_item_user_id', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.drop_constraint('fk_item_user_id', type_='foreignkey')
        batch_op.drop_index('ix_item_user_id')
        batch_op.drop_column('user_id')
