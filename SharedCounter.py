import threading

class SharedCounter:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def increment(self,num):
        with self._lock:
            self.value += num
    def get(self):
        return self.value
