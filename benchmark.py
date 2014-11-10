__author__ = 'brian'
"""
Output in test run:

Looking up 10 keys from Google Finance

Time to download 10 stocks from Google with Multi-Threading : 6.987292528152466 seconds.

Looking up 10 keys from Google Finance

Time to download 10 stocks from Google with Multi Processing : 6.1684489250183105 seconds.

Looking up 10 keys from Google Finance

Time to download 10 stocks from Google with Single Threading : 7.67667818069458 seconds.

Process finished with exit code 0

"""
import concurrentpandas
import time


# Define your keys
finance_keys = ["aapl", "xom", "msft", "goog", "brk-b", "TSLA", "IRBT", "VTI", "VT", "VNQ"]
# Instantiate Concurrent Pandas
fast_panda = concurrentpandas.ConcurrentPandas()
# Set your data source
fast_panda.set_source_google_finance()

# Insert your keys
fast_panda.insert_keys(finance_keys)
# Choose either asynchronous threads, processes, or a single sequential download
pre = time.time()
fast_panda.consume_keys_asynchronous_threads()
post = time.time()
print("Time to download 10 stocks from Google with Multi-Threading : " + (post - pre).__str__() + " seconds.")

# Insert your keys
fast_panda.insert_keys(finance_keys)
# Choose either asynchronous threads, processes, or a single sequential download
pre = time.time()
fast_panda.consume_keys_asynchronous_processes()
post = time.time()
print("Time to download 10 stocks from Google with Multi Processing : " + (post - pre).__str__() + " seconds.")

# Insert your keys
fast_panda.insert_keys(finance_keys)
# Choose either asynchronous threads, processes, or a single sequential download
pre = time.time()
fast_panda.consume_keys()
post = time.time()
print("Time to download 10 stocks from Google with Single Threading : " + (post - pre).__str__() + " seconds.")