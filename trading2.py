import yahoo_fin.stock_info as si
import yfinance as yf
import time
import warnings
from decimal import Decimal
from enum import Enum
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLineEdit

#warnings.simplefilter(action='ignore', category=FutureWarning)

class AssetPrice:
    def __init__(self):
        self.popular_assets = si.tickers_dow()[0:10] 
        self.prices = {}

    def update_prices(self):
        for asset in self.popular_assets:
            try:
                tickers = yf.Tickers(self.popular_assets)  # создаем объект Tickers
                self.prices[asset] = tickers.tickers[asset].info["currentPrice"] 
                print(f"Current price of {asset} is {self.prices[asset]}")
            except Exception as e:
                print(f"Error occurred while getting live price for {asset}")
                print(f"The error message is: {str(e)}")


    def get_price(self, ticker):
        return self.prices.get(ticker)




class Portfolio:
    def __init__(self):

        self.balance = Decimal(64053)  # Баланс на счёте.

    def buy(self, asset, quantity):
        """Выполняет транзакцию покупки актива."""
        cost = asset.value * quantity
        if self.balance < cost:
            print("Недостаточно средств для транзакции покупки!")
            return
        self.balance -= cost
        self.assets[asset] += quantity
        print(f"Покупка {asset.name}: {quantity} шт. за {cost} руб.")

    def sell(self, asset, quantity):
        """Выполняет транзакцию продажи актива."""
        if self.assets[asset] < quantity:
            print("Недостаточно активов для транзакции продажи!")
            return
        self.balance += asset.value * quantity
        self.assets[asset] -= quantity
        print(f"Продажа {asset.name}: {quantity} шт. за {asset.value * quantity} руб.")

    def portfolio_value(self):
        """Вычисляет текущую стоимость портфеля."""
        total_value = self.balance
        for asset, quantity in self.assets.items():
            total_value += asset.value * quantity
        return total_value


if __name__ == '__main__':

    portfolio = Portfolio()
    ap = AssetPrice()
    ap.update_prices()  # обновляем данные
    for ticker in ap.popular_assets:
        price = ap.get_price(ticker)  # получаем цену для текущего тикера
        if price:
            print(ticker, ":", price)
