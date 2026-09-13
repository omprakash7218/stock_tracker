# import streamlit as st
import requests

# st.title("My First Streamlit App")

# name = st.text_input("Enter your name")

# if name:
#     st.write(f"Hello {name} 👋")
# occupation = st.text_input("What do you do for a living? (OCCUPAION)")
# if occupation:
# 	st.write(f"Nice")
# import yfinance as yf
# stockie = (input("What is the name of the stock."))
# stock = yf.Ticker(stockie)

# info = stock.info
# print(info["currentPrice"])
# import requests
# url = "https://official-joke-api.appspot.com/random_joke"
# response = requests.get(url)
# data = response.json()
# print("Here is a random joke for you:")
# print(data["setup"])
# print(data["punchline"])


coin = input("Enter crypto id (bitcoin,ethereum,solana):")
url = "https://api.coingecko.com/api/v3/simple/price"
params = {
    "ids":coin,
    "vs_currencies":"inr"
}
response = requests.get(url,params=params)
data = response.json()
price = data[coin]["inr"]
print(f"The current price of {coin} is Rs.{price}")


# import yfinance as yf

# def get_price_in_inr(ticker_symbol):
#     stock = yf.Ticker(ticker_symbol)
#     # inr_rate = yf.Ticker("INR=X")

#     stock_price_usd = stock.history(period="1d")["Close"].iloc[-1]
#     # usd_inr = inr_rate.history(period="1d")["Close"].iloc[-1]

#     stock_price_inr = stock_price_usd

#     return stock_price_inr

# print(get_price_in_inr("MRF.NS"))
# print(get_price_in_inr("MRF.NS"))


# def sum(a: int, b: int) -> int:
#     results = a + b
#     return str(results)


# a, b = 1, 4
# print(sum(a, b))
# async func vs sync func

# import asyncio
# import time
# def function1():
#     time.sleep(3)
#     print("hello function 1 ")

# def function2():
#     time.sleep(5)
#     print("hello function 2")

# def function3():
#     time.sleep(1)
#     print("hello function 3")


# function1()
# function2()
# function3()

# mypy learnings

# name = "om"
# age = 24
# price = 24.5
# wtf = age + price
# print(wtf)

# a = "20"
# print(a, type(a))

# name: str = "union"
# age: int = 55555
# height: float = 5.69
# student: bool = False


# age = "Nivea men fresh deodrant"


def sum(a: int, b) -> int:
    return a + b


print(sum(1, 2))


user: str | None = "om"

print(user)


