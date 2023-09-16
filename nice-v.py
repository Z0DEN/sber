import threading
import sys
import time
#from decimal import Decimal
#from enum import Enum
import yahoo_fin.stock_info as si
import yfinance as yf
from PyQt5.QtWidgets import QGridLayout, QMainWindow, QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLineEdit
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt


class AssetPrice:
    def __init__(self):
        self.popular_assets = si.tickers_dow()[0:10]        #Получаем 10 самых популярных активов 
        self.prices = {}
        self.update_thread = threading.Thread(target=self.update_prices, daemon=True)      # Отдельный поток для обновления цен
        self.update_thread.start()


    def update_prices(self):
        while True:
            for asset in self.popular_assets:
                try:
                    tickers_obj = yf.Tickers(self.popular_assets)  # создаем объект Tickers 
                    self.prices[asset] = round(tickers_obj.tickers[asset].info["currentPrice"], 2)        # Получем цены
                except Exception as e:
                    print(f"Error occurred while getting live price for {asset}")
                    print(f"The error message is: {str(e)}")
            print("обновление цены")
            profile.count_value()


    def get_price(self, ticker):
        price = self.prices.get(ticker.upper(), False)
        if price == False:
            print("Дождитесь обновления цены")
            return False 
        return price


class Profile:
    def __init__(self):
        self.portfolio_balance = 10000
        self.portfolio_value = 0 
        self.portfolio_quantity = [[asset, 0] for asset in ap.popular_assets]

    def count_value(self):
        total = 0
        for asset in self.portfolio_quantity:
            total += asset[1] * ap.prices.get(asset[0])
        self.portfolio_value = total
        self.update_labels()


    def update_labels(self):
        asset, asset_index, quantity, portfolio_quantity, price = self.get_info()
        window.available.setText(f"Доступно {asset}: {portfolio_quantity}")
        window.balance.setText(f"Баланс: {round(self.portfolio_balance, 4)}")
        window.value.setText(f"Стоимость портфолио: {round(self.portfolio_value, 4)}")
    

    def buy(self):
        asset, asset_index, quantity, portfolio_quantity, price = self.get_info()
        if not price:
            return
        if price >= self.portfolio_balance:
            print("Недостаточно средств для совершения транзакции")
            return
        self.portfolio_quantity[asset_index][1] += quantity  # Обновляем количество активов
        self.portfolio_value += price
        self.portfolio_balance -= price
        self.update_labels()
        print(f"Покупка {quantity} {asset} по цене {price}")

    
    def sell(self):
        asset, asset_index, quantity, portfolio_quantity, price = self.get_info()
        if not price:
            return
        if quantity > portfolio_quantity:
            print("Недостаточно активов для совершения транзакции")
            return
        if price >= self.portfolio_value:
            self.portfolio_value = 0
        else:
            self.portfolio_value -= price
        self.portfolio_quantity[asset_index][1] -= quantity  # Обновляем количество активов
        self.portfolio_balance += price
        self.update_labels()
        print(f"Продажа {quantity} {asset} по цене {price}")
    

    def get_info(self):
        asset = window.select.currentText()
        quantity = int(window.text_input.text())
        asset_index = ap.popular_assets.index(asset)
        portfolio_quantity = self.portfolio_quantity[asset_index][1] 
        price = ap.get_price(asset) * quantity
        return asset, asset_index, quantity, portfolio_quantity, price

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trading Training")
        self.setGeometry(100, 100, 800, 500)
            
        """ Widgets """
        self.main_widget = QWidget()
        self.description_widget = QWidget()
        self.button_widget = QWidget()
        self.select_widget = QWidget()
        self.text_input_widget = QWidget()

        """ Layouts """
        self.main_layout = QGridLayout(self.main_widget)
        self.description_layout = QVBoxLayout(self.description_widget)
        self.button_layout = QVBoxLayout(self.button_widget)
        self.select_layout = QVBoxLayout(self.select_widget)
        self.text_input_layout = QVBoxLayout(self.text_input_widget)

        """ Buttons """
        self.buy_button = QPushButton("Купить")
        self.sell_button = QPushButton("Продать")

        self.buy_button.setGeometry(0, 0, 500, 200)
        self.sell_button.setGeometry(0, 0, 500, 200)

        self.button_layout.addWidget(self.buy_button)
        self.button_layout.addWidget(self.sell_button)

        self.buy_button.clicked.connect(profile.buy)
        self.sell_button.clicked.connect(profile.sell)

        """ Select """
        self.select = QComboBox()
        self.select.addItems(ap.popular_assets)
        self.select_layout.addWidget(self.select)

        """ Text field """
        self.text_input = QLineEdit()
        self.text_input.setText("1")
        self.text_input_layout.addWidget(self.text_input)

        """ Text labels """ 
        self.available = QLabel()
        self.balance = QLabel()
        self.value = QLabel()

        self.description_layout.addWidget(self.available)
        self.description_layout.addWidget(self.balance)
        self.description_layout.addWidget(self.value)

        """ Set widgets and layouts """
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self.main_layout.addWidget(self.description_widget, 2, 1, Qt.AlignBottom | Qt.AlignLeft)
        self.main_layout.addWidget(self.button_widget, 2, 2, Qt.AlignBottom | Qt.AlignRight)
        self.main_layout.addWidget(self.select_widget, 2, 3, Qt.AlignBottom | Qt.AlignRight)
        self.main_layout.addWidget(self.text_input_widget, 2, 4, Qt.AlignBottom | Qt.AlignRight)

        """ Fonts """
        font = QFont()
        font.setPointSize(16)
        self.setFont(font)


if __name__ == '__main__':
    ap = AssetPrice()
    profile = Profile()
    print("Запуск приложения")
    app = QApplication(sys.argv)
    window = MainWindow()
    profile.update_labels()
    window.show()
    sys.exit(app.exec())

