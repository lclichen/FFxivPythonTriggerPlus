from binascii import unhexlify


def long_to_bytes(val, little_endianness=False):
    width = val.bit_length()
    width += 8 - ((width % 8) or 8)
    fmt = '%%0%dx' % (width // 4)
    s = unhexlify(fmt % val)
    return s[::-1] if little_endianness else s
