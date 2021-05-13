def counter(fu):

    def inner(*a, **kw):
        inner.count += 1
        return fu(*a, **kw)
    inner.count = 0
    return inner


@counter
def test_f():
    if test_f.count % 3 == 0:
        return '!!!'
    return


for i in range(13):
    print(f' {i}:  {test_f()}')
