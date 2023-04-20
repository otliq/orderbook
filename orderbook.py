import pandas as pd

def p2p_orderbook():
    # Load bid and ask data into separate pandas dataframes:
    bid_data = get_rates()
    ask_data = get_rates()

    # Sort the bid and ask dataframes by price and quantity:
    bid_data = bid_data.sort_values(['price', 'quantity'], ascending=[True, False])
    ask_data = ask_data.sort_values(['price', 'quantity'], ascending=[False, False])

    # Group the bid and ask dataframes by price and aggregate the quantity:
    bid_data = bid_data.groupby('price').agg({'quantity': 'sum'}).reset_index()
    ask_data = ask_data.groupby('price').agg({'quantity': 'sum'}).reset_index()

    # Rename the columns and add a column for the total quantity:
    bid_data.columns = ['BidP', 'BidQ']
    bid_data['total_bid_quantity'] = bid_data['BidQ'].cumsum()

    ask_data.columns = ['AskP', 'AskQ']
    # ask_data['total_ask_quantity'] = -ask_data['AskQ'].cumsum()
    # Note that we added a negative sign to the total ask quantity column to indicate that it represents the cumulative sum of negative quantities

    # Merge the bid and ask dataframes:
    orderbook = pd.merge(bid_data, ask_data, how='outer', left_on='BidP', right_on='AskP')

    # Fill any missing values with zero:
    orderbook = orderbook.fillna(0)

    # Calculate the spread:
    orderbook['spread'] = orderbook['AskP'] - orderbook['BidP']

    # orderbook = orderbook[
    #     ['total_bid_quantity', 'bid(quantity)', 'bid(price)', 'ask(price)', 'ask(quantity)', 'total_ask_quantity']]

    orderbook = orderbook[
        ['BidQ', 'BidP', 'AskP', 'AskQ', 'spread']]

    df = orderbook.to_string(index=False)
    return df