from settings import deposit
async def market_order(session,symbol,side,close_price):
    qty_p, limit_p = getPrecision(symbol, session)
    qty = round(deposit / close_price[-1], qty_p)
    market_order = session.place_order(
        category="linear",
        symbol=symbol,
        side=side,
        orderType="Market",
        qty=qty,
        timeInForce="PostOnly",
        orderFilter="Order",
    )
    print(market_order)


def getPrecision(symbol,session):
    response = session.get_instruments_info(
        category="linear",  # or "spot", "inverse", "option" depending on your requirement
        symbol=symbol  # specify the trading pair
    )
    priceFilter = response['result']['list'][0]['priceFilter']
    lotSizeFilter = response['result']['list'][0]['lotSizeFilter']
    tickSize = priceFilter['tickSize']
    qtyStep = lotSizeFilter['qtyStep']
    if tickSize.startswith("0."):
        tickSize = tickSize.replace("0.", "")
    else:
        tickSize = str(float(tickSize))

    if qtyStep.startswith("0."):
        qtyStep = qtyStep.replace("0.", "")

    else:
        qtyStep = str(float(qtyStep))

    return int(len(qtyStep)),int(len(tickSize))