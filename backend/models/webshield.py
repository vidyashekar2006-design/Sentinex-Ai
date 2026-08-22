from pydantic import BaseModel, Field


class WebShieldData(BaseModel):
    suspicious_listings: int = Field(default=0, ge=0)
    price_anomalies: int = Field(default=0, ge=0)
    counterfeit_risks: int = Field(default=0, ge=0)
    supplier_web_alerts: int = Field(default=0, ge=0)