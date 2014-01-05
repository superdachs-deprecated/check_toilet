import argparse
from urllib import urlopen
import nagiosplugin

__author__ = 'stk'

class ToiletSeat(nagiosplugin.Resource):

    def __init__(self, args):
        self.args = args

    def probe(self):
        response = urlopen("http://" + self.args.host)
        statusstr = response.read()

        if(statusstr == "0"):
            status = 0
        if(statusstr == "1"):
            status = 1
        if(statusstr == "2"):
            status = 2

        yield nagiosplugin.Metric('status', status, context='status')

class ToiletSeatSummary(nagiosplugin.Summary):

    def problem(self, results):

        res = str(results["status"].metric)

        returnstr = ""

        if res == "1":
            returnstr = "lid open, seat closed"
        if res == "2":
            returnstr = "lid open, seat open"

        return returnstr

    def ok(self, results):

        #return str(results["status"].metric)
        return "lid closed, seat closed"

@nagiosplugin.guarded
def main():

    argp = argparse.ArgumentParser(description=__doc__)
    argp.add_argument('-H', '--host', dest='host', default='', help='toilet host')
    args = argp.parse_args()

    check = nagiosplugin.Check(ToiletSeat(args), nagiosplugin.ScalarContext('status', '0:0', '0:1'), ToiletSeatSummary())

    check.main()

if __name__ == '__main__':
    main()

