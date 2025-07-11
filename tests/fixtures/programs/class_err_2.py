class Foo:
    def __init__(self):
        self.x = 42

    def test(self):
        return self.y+100

x = Foo()
print(x.test())

