from datetime import datetime
from sqlalchemy.orm import Session
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from models import User, Boost

scheduler = AsyncIOScheduler()


def update_balances(db: Session):
    users = db.query(User).all()
    now = datetime.utcnow()
    for user in users:
        elapsed = (now - user.last_update).total_seconds() / 60
        income = elapsed * user.trx_per_min
        for boost in user.boosts:
            if boost.expires_at > now:
                income += elapsed * boost.boost_value
        user.balance += income
        user.total_earned += income
        user.last_update = now
    db.commit()


def start(db: Session):
    scheduler.add_job(update_balances, 'interval', minutes=1, args=[db])
    scheduler.start()
