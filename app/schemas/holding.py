from pydantic import BaseModel


class HoldingCreate(BaseModel):
    id: int
    portfolio_id: int
    symbol: str
    quantity: int
    average_buy_price: float
