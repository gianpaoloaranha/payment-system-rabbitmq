from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment import Payment


class PaymentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, payment_id: UUID) -> Payment | None:
        return await self.session.get(Payment, payment_id)

    async def get_by_user_id(self, user_id: UUID) -> list[Payment]:
        result = await self.session.execute(select(Payment).where(Payment.user_id == user_id))
        return list(result.scalars().all())

    async def create(self, amount: Decimal, user_id: UUID) -> Payment:
        payment = Payment(amount=amount, user_id=user_id)
        self.session.add(payment)
        await self.session.commit()
        await self.session.refresh(payment)
        return payment
