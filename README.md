Concurrent-Pandas
=================


Concurrent Pandas
-------------

**Concurrent Pandas** is a Python Library that allows you to use Pandas and / or Quandl to concurrently download bulk data using threads or processes. What does concurrency do for you? Download your data simultaneously instead of one key at a time, Concurrent Pandas automatically spawns an optimal number of processes or threads based on the number of processes available on your machine. 

Note: Concurrent Pandas is not associated with Quandl or Python Pandas, it just allows you to access them faster. 

---
####Features

- **Working in Python 2 and 3**
- **Sequential Downloading of Keys**
- **Concurrent downloading of keys using thread or process pools**
- **All Concurrent Downloading will automatically pick an optimal number of threads or processes to use for your system**
- **Recursive data structure unpacking for key insertion**
  - Pass one or many:
    - Lists
    - Sets 
    - Deques
    - Any other data structures that inherit from abstract base class *Container* provided it is not also inheriting from Python *basestring* and it allows for iteration.
- **Automatic re-attempts if the download fails or times out**
  - Retries increase the time to try again with each successive failure
- **Variety of data sources supported**
  - Quandl
  - Federal Reserve Economic Data
  - Google Finance
  - Yahoo Finance
  - More coming soon!
- **Data is returned in a hashmap for fast lookups** ( *O(1) average case* )
  - Hash Map Keys are the strings entered for lookup, buckets contain your Panda data frame


---
####Easy to use
```
# Define your keys
yahoo_keys = ["aapl", "xom", "msft", "goog", "brk-b", "TSLA", "IRBT"]
# Instantiate Concurrent Pandas
fast_panda = concurrentpandas.ConcurrentPandas()
# Set your data source
fast_panda.set_source_yahoo_finance()
# Insert your keys
fast_panda.insert_keys(yahoo_keys)
# Choose either asynchronous threads, processes, or a single sequential download
fast_panda.consume_keys_asynchronous_threads()
# The Concurrent Pandas object contains a dict of your results now
mymap = fast_panda.return_map()
# Easily pull the data out of the map for your research
print(mymap["aapl"].head)
```

---
#####Installation Instructions

Note : only tested on Linux

To install execute:

```
pip install ConcurrentPandas
```


---
#####Updates

New in 0.1.2
Ability to interact with stock options

Now requires BeautifulSoup4, and Pandas 0.16 or newer.

---
#####Misc

Tested on Python 2.7.6 and Python 3.4.0 

To see what else I'm building or follow / contact me check out my [github][1], [twitter][3], and my [personal site][2]. 

[1]: https://github.com/briwilcox
[2]: http://brianmwilcox.com/
[3]: https://twitter.com/brian_m_wilcox
