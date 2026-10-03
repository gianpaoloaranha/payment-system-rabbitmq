from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.payment import PaymentStatus


class CreatePaymentRequest(BaseModel):
    # Decimal em vez de float para não perder precisão com valores monetários.
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    amount: Decimal
    status: PaymentStatus
    user_id: UUID
    created_at: datetime
    payed_at: datetime | None
