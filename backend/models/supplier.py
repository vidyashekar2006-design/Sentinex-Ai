from pydantic import BaseModel, Field


class Supplier(BaseModel):
    name: str
    risk: float = Field(ge=0, le=100)
    status: str
    delivery_delay: float = Field(ge=0)
    price_change: float
    sentiment_score: float = Field(ge=0, le=1)
    disruption_history: float = Field(ge=0, le=1)