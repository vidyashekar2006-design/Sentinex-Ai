from pydantic import BaseModel, Field


class MarketData(BaseModel):
    component_price_change: float = Field(default=0.0)
    demand_change: float = Field(default=0.0)
    supply_pressure: float = Field(default=0.0)
    market_anomalies: int = Field(default=0, ge=0)