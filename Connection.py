import inspect

class Device(object):
    def __init__(self):
        pass

    def lywsd02(self):
        """Clock Thermometer"""
        pass

    def lywsd03(self):
        """Thermometer/Hygrometer"""
        pass

    @classmethod
    def _members(cls):
        members = inspect.getmembers(
                cls(),
                predicate=lambda m: 
                    inspect.isroutine(m)
                    and (not m.__name__.startswith('_'))
                    and (not m.__self__ == cls)
                )
        return dict(members)

    @classmethod
    def create(cls):
        pass

    @classmethod
    def add_parser(cls, parser):
        members = cls._members()
        choices = list(members.keys())

        helptext = ['Device to connect to.  One of: ']
        helptext.extend([f'{a} - {members[a].__doc__}' for a in choices])
        helptext = '\n'.join(helptext)
        
        parser.add_argument('device', help=helptext, choices=choices)

        return choices
