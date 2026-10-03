from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_current_user, get_payment_service
from app.models.user import User
from app.schemas.payment import CreatePaymentRequest, PaymentResponse
from app.services.payment_service import PaymentService

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    request: CreatePaymentRequest,
    user: User = Depends(get_current_user),
    service: PaymentService = Depends(get_payment_service),
):
    return await service.register(request, user)
