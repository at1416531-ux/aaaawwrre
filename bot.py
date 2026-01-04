import time
import threading
import ccxt
from flask import Flask

app = Flask(__name__)

# Инициализируем биржи (реальные данные без API ключей для чтения)
binance = ccxt.binance()
bybit = ccxt.bybit()

last_log = "Initializing real-time scanner..."

@app.route('/')
def home():
    return f"EXOCORTEX ΩΣ++++ LIVE MONITORING: {last_log}"

def live_scanner_loop():
    global last_log
    print("ΩΣ++++ LIVE MODE: Scanning Real Market Data...")
    
    symbol = 'ETH/USDT' # Можем менять на BTC/USDT или любой другой
    
    while True:
        try:
            # Получаем реальные тикеры
            b_ticker = binance.fetch_ticker(symbol)
            by_ticker = bybit.fetch_ticker(symbol)
            
            b_price = b_ticker['last']
            by_price = by_ticker['last']
            
            # Считаем разницу
            diff = abs(b_price - by_price)
            spread = (diff / min(b_price, by_price)) * 100
            
            log_entry = f"[{time.strftime('%H:%M:%S')}] {symbol} | Binance: ${b_price} | Bybit: ${by_price} | Spread: {spread:.4f}%"
            last_log = log_entry
            
            # Выводим в консоль Render
            print(log_entry)
            
            # Если спред выше порога (например, 0.1%), выделяем это
            if spread > 0.1:
                print(f"!!! REAL OPPORTUNITY FOUND !!! Profit Gap: ${diff:.2f}")

            time.sleep(10) # Опрос каждые 10 секунд
            
        except Exception as e:
            print(f"Scanner Error: {e}")
            time.sleep(20)

threading.Thread(target=live_scanner_loop, daemon=True).start()

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
