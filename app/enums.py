from enum import Enum


class TradeType(str,Enum):
	BUY = "buy"
	SELL = "sell"


class TransactionType(str,Enum):
	CREDIT = "credit"
	DEBIT = "debit"
