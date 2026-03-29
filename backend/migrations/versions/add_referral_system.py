"""add referral columns to users

Revision ID: add_referral_system
Revises: 338117e8a6f7
Create Date: 2025-01-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = 'add_referral_system'
down_revision = '338117e8a6f7'   # ← set to your latest migration ID
branch_labels = None
depends_on = None


def upgrade():
    # Add referral_code — unique per user, generated on registration
    op.add_column('users',
        sa.Column('referral_code', sa.String(20), nullable=True)
    )
    op.create_unique_constraint('uq_users_referral_code', 'users', ['referral_code'])

    # Add referred_by_id — FK to the user who referred this user
    op.add_column('users',
        sa.Column('referred_by_id', sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        'fk_users_referred_by_id',
        'users', 'users',
        ['referred_by_id'], ['id'],
        ondelete='SET NULL'
    )

    # Back-fill a referral code for every existing user
    op.execute("""
        UPDATE users
        SET referral_code = CONCAT('LS-', UPPER(SUBSTRING(MD5(RAND()), 1, 8)))
        WHERE referral_code IS NULL
    """)

    # Now make it non-nullable
    op.alter_column('users', 'referral_code', nullable=False)


def downgrade():
    op.drop_constraint('fk_users_referred_by_id', 'users', type_='foreignkey')
    op.drop_column('users', 'referred_by_id')
    op.drop_constraint('uq_users_referral_code', 'users', type_='unique')
    op.drop_column('users', 'referral_code')
