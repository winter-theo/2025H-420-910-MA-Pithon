class Foo:
    def __init__(self):
        self.x = 42

    def test(self):
        return self.x+100

y = Foo()
y.toto = 5
print(y.toto)


