from telegram import Bot
from phocos import get_latest_status
import json

TOKEN = "TELEGRAM TOKEN"
TELEGRAM_CHAT_ID = -1234   # individual or group

def main():
    bot = Bot(TOKEN)
    # current status and saved status each
    # contain latest and previous - two
    # consecutive periods
    current_status = get_latest_status()

    # if current contains a 'L' (load) and then a 'B' (battery) or vice versa
    # we can immediately send a status has changed alert
    # note: Sep 2022: changed to "Grid" and "Off-grid"

    print(current_status)
    current_value = current_status['latest']['value']
    previous_value = current_status['previous']['value']

    m = ''
    if current_value and previous_value:
        current_time = current_status['latest']['ts'].split(" ")[-1]
        if current_value == 'Off-grid' and previous_value == 'Grid':
            m = f"Switched from ⚡ to 🔋 at or before {current_time}"
        elif current_value == 'Grid' and previous_value == 'Off-grid':
            m = f"Switched from 🔋 to ⚡ at or before {current_time}"
        elif current_value != previous_value:
            m = f"Status change alert. Current status is {current_status['latest']['value']} recorded at {current_status['latest']['ts']}, but previously it was {current_status['previous']['value']} at {current_status['previous']['ts']}"
        else:
            # status hasn't changed, nothing interesting to report
            m = ''

    else:
        m = f"""Missing status info

```
{current_status}
```"""
    if m:
        bot.send_message(TELEGRAM_CHAT_ID, m, parse_mode="markdown")

if __name__ == '__main__':
    main()
