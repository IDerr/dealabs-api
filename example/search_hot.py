from dealabs import Dealabs
import json
import sys
dealabs = Dealabs()

deals = dealabs.search_deals(
    params={
        "order_by": "hot",
        "query": "1070"
    }
)

for deal in deals["data"]:
    embed = discord.Embed(title=deal["title_formatted"], description="Desc", color=0x00ff00)
    embed.add_field(name="Price", value=deal["price"], inline=False)
    embed.add_field(name="HOT", value=deal["temperature_rating"], inline=False)
    await client.send_message(message.channel, embed=embed)
    print(deal)
    sys.exit(0)