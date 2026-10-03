from app.models.payment import Payment
from app.models.user import User
from app.repositories.payment_repository import PaymentRepository
from app.schemas.payment import CreatePaymentRequest


class PaymentService:
    def __init__(self, payments: PaymentRepository):
        self.payments = payments

    async def register(self, request: CreatePaymentRequest, user: User) -> Payment:
        # O pagamento nasce como PENDING; o processamento fica a cargo de um consumer.
        return await self.payments.create(request.amount, user.id)
