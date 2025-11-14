class Queue:
    def __init__(self, max_size=100):
        self.MAX = max_size
        self.queue = [0] * self.MAX
        self.front = -1
        self.rear = -1

    def is_empty(self):
        return self.front == -1

    def is_full(self):
        return (self.rear + 1) % self.MAX == self.front

    def enqueue(self, song):
        if self.is_full():
            print("Queue Overflow!")
            return

        if self.is_empty():
            self.front = 0
        self.rear = (self.rear + 1) % self.MAX
        self.queue[self.rear] = song
        # print(f"Added: {song}")  # Optional for debugging

    def dequeue(self):
        if self.is_empty():
            print("Queue Underflow!")
            return -1

        song = self.queue[self.front]
        if self.front == self.rear:
            self.front = self.rear = -1
        else:
            self.front = (self.front + 1) % self.MAX
        # print(f"Removed: {song}")  # Optional for debugging
        return song

    def getAllqueue(self):
        if self.is_empty():
            return []
        lst = []
        i = self.front
        while True:
            lst.append(self.queue[i])
            if i == self.rear:
                break
            i = (i + 1) % self.MAX
        return lst

