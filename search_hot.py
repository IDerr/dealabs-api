from dealabs import Dealabs
import json
import sys
dealabs = Dealabs()

deals = dealabs.get_new_deals()
print(deals)