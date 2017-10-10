from curry import curry


@curry
def foo(a, b, c):
    print "ALL:", a, b, c


def main():
    a = foo(10)

    a(11, 12)


if __name__ == '__main__':
    main()
