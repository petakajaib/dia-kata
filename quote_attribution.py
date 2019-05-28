from time import sleep
from quote_attribution_pipeline import quote_attribution

while True:
    quote_attribution()
    print("sleep for a few hour")
    sleep(3600*12)
