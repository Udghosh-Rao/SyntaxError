"""add wallet tables and avatar_url to users

Revision ID: add_wallet_and_avatar
Revises: add_escalation_user_fk
Create Date: 2025-01-01 00:00:00
"""
from alembic import op
import sqlalchemy as sa

revision      = 'add_wallet_and_avatar'
down_revision = 'add_escalation_user_fk'   # ← update to your latest revision
branch_labels = None
depends_on    = None


def upgrade():
    # avatar_url on users
    op.add_column('users', sa.Column('avatar_url', sa.String(500), nullable=True))

    # wallets table
    op.create_table(
        'wallets',
        sa.Column('id',         sa.Integer(),  primary_key=True, autoincrement=True),
        sa.Column('user_id',    sa.Integer(),  sa.ForeignKey('users.id', ondelete='CASCADE'),
                  unique=True, nullable=False),
        sa.Column('balance',    sa.Float(),    nullable=False, server_default='0'),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # wallet_transactions table
    op.create_table(
        'wallet_transactions',
        sa.Column('id',          sa.Integer(),     primary_key=True, autoincrement=True),
        sa.Column('wallet_id',   sa.Integer(),     sa.ForeignKey('wallets.id', ondelete='CASCADE'),
                  nullable=False),
        sa.Column('amount',      sa.Float(),       nullable=False),
        sa.Column('type',        sa.String(30),    nullable=False),
        sa.Column('description', sa.String(200),   nullable=True),
        sa.Column('created_at',  sa.DateTime(),    server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table('wallet_transactions')
    op.drop_table('wallets')
    op.drop_column('users', 'avatar_url')