# queuemp.py
#
# An example of using queues with multiprocessing

def consumer(input_q):
    while True:
        # Get an item from the queue
        item = input_q.get()
        # Process item
        print(item)
        # Signal completion
        input_q.task_done()


def producer(sequence, output_q):
    for item in sequence:
        # Put the item on the queue
        output_q.put(item)


if __name__ == '__main__':
    from multiprocessing import Process, JoinableQueue

    q = JoinableQueue()

    # Launch the consumer process
    cons_p = Process(target=consumer, args=(q,))
    cons_p.daemon = True
    cons_p.start()

    # Run the producer function on some data
    sequence = range(100)  # Replace with useful data
    producer(sequence, q)

    # Wait for the consumer to finish
    q.join()
