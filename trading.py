import threading
import sys
import time
import yahoo_fin.stock_info as si
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QGridLayout, QMainWindow, QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLineEdit
from PyQt5.QtGui import QPainter, QColor, QFont, QFontDatabase
from PyQt5.QtCore import Qt


class AssetPrice:
    def __init__(self):
        self.popular_symbols = si.tickers_dow()[0:10]        #Получаем 10 самых популярных активов 
        self.prices = {}
        self.flag = False
        self.temp = 0
        self.i = 0
        self.update_thread = threading.Thread(target=self.run, daemon=True)      # Отдельный поток для обновления цен
        self.update_thread.start()
        self.start_time = time.time()


    def run(self):
        while True:
            if self.flag:
                self.update_prices_1()
                profile.update_chart()
            else:
                self.update_prices_2()
                window.buy_button.setEnabled(True)
                window.sell_button.setEnabled(True)
            profile.count_portfolio_value()


    def update_prices_1(self):
        symbol, symbol_index, quantity, portfolio_quantity, price = profile.get_info() 
        tickers_obj = yf.Tickers(symbol)     # создаем объект Tickers 
        self.prices[symbol] = round(tickers_obj.tickers[symbol].info["currentPrice"], 2)        # Получем цены для выбранного в select symbol
        print(f" symbol: {symbol},tickers_obj: {tickers_obj},price: {self.prices[symbol]}")


    def update_prices_2(self):
        for symbol in self.popular_symbols:
            try:
                tickers_obj = yf.Tickers(self.popular_symbols)  
                self.prices[symbol] = round(tickers_obj.tickers[symbol].info["currentPrice"], 2)     # Получем цены для каждого symbol в popular_symbols
                self.flag = True
            except Exception as e:
                print(f"Error occurred while getting live price for {symbol}")
                print(f"The error message is: {str(e)}")
        print("Обновление цен завершено")


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
        self.portfolio_quantity = [[symbol, 0] for symbol in ap.popular_symbols]
        self.chart_data = {}
        self.time_data= {}

    def buy(self):
        symbol, symbol_index, quantity, portfolio_quantity, price = self.get_info()
        if not price:
            return
        if price >= self.portfolio_balance:
            print("Недостаточно средств для совершения транзакции")
            return
        self.portfolio_quantity[symbol_index][1] += quantity  # Обновляем количество активов
        self.portfolio_value += price
        self.portfolio_balance -= price
        self.update_labels()
        print(f"Покупка {quantity} {symbol} по цене {price}")

    
    def sell(self):
        symbol, symbol_index, quantity, portfolio_quantity, price = self.get_info()
        if not price:
            return
        if quantity > portfolio_quantity:
            print("Недостаточно активов для совершения транзакции")
            return
        if price >= self.portfolio_value:
            self.portfolio_value = 0
        else:
            self.portfolio_value -= price
        self.portfolio_quantity[symbol_index][1] -= quantity  # Обновляем количество активов
        self.portfolio_balance += price
        self.update_labels()
        print(f"Продажа {quantity} {symbol} по цене {price}")
    

    def get_info(self):
        try:
            quantity = int(window.text_input.text())
        except ValueError:
            print("Некорректное значение количества активов")
            quantity = 0

        symbol = window.select.currentText()
        symbol_index = ap.popular_symbols.index(symbol)
        portfolio_quantity = self.portfolio_quantity[symbol_index][1]
        price = ap.get_price(symbol) * quantity
        return symbol, symbol_index, quantity, portfolio_quantity, price


    def count_portfolio_value(self):
        total = 0
        for symbol in self.portfolio_quantity:
            total += symbol[1] * ap.prices.get(symbol[0])
        self.portfolio_value = total
        self.update_labels()


    def update_labels(self):
        symbol, _, _, portfolio_quantity, _ = self.get_info()
        window.available.setText(f"Доступно {symbol}: {portfolio_quantity}")
        window.balance.setText(f"Баланс: {round(self.portfolio_balance, 4)}")
        window.value.setText(f"Стоимость портфолио: {round(self.portfolio_value, 4)}")
    
    
    def update_chart(self):
        symbol = window.select.currentText()
        price = ap.get_price(symbol)
        check_dir = True 

        if symbol not in self.chart_data:
            self.chart_data[symbol] = []

        self.chart_data[symbol].append(price)
        symbol_prices = self.chart_data[symbol]
        try:
            last_value = self.chart_data[symbol][-1]
            second_last_value = self.chart_data[symbol][-2]
            if last_value < second_last_value:
                check_dir = False        # Вниз
        except:
            chart.update_chart(range(len(symbol_prices)), symbol_prices, check_dir)
        chart.update_chart(range(len(symbol_prices)), symbol_prices, check_dir)


class ChartWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.figure = plt.figure()  # Create a new figure
        self.canvas = FigureCanvasQTAgg(self.figure)  # Create a canvas for the figure
        self.axes = self.figure.add_subplot(111)  # Add subplot to the figure
        
        chart_layout = QVBoxLayout()
        chart_layout.addWidget(self.canvas)
        self.setLayout(chart_layout)

    def clear_chart(self):
        self.axes.clear()

    def update_chart(self, x_data, y_data, check_dir):
        if check_dir:
            self.axes.plot(x_data, y_data, linestyle='-', color='green')
        else:
            self.axes.plot(x_data, y_data, linestyle='-', color='red')

        self.axes.set_xlabel('Timestamp')
        self.axes.set_ylabel('Price')
        self.canvas.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trading Training")
        self.setGeometry(100, 100, 1200, 800)
            
        """ Widgets """
        self.main_widget = QWidget()
        self.description_widget = QWidget()
        self.button_widget = QWidget()

        """ Layouts """
        self.main_layout = QGridLayout(self.main_widget)
        self.description_layout = QVBoxLayout(self.description_widget)
        self.button_layout = QVBoxLayout(self.button_widget)

        """ Buttons """
        self.buy_button = QPushButton("Купить")
        self.sell_button = QPushButton("Продать")
        self.buy_button.setEnabled(False)
        self.sell_button.setEnabled(False)

        self.buy_button.setFixedSize(200, 50)
        self.sell_button.setFixedSize(200, 50)

        self.button_layout.addWidget(self.buy_button)
        self.button_layout.addWidget(self.sell_button)

        self.buy_button.clicked.connect(profile.buy)
        self.sell_button.clicked.connect(profile.sell)

        """ Select """
        self.select = QComboBox()
        self.select.addItems(ap.popular_symbols)
        self.select.setFixedSize(100, 50)
        self.select.currentIndexChanged.connect(chart.clear_chart)

        """ Text field """
        self.text_input = QLineEdit()
        self.text_input.setText("1")
        self.text_input.setFixedSize(100, 50)

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
        self.main_layout.addWidget(self.button_widget, 2, 2, Qt.AlignCenter)
        self.main_layout.addWidget(self.select, 2, 3)
        self.main_layout.addWidget(self.text_input, 2, 4)
        self.main_layout.addWidget(chart.canvas, 1, 1, 1, 4)

        """ Fonts """
        font = QFont()
        font.setPointSize(16)
        self.setFont(font)


if __name__ == '__main__':
    ap = AssetPrice()
    profile = Profile()
    print("Запуск приложения")
    app = QApplication(sys.argv)
    chart = ChartWidget()
    window = MainWindow()
    profile.update_labels()
    window.show()
    sys.exit(app.exec())
