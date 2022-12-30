
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

        units = ''
        formatted_units = ''
        if fmt[-1] in ('c', 'C', 'f', 'F'):
            units = fmt[-1]
            formatted_units = f'{DEGREES}{fmt[-1]}'
            fmt = fmt[:-1]

        formatter = f':{fmt}' if len(fmt) > 0 else ''

        value = self.degrees_f if units in ('f', 'F') else self.degrees_c

        fmt_str = f'{{{formatter}f}}{{}}'

        return fmt_str.format(value, formatted_units)

    @classmethod
    def from_bytes(cls, value: bytes, fixed_point: int=1):
        return cls(int.from_bytes(value, byteorder='little') / fixed_point)
