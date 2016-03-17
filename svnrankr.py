import argparse, os, operator
from math import sqrt
from itertools import count, islice

class SvnRankr:
    def __init__(self):
        self.ranking = {}

    def rank(self, logLine):
        data = self.extractData(logLine)
        n = data[0]
        user = data[1]
        if self.isInteresting(n):
            if user not in self.ranking:
                self.ranking[user] = 1
            else:
                self.ranking[user] += 1

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
if os.path.isfile(filename):
    infile = open(filename, 'r')
    line = infile.readline()
    while line != '':
        if line[0] == 'r':
            svnrankr.rank(line)
        line = infile.readline()
    infile.close()
    ranking = svnrankr.getRanking()
    for user in ranking:
        print user + ': ' + str(ranking[user])
else:
    print 'File not exists: ' + filename
