from multiprocessing import Queue, cpu_count, Process
import math

def reduce(data, func, chunks=10000, process=None):
  pass

# BASED ON 
# http://stackoverflow.com/questions/20727375/multiprocessing-pool-slower-than-just-using-ordinary-functions
def map(data, func, chunks=10000): 
  def consumer(func, data, in_queue, out_queue):
    # get a new message
    val = in_queue.get()

    # terminate condition
    if val is None: return

        # unpack the message
    pos = val[0]  # it is helpful to pass in/out the pos in the array
    rng = val[1]

    # process the data
    ret = [func(i) for i in data[rng[0]:rng[1]] ]

    # send the response / results
    out_queue.put( (pos, ret) )

  def processIN(batches, chunks, in_queue):
    # send position and data to workers
    for b in range(batches):
      in_queue.put((b, [b*chunks, (b+1)*chunks]))

  def processOUT(batches, out_queue):
    # process results
    ans = list(range(batches+1))
    
    for i in range(batches):
      ret = out_queue.get()
      
      if ret is None: break

      pos = ret[0]
      dat = ret[1]
      ans[pos] = dat

    return ans


  def main(data, func, chunks):
    # initialize things
    in_queue = Queue()
    out_queue = Queue()
    
    # instantiate workers
    batches = math.ceil(len(data)/chunks)
    workers = [Process(target=consumer, args=(func, data, in_queue, out_queue)) for i in range(batches)]

    # start the workers
    for w in workers: w.start()

    processIN(batches, chunks, in_queue)
    
    # tell all workers, no more data (one msg for each)
    for i in range(batches): in_queue.put(None)

    ans = processOUT(batches, out_queue)

    # join on the workers
    for w in workers: w.join()

    return ans

  return main(data, func, chunks)


def daemonMap(data, func, chunks=10000): 
  """ Initiates Process class with daemon=True??? 
  
  [description]
  
  Arguments:
    data {[type]} -- [description]
    func {[type]} -- [description]
  
  Keyword Arguments:
    chunks {number} -- [description] (default: {10000})
  
  Returns:
    [type] -- [description]
  """

  def consumer(func, data, in_queue, out_queue):
    # get a new message
    val = in_queue.get()

    # terminate condition
    if val is None: return

    # unpack the message
    pos = val[0]  # it is helpful to pass in/out the pos in the array
    rng = val[1]

    # process the data
    ret = [func(i) for i in data[rng[0]:rng[1]] ]

    # send the response / results
    out_queue.put( (pos, ret) )

  def processIN(batches, chunks, in_queue):
    # send position and data to workers
    for b in range(batches):
      in_queue.put( (b, [b*chunks,(b+1)*chunks]) )

  def processOUT(batches, out_queue):
    # process results
    ans = list(range(batches+1))
    for i in range(batches):
      ret = out_queue.get()
      if ret is None: 
        break
      pos = ret[0]
      dat = ret[1]
      ans[pos] = dat

    return ans


  def main(data, func, chunks):
    # initialize things
    in_queue = Queue()
    out_queue = Queue()
    
    # instantiate workers
    batches = math.ceil(len(data)/chunks)
    workers = [Process(target=consumer, args=(func, data, in_queue, out_queue), daemon=True) for i in range(cpu_count())]

    # start the workers
    for w in workers: w.start()

    processIN(batches, chunks, in_queue)
    
    # tell all workers, no more data (one msg for each)
    for i in range(batches): in_queue.put(None)

    ans = processOUT(batches, out_queue)

    # join on the workers
    for w in workers: w.join()

    return ans

  return main(data, func, chunks)