from fastapi import FastAPI
from .database import engine,Base
from app.models.asset import Base
from app.routers import users,assets,auth,portfolios,trades,transactions,holdings,cashtransactions
app = FastAPI()


Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(assets.router)
app.include_router(portfolios.router)
app.include_router(trades.router)
app.include_router(transactions.router)
app.include_router(holdings.router)
app.include_router(cashtransactions.router)
@app.get("/")
def root():
    return {"message": "Stock Tracker API is running."}
