# subject.py

class Subject:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self, data):
        for observer in self.observers:
            observer.update(data)
