
DEGREES = '\N{DEGREE SIGN}'

class Temperature:
    def __init__(self, value:int=None):
        self._value = value

    @property
    def degrees_c(self):
        return self._value

    @property
    def degrees_f(self):
        return self._value * 9/5 + 32

    def __format__(self, fmt):
        # todo:  this should probably be :.1F, not :1F
        if (fmt or '') == '':
            return f'{self._value}'
        if len(fmt) > 2:
            raise ValueError('fmt can be at most 2 characters long')

        decimals = 0
        units = ''
        if len(fmt) == 2:
            decimals = int(fmt[0])
            units = fmt[1]
        else:
            if fmt.isnumeric():
                decimals = int(fmt)
            else:
                units = fmt
        value = self.degrees_f if units in ('f', 'F') else self.degrees_c
        fmt_str = f'{{:.{decimals}f}}{{}}{{}}'
        return fmt_str.format(value, DEGREES, units)

    @classmethod
    def from_bytes(cls, value: bytes, fixed_point: int=1):
        return cls(int.from_bytes(value, byteorder='little') / fixed_point)
