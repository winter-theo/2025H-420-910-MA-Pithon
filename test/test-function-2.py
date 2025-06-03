def foo(a, b):
    return a + b
    x = 42
    return 42  # Ceci devrait être inatteignable

print(foo(1, 2))  # Should print 3