class Timer:
    def __init__(self, startVal=-1):
        self.val = startVal

    def tick(self):
        if self.val >= 0:
            self.val -= 1
    
    def reset(self):
        self.val = -1
    
    def set(self, val):
        self.val = val
    
    def get(self):
        return self.val