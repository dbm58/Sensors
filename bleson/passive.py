#!/usr/bin/env python

from collector import Collector
from output    import Output
from parser    import Parser
from scanner   import Scanner

if __name__ == '__main__':
    args = Parser.parse()

    collector = Collector(args)
    Scanner.scan(args, collector)

    Output.write(args, collector)
