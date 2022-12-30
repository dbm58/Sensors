
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
        """
        Support for str.format() and f'...' strings

        Syntax: [<fmt-spec>][<units-spec>]

        Where:
        <fmt-spec> can be any valid floating point format specification, but
        without the type part (that is, 10.3, not 10.3d)

        <units-spec> is one of: c, C, f, or F.  If included, a degree symbol
        will be appended to the formatted value, followed by the <units-spec>.

        If the <units-spec> is not include, the value will be in degrees C.  If
        the <units-spec> is 'f' or 'F', then the value will be converted to 
        Farhenheit before formatting.

        Known issues:
        * The degree symbol and units spec is always printed at the end of the
          field.  Even if the left-adjust or center option is used
          (e.g. {:<10.1C})
        """
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
