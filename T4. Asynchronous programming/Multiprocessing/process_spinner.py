import sys
import time

for i in range(12):
    sys.stdout.write("\rReading data {}".format('.'*i))
    sys.stdout.flush()
    time.sleep(0.5)