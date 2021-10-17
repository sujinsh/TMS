class MeanFilter():
    def __init__(self, size=4):
        self.q = []
        self.size = max(size, 1)
        self.mean = 0

    def get(self):
        if len(self.q) >self.size:
            return self.mean
        elif len(self.q) > 0:
            return self.q[-1]
        return None

    def add(self, val):
        if len(self.q) < self.size:
            self.q.append(val)
            self.mean += val/self.size
        else:
            self.mean -= self.q[0]/self.size
            for i in range(self.size-1):
                self.q[i] = self.q[i+1]
            self.q[-1] = val
            self.mean += val/self.size


class WeightedFilter():
    def __init__(self, weight_new=0.9):
        self.val = 0
        self.w = min(max(weight_new,0.01),1)

    def get(self):
        return self.val

    def add(self, val):
        self.val = (1-self.w)*self.val + self.w * val

class ConstFilter():
    def __init__(self):
        self.val = None

    def get(self):
        return self.val

    def add(self, val):
        self.val = val