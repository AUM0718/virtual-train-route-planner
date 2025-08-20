class StationNode:
    def __init__(self, name):
        self.name = name
        self.next = None
        self.prev = None
        self.negative = False
    def __repr__(self):
        return f"{self.name}{'(NEG)' if self.negative else ''}"

class BaseLine:
    def __init__(self, name):
        self.name = name
        self._lookup = {}
    def has_station(self, n): return n in self._lookup
    def get(self, n): return self._lookup.get(n)
    def mark_negative(self, n, neg=True):
        self.get(n).negative = neg
    def add_stations(self, names):
        for n in names: self.add_station(n)

class DoublyLinkedLine(BaseLine):
    def __init__(self, name):
        super().__init__(name); self.head = None; self.tail = None
    def add_station(self, name):
        node = StationNode(name); self._lookup[name] = node
        if not self.head: self.head = self.tail = node; return
        self.tail.next = node; node.prev = self.tail; self.tail = node
    def remove_station(self, name):
        node = self._lookup.pop(name); 
        if node.prev: node.prev.next = node.next
        else: self.head = node.next
        if node.next: node.next.prev = node.prev
        else: self.tail = node.prev
    def iter_forward(self, start):
        node = self.get(start)
        while node: yield node; node = node.next
    def iter_backward(self, start):
        node = self.get(start)
        while node: yield node; node = node.prev

class CircularLine(BaseLine):
    def __init__(self, name):
        super().__init__(name); self.head = None; self._size = 0
    def add_station(self, name):
        node = StationNode(name); self._lookup[name] = node
        if not self.head: self.head = node; node.next = node.prev = node
        else:
            tail = self.head.prev
            tail.next = node; node.prev = tail
            node.next = self.head; self.head.prev = node
        self._size += 1
    def remove_station(self, name):
        node = self._lookup.pop(name)
        if self._size == 1: self.head = None; self._size = 0; return
        node.prev.next, node.next.prev = node.next, node.prev
        if self.head is node: self.head = node.next
        self._size -= 1
    def iter_forward(self, start):
        node = self.get(start); curr = node
        while True: yield curr; curr = curr.next; 
        if curr is node: break
    def iter_backward(self, start):
        node = self.get(start); curr = node
        while True: yield curr; curr = curr.prev; 
        if curr is node: break
    def size(self): return self._size

class RoutePlanner:
    def _validate(self, line, s, e):
        if not line.has_station(s) or not line.has_station(e): raise KeyError
        if line.get(s).negative or line.get(e).negative: raise ValueError
    def _names(self, path): return [n.name for n in path]
    def plan_on_linear(self, line, s, e):
        self._validate(line, s, e)
        path = []
        for n in line.iter_forward(s):
            if not n.negative: path.append(n)
            if n.name == e: return self._names(path)
        path = []
        for n in line.iter_backward(s):
            if not n.negative: path.append(n)
            if n.name == e: return self._names(path)
    def plan_on_circular(self, line, s, e):
        self._validate(line, s, e)
        cw, ccw = [], []
        for n in line.iter_forward(s):
            if not n.negative: cw.append(n)
            if n.name == e: break
        for n in line.iter_backward(s):
            if not n.negative: ccw.append(n)
            if n.name == e: break
        return self._names(cw) if cw and (not ccw or len(cw)<=len(ccw)) else self._names(ccw) if ccw else None
    def plan(self, line, s, e):
        return self.plan_on_linear(line,s,e) if isinstance(line,DoublyLinkedLine) else self.plan_on_circular(line,s,e)

if __name__ == "__main__":
    red = DoublyLinkedLine("Red"); red.add_stations(["A1","A2","A3","A4","A5","A6"])
    loop = CircularLine("Loop"); loop.add_stations(["C1","C2","C3","C4","C5","C6"])
    p = RoutePlanner()
    print("Linear A2->A5:", p.plan(red,"A2","A5"))
    red.mark_negative("A4",True); print("A2->A5 with A4 NEG:", p.plan(red,"A2","A5"))
    red.mark_negative("A4",False); print("A2->A5 restored:", p.plan(red,"A2","A5"))
    print("Circular C6->C3:", p.plan(loop,"C6","C3"))
    loop.mark_negative("C2",True); print("C6->C3 with C2 NEG:", p.plan(loop,"C6","C3"))
