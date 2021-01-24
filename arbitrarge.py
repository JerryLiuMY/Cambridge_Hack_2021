
def hedge (amount):
    if amount < 0:
        # bid from a
        book_a = e.get_last_price_book(a_id)
        book_b = e.get_last_price_book(b_id)    
        ask_a_price_0 = book_a.asks[0].price
        bid_result = e.insert_order(a_id, price=ask_a_price_0, volume=int(-amount), side='bid', order_type='ioc')
    if amount > 0:
        # bid from a
        book_a = e.get_last_price_book(a_id)
        book_b = e.get_last_price_book(b_id)    
        bid_a_price_0 = book_a.bids[0].price
        ask_result = e.insert_order(a_id, price=bid_a_price_0, volume=int(amount), side='ask', order_type='ioc')
while True:
    positions = e.get_positions()
    sum = positions[a_id] + positions[b_id]
    print(positions[a_id], positions[b_id])
    time.sleep(2.0)
    positions = e.get_positions()
    if sum > 30 or sum < -30:
        hedge (sum // 2)
        print ("hedging...")
    else:
        book_a = e.get_last_price_book(a_id)
        book_b = e.get_last_price_book(b_id)
        bid_b_price_0 = book_b.bids[0].price
        ask_b_price_0 = book_b.asks[0].price
        ask_result = e.insert_order(b_id, price=ask_b_price_0, volume=10, side='ask', order_type='limit')
        bid_result = e.insert_order(b_id, price=bid_b_price_0, volume=10, side='bid', order_type='limit')
        print ("market making...")
    # step 2: check position (before step 1), if b's position > 30, decide hedge
    
# # step 3: hedge? neutralize in A. 

# # (outstanding order <= 800). withdraw, ..
# positions = e.get_positions()
# print(positions[a_id], positions[b_id])


#main
it = 0

while (True):
    if it % 1000 == 0:
        print ("part", it/1000, '...')
        positions = e.get_positions()
        print(positions[a_id], positions[b_id])
    it += 1
    time.sleep(0.002)
    positions = e.get_positions()
    
    book_a = e.get_last_price_book(a_id)
    book_b = e.get_last_price_book(b_id)
    trade, bid_id, ask_id, bid_price, ask_price, bid_volume, ask_volume = check_trade(book_a, book_b)
#     print(bid_price, ask_price)
    
    if trade == None:
        time.sleep(0.008)
        # print("Done nothing")
        continue 
    
     # decide price and volume
#     if bid_price == ask_price:
# #         print("special_deal!")
#         bid_price += 0.005
#         ask_price -= 0.005
#         Volume = 5
#     else:
# #         print("normal_deal!")
#         bid_price -= 0.001
#         ask_price += 0.001
    av = (ask_price + bid_price) * 0.5
    bid_price = av
    ask_price = av
    Volume = min(1, min (bid_volume, ask_volume))
        
    ask_initial = positions[ask_id]
    bid_initial = positions[bid_id]
#     print("almost done deal")
    if ask_initial - Volume <= -1:
        continue 
    if bid_initial + Volume >= 1:
        continue
        
    if trade == True:
#         print("have a deal")
        if ask_id == b_id: 
            # sell in b
            ask_result = e.insert_order(b_id, price=bid_price, volume=Volume, side='ask', order_type='limit')
            bid_result = e.insert_order(a_id, price=ask_price, volume=Volume, side='bid', order_type='limit')
#             print(f"Firs t Trade Order Id: {ask_result}", "ask ", bid_price, Volume)
#             print(f"Second Trade Order Id: {bid_result}", "bid ", ask_price, Volume)
            print("earned: ", (bid_price - ask_price) * Volume)
        if bid_id == b_id: 
            bid_result = e.insert_order(b_id, price=ask_price, volume=Volume, side='bid', order_type='limit')
            ask_result = e.insert_order(a_id, price=bid_price, volume=Volume, side='ask', order_type='limit')
#             print(f"F irst Trade Order Id: {bid_result}", "bid ", ask_price, Volume)
#             print(f"Second Trade Order Id: {ask_result}", "ask ", bid_price, Volume)
            print("earned: ", (bid_price - ask_price) * Volume)
        positions = e.get_positions()
        print(positions[a_id], positions[b_id])
#         break 
#     time.sleep(1)
    