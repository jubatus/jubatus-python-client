import sys

if sys.version_info >= (3, 0):
    int_types = (int, )
    string_types = (str, )
    binary_types = (bytes, )

    def u(s):
        return s

    def b(s):
        return s.encode()

else:
    int_types = (int, long)
    string_types = (str, unicode)
    binary_types = (str, )

    def u(s):
        return unicode(s)

    def b(s):
        return s
