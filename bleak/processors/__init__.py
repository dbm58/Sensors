import inspect

from .aranet4 import Aranet4
from .govee import Govee
from .lywsd03 import Lywsd03
from .unknown import Unknown

members = dict(
              map(
                  lambda m: (m[0].lower(), m[1]),
                  filter(
                      lambda m: inspect.isclass(m[1]),
                      globals().items()
                  )
              )
          )
