from config import API_KEY, API_SECRET, TOKEN
import ccxt
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

bybit = ccxt.bybit({
    'apiKey': API_KEY,
    'secret': API_SECRET
    })

bot = Bot(TOKEN)
print(bot)
dp = Dispatcher(bot)

b1 = KeyboardButton('/balance')
b2 = KeyboardButton('/limits')
b3 = KeyboardButton('/close_limits')
b4 = KeyboardButton('/positions')
b5 = KeyboardButton('/close_positions')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client.add(b1).add(b2).insert(b3).add(b4).insert(b5)


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
        await bot.send_message(message.from_user.id, "Бот запущен", reply_markup=kb_client)


@dp.message_handler(commands=['balance'])
async def balance(message: types.Message):
        balance = bybit.fetch_balance()['info']['result']['list']
        for i in balance:
            if float(i['walletBalance']) > 0:
                response = f"{'Баланс: '+round(float(i['walletBalance']), 2)} {i['coin']}"
                await message.answer(response)
        


@dp.message_handler(commands=['limits'])
async def limits(message: types.Message):
    open_limits_orders = bybit.fetch_derivatives_open_orders()
    for i in open_limits_orders:
        data = i['info']
        response = f"{data['symbol']} {data['side']} Quant: {data['qty']}  Price: {round( float(data['price']),2 )}"
        await message.answer(response)
    

@dp.message_handler(commands=['close_limits'])
async def close_position(message: types.Message):
        bybit.cancel_all_orders()


@dp.message_handler(commands=['positions'])
async def position(message: types.Message):
    positions = bybit.fetch_derivatives_positions()
    for i in positions:
        data = i['info'] 
        response = f"{data['symbol']} {data['side']} Quant: {data['size']}"
        await message.answer(response)



@dp.message_handler(commands=['close_positions'])
async def close_position(message: types.Message):
    positions = bybit.fetch_derivatives_positions()
    for i in positions:
        data = i['info']
        symbol = data['symbol']
        side = data['side']
        size = data['size']
        if side == 'Buy':
            side = 'Sell'
        else:
            side = 'Buy'
        order = bybit.create_market_order(symbol, side, size)
        await bot.send_message(message.from_user.id, "Позиции закрыты", reply_markup=kb_client)

executor.start_polling(dp, skip_updates=True)

