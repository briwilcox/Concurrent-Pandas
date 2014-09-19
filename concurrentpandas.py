__author__ = 'brian wilcox'
import Quandl
import collections
import time
import sys
import pandas.io.data
from random import randrange
import multiprocessing
from multiprocessing import Process, Manager
from multiprocessing.pool import ThreadPool


def data_worker(**kwargs):
    """
    Function to be spawned concurrently,
    consume data keys from input queue, and push the resulting dataframes to output map
    """
    if kwargs is not None:
        if "function" in kwargs:
            function = kwargs["function"]
        else:
            Exception("Invalid arguments, no function specified")
        if "input" in kwargs:
            input_queue = kwargs["input"]
        else:
            Exception("Invalid Arguments, no input queue")
        if "output" in kwargs:
            output_map = kwargs["output"]
        else:
            Exception("Invalid Arguments, no output map")
        if "token" in kwargs:
            argsdict = {"quandl_token": kwargs["token"]}

        else:
            if "Quandl" in function.__module__:
                Exception("Invalid Arguments, no Quandl token")
        if ("source" and "begin" and "end") in kwargs:
            argsdict = {"data_source": kwargs["source"], "begin": kwargs["begin"], "end": kwargs["end"]}
        else:
            if "pandas.io.data" in function.__module__:
                Exception("Invalid Arguments, no pandas data source specified")
        if ("source" in kwargs) and (("begin" and "end") not in kwargs):
            argsdict = {"data_source": kwargs["source"]}
        else:
            if "pandas.io.data" in function.__module__:
                Exception("Invalid Arguments, no pandas data source specified")
    else:
        Exception("Invalid Arguments")

    retries = 5
    while not input_queue.empty():
        data_key = input_queue.get()
        get_data(function, data_key, output_map, retries, argsdict)


def get_data(data_get, data_key, output_map, retries_left, argdict):
        if retries_left <= 0:
            print(data_key + " Failed to download.")
            return
        if "Quandl" in data_get.__module__:
            #try:
                output_map[data_key] = data_get(data_key, authtoken=argdict["quandl_token"])
                return
            #except:
            #    print(data_key + " failed to download. Retrying up to " + retries_left.__str__() + " more times...")

        if "pandas.io.data" in data_get.__module__:
            if ("source" and "begin" and "end") in argdict:
                try:
                    output_map[data_key] = data_get(data_key, argdict["data_source"], argdict["begin"], argdict["end"])
                    return
                except:
                    print(data_key + " failed to download. Retrying up to " + retries_left.__str__() + " more times...")
            else:
                try:
                    output_map[data_key] = data_get(data_key, argdict["data_source"])
                    return
                except:
                    print(data_key + " failed to download. Retrying up to " + retries_left.__str__() + " more times...")

        # TODO : Replace this with a formula
        # Progressively decrease request speed due to failures
        if (retries_left == 3):
            time.sleep(randrange(0, 4))
        if (retries_left == 2):
            time.sleep(randrange(2, 6))
        if (retries_left == 1):
            time.sleep(randrange(5, 15))
        get_data(data_get, data_key, output_map, (retries_left-1), argdict)


class ConcurrentPandas:
    """
    Concurrent Pandas is a class for concurrent asynchronous data downloads
    from a variety of sources using either threads, or processes.
    """
    def __init__(self):
        self.output_map = Manager().dict()
        self.input_queue = Manager().Queue()
        self.data_worker = None
        self.worker_args = None
        self.source_name = None

    def consume_keys(self):
        """
        Work through the keys to look up sequentially
        """
        print("\nLooking up " + self.input_queue.qsize().__str__() + " keys from " + self.source_name + "\n")
        self.data_worker(**self.worker_args)

    def consume_keys_asynchronous_processes(self):
        """
        Work through the keys to look up asynchronously using multiple processes
        """
        print("\nLooking up " + self.input_queue.qsize().__str__() + " keys from " + self.source_name + "\n")
        jobs = multiprocessing.cpu_count()*4 if (multiprocessing.cpu_count()*4 < self.input_queue.qsize()) \
            else self.input_queue.qsize()

        pool = multiprocessing.Pool(processes=jobs,  maxtasksperchild=10)
        for x in range(jobs):
            pool.apply(self.data_worker, [], self.worker_args)

        pool.close()
        pool.join()

    def consume_keys_asynchronous_threads(self):
        """
        Work through the keys to look up asynchronously using multiple threads
        """
        print("\nLooking up " + self.input_queue.qsize().__str__() + " keys from " + self.source_name + "\n")
        jobs = multiprocessing.cpu_count()*4 if (multiprocessing.cpu_count()*4 < self.input_queue.qsize()) \
            else self.input_queue.qsize()

        pool = ThreadPool(jobs)

        for x in range(jobs):
            pool.apply(self.data_worker, [], self.worker_args)

        pool.close()
        pool.join()

    def return_map(self):
        """
        Return hashmap consisting of key string -> data frame
        """
        return self.output_map

    def return_input_queue(self):
        """
        Return input Queue
        """
        return self.input_queue

    def insert_keys(self, *args):
        """
        Unpack each key and add to queue
        """
        for key in args:
            self.unpack(key)

    def unpack(self, to_unpack):
        """
        Unpack is a recursive function that will unpack anything that inherits
        from abstract base class Container provided it is not also inheriting from Python basestring.

        Raise Exception if resulting object is neither a container or a string

        Code working in both Python 2 and Python 3
        """

        # Python 3 lacks basestring type, work around below
        try:
            isinstance(to_unpack, basestring)
        except NameError:
            basestring = str

        # Base Case
        if isinstance(to_unpack, basestring):
            self.input_queue.put(to_unpack)
            return

        for possible_key in to_unpack:
            if isinstance(possible_key, basestring):
                self.input_queue.put(possible_key)

            elif sys.version_info >= (3, 0):
                if isinstance(possible_key, collections.abc.Container) and not isinstance(possible_key, basestring):
                    self.unpack(possible_key)
                else:
                    raise Exception("A type that is neither a string or a container was passed to unpack. "
                                    "Aborting!")

            else:
                if isinstance(possible_key, collections.Container) and not isinstance(possible_key, basestring):
                    self.unpack(possible_key)
                else:
                    raise Exception("A type that is neither a string or a container was passed to unpack. "
                                    "Aborting!")

    def set_source_quandl(self, quandl_token):
        """
        Set data source to Quandl
        """
        self.data_worker = data_worker
        self.worker_args = {"function": Quandl.get, "input": self.input_queue, "output": self.output_map,
                            "token": quandl_token}
        self.source_name = "Quandl"

    def set_source_yahoo_finance(self):
        """
        Set data source to Yahoo Finance
        """
        self.data_worker = data_worker
        self.worker_args = {"function": pandas.io.data.DataReader, "input": self.input_queue, "output": self.output_map,
                            "source": 'yahoo'}
        self.source_name = "Yahoo Finance"

    def set_source_google_finance(self):
        """
        Set data source to Google Finance
        """
        self.data_worker = data_worker
        self.worker_args = {"function": pandas.io.data.DataReader, "input": self.input_queue, "output": self.output_map,
                            "source": 'google'}
        self.source_name = "Google Finance"

    def set_source_federal_reserve_economic_data(self):
        """
        Set data source to Federal Reserve Economic Data
        """
        self.data_worker = data_worker
        self.worker_args = {"function": pandas.io.data.DataReader, "input": self.input_queue, "output": self.output_map,
                            "source": 'fred'}
        self.source_name = "Federal Reserve Economic Data"
