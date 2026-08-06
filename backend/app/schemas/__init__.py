from .auth import UserRegisterSchema, UserLoginSchema, TokenResponseSchema, ForgotPasswordSchema, ResetPasswordSchema
from .user import UserProfileUpdateSchema, UserResponseSchema
from .prediction import LoanPredictionInputSchema, EmiCalculationInputSchema
from .health import ServerHealthSchema, DatabaseHealthSchema, MLHealthSchema

__all__ = [
    "UserRegisterSchema",
    "UserLoginSchema",
    "TokenResponseSchema",
    "ForgotPasswordSchema",
    "ResetPasswordSchema",
    "UserProfileUpdateSchema",
    "UserResponseSchema",
    "LoanPredictionInputSchema",
    "EmiCalculationInputSchema",
    "ServerHealthSchema",
    "DatabaseHealthSchema",
    "MLHealthSchema",
]
