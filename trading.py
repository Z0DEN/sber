import yahoo_fin.stock_info as si
import time
import warnings
from decimal import Decimal
from enum import Enum
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLineEdit

warnings.simplefilter(action='ignore', category=FutureWarning)

class AssetPrice:
    def __init__(self):
        self.dow_list = si.tickers_dow()[0:10]
        self.prices = {}

    def update_prices(self):
        for ticker in self.dow_list:
            try:
                self.prices[ticker] = si.get_live_price(ticker)
            except Exception:
                print(f"Error occurred while getting live price for {ticker}")

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


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Trading'
        self.left = 10
        self.top = 10
        self.width = 350
        self.height = 250
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Создание виджетов GUI
        bal_lbl = QLabel(f"Баланс: {portfolio.balance}", self, objectName="bal_lbl")
        val_lbl = QLabel(f"Текущая стоимость портфеля: {portfolio.portfolio_value()}", self, objectName="val_lbl")

        buy_button = QPushButton('Покупка', self)
        buy_button.clicked.connect(self.buy)

        sell_button = QPushButton('Продажа', self)
        sell_button.clicked.connect(self.sell)

        self.asset_combo = QComboBox(self)
        self.asset_combo.addItem(AssetPrice.LKOH.name)
        self.asset_combo.addItem(AssetPrice.SBER.name)
        self.asset_combo.addItem(AssetPrice.GAZP.name)
        self.asset_combo.addItem(AssetPrice.ROSN.name)
        self.asset_combo.addItem(AssetPrice.MGNT.name)
        self.asset_combo.addItem(AssetPrice.YNDX.name)

        self.quantity_edit = QLineEdit(self)
        self.quantity_edit.setPlaceholderText("Количество")

        # Создание горизонтальных и вертикальных контейнеров
        hbox1 = QHBoxLayout()
        hbox1.addWidget(bal_lbl)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(val_lbl)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.asset_combo)
        hbox3.addWidget(self.quantity_edit)
        hbox4 = QHBoxLayout()
        hbox4.addWidget(buy_button)
        hbox4.addWidget(sell_button)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)

        self.setLayout(vbox)
        self.show()

    def buy(self):
        asset = AssetPrice[self.asset_combo.currentText()]
        quantity = int(self.quantity_edit.text())
        portfolio.buy(asset, quantity)
        self.update_labels()

    def sell(self):
        asset = AssetPrice[self.asset_combo.currentText()]
        quantity = int(self.quantity_edit.text())
        portfolio.sell(asset, quantity)
        self.update_labels()

    def update_labels(self):
        bal_lbl = self.findChild(QLabel, "bal_lbl")
        bal_lbl.setText(f"Баланс: {portfolio.balance}")
        val_lbl = self.findChild(QLabel, "val_lbl")
        val_lbl.setText(f"Текущая стоимость портфеля: {portfolio.portfolio_value()}")


if __name__ == '__main__':
    portfolio = Portfolio()
    ap = AssetPrice()
    print(ap.dow_list)
    for ticker in ap.dow_list:
        ap.update_prices()  # обновляем данные
        price = ap.get_price(ticker)  # получаем цену для текущего тикера
        if price:
           print(price)
    
#    app = QApplication(sys.argv)
#    ex = App()
#    sys.exit(app.exec_())
