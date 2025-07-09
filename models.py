from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, index=True)
    trx_address = Column(String, unique=True)
    private_key = Column(String)
    balance = Column(Float, default=0)
    total_earned = Column(Float, default=0)
    trx_per_min = Column(Float, default=0.1)
    last_update = Column(DateTime, default=datetime.utcnow)
    referrals = Column(Integer, default=0)

    boosts = relationship('Boost', back_populates='user')

class Boost(Base):
    __tablename__ = 'boosts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    boost_value = Column(Float)
    expires_at = Column(DateTime)

    user = relationship('User', back_populates='boosts')

class Withdrawal(Base):
    __tablename__ = 'withdrawals'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float)
    address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed = Column(Boolean, default=False)
