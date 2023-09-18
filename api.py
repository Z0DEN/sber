from binance.client import Client

# Введите ваш API-ключ и секретный ключ
api_key = 'ВАШ_API_КЛЮЧ'
api_secret = 'ВАШ_СЕКРЕТНЫЙ_КЛЮЧ'

# Создайте экземпляр клиента Binance API
client = Client(api_key, api_secret)

# Получите цену для выбранного актива
symbol = 'BTCUSDT'  # Замените на символ своего актива
ticker = client.get_symbol_ticker(symbol=symbol)

# Выведите цену
print(f'Цена {symbol}: {ticker["price"]}')

