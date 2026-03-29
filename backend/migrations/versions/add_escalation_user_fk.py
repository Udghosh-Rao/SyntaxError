"""add user_id fk to escalation_tickets

Revision ID: add_escalation_user_fk
Revises: add_referral_system
Create Date: 2025-01-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision      = 'add_escalation_user_fk'
down_revision = 'add_referral_system'   # ← set to your latest migration ID
branch_labels = None
depends_on    = None


def upgrade():
    op.add_column('escalation_tickets',
        sa.Column('user_id', sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        'fk_escalation_tickets_user_id',
        'escalation_tickets', 'users',
        ['user_id'], ['id'],
        ondelete='SET NULL'
    )


def downgrade():
    op.drop_constraint('fk_escalation_tickets_user_id', 'escalation_tickets', type_='foreignkey')
    op.drop_column('escalation_tickets', 'user_id')
