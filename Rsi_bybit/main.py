from pybit.unified_trading import HTTP
from config import api_key,api_secret
from settings import symbol,kline_time,rsi_len,rsi_low,rsi_high,deposit
import asyncio
import talib
import numpy as np
from orders import market_order,getPrecision


session = HTTP(testnet=True,api_key=api_key,api_secret=api_secret)


async def run():
    last_signal = None
    while True:
        close_price = []

        response = session.get_kline(
            category="linear",
            symbol=symbol,
            interval=kline_time,
            limit=1000
        )
        klines = response.get('result', {}).get('list', [])
        klines = sorted(klines, key=lambda x: int(x[0]))

        for candle in klines:
            close_price_for_list = float(candle[4])
            close_price.append(close_price_for_list)

        close_price = np.array(close_price, dtype='float')

        rsi_value = talib.RSI(close_price, timeperiod=rsi_len)[-1]
        print(f"RSI: {round(rsi_value,2)}")

        if rsi_value < rsi_low and last_signal != "Buy":
            """BUY"""
            await market_order(session,symbol,"Buy",close_price)
            last_signal = "Buy"
        elif rsi_value > rsi_high and last_signal != "Sell":
            """SELL"""
            await market_order(session,symbol,"Sell",close_price)
            last_signal = "Sell"



        await asyncio.sleep(60)


if __name__ == '__main__':
    asyncio.run(run())

