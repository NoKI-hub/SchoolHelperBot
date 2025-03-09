from sqlalchemy import Table, Column, ForeignKey

from db.core.base import Base


user_to_event_table = Table('association', Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('event_id', ForeignKey('events.id'))
)