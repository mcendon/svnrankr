import argparse, os, operator, sys, json
from math import sqrt
from itertools import count, islice

class SvnRankr:
    def __init__(self):
        self.ranking = {
            "range": {
                "date": {"from": None, "to": None},
                "commits": {"from": None, "to": None}
            },
            "results": {}
        }

    def rank(self, logLine):
        data = self.extractData(logLine)
        n = data[0]
        user = data[1]
        date = data[2]

        if self.ranking["range"]["date"]["to"] == None:
            self.ranking["range"]["date"]["to"] = date
        self.ranking["range"]["date"]["from"] = date

        if self.ranking["range"]["commits"]["to"] == None:
            self.ranking["range"]["commits"]["to"] = n
        self.ranking["range"]["commits"]["from"] = n

        if user not in self.ranking["results"]:
            self.ranking["results"][user] = {"all": {"count": 0}, "special": {"count": 0, "numbers": []}}
        else:
            self.ranking["results"][user]["all"]["count"] += 1
        if self.isInteresting(n):
                self.ranking["results"][user]["special"]["numbers"].append(n)
                self.ranking["results"][user]["special"]["count"] += 1

    def getRanking(self):
        return self.ranking

    def extractData(self, line):
        lineArr = line.split('|')
        for i in range(0, len(lineArr)):
            lineArr[i] = lineArr[i].strip()
            if i == 0:
                lineArr[i] = int(lineArr[i][1:])
        return lineArr

    def isInteresting(self, n):
        return (self.oneHundredMultiple(n)
        or self.isPrime(n)
        or self.isStair(n)
        or self.isSymmetrical(n)
        or self.isMirror(n))

    def oneHundredMultiple(self, n):
        return n % 100 == 0

    # 1, 3, 5, 7, 11, etc
    def isPrime(self, n):
        return n > 1 and all(n%i for i in islice(count(2), int(sqrt(n)-1)))

    # 1234 / 4321
    def isStair(self, n):
        numberList = list(str(n))
        pivot = int(numberList[0])
        for i in range(1,len(numberList)):
            if int(numberList[i]) != pivot + 1:
                return False
            pivot = int(numberList[i])
        return True

    #1221 / 1331 / 2332 / 1111 / 55555
    def isSymmetrical(self, n):
        numberList = list(str(n))
        length = len(numberList)
        for i in range(0,length):
            if int(numberList[i]) != int(numberList[length-1-i]):
                return False
        return True

    def isMirror(self, n):
        strn = str(n)
        digits = len(strn)
        return digits % 2 == 0 and strn[:digits / 2] == strn[-digits / 2:]

parser = argparse.ArgumentParser(description='Make an SVN commit ranking, by interesting commit numbers.')
parser.add_argument('file', metavar='File', type=str, nargs=1,
                   help='SVN log database file')
svnrankr = SvnRankr()
args = parser.parse_args()
filename = args.file[0]
if os.path.isfile(filename) or filename == 'stdin':
    if filename == 'stdin':
        infile = sys.stdin
    else:
        infile = open(filename, 'r')
    line = infile.readline()
    while line != '':
        if line[0] == 'r':
            svnrankr.rank(line)
        line = infile.readline()
    infile.close()
    ranking = svnrankr.getRanking()
    print json.dumps(ranking, sort_keys=True, indent=4, separators=(',', ': '))
else:
    print 'File not exists: ' + filename
