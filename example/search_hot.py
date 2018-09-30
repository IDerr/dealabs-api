from dealabs import Dealabs

dealabs = Dealabs()

deals = dealabs.get_deals_hot(params={})

for deal in deals["data"]:
    print(deal)