__author__ = 'Rajaram Kaliyaperumal'
__author__ = 'Mark Thompson'
__author__ = 'Eelke van der Horst'

import sys
import vcf


def intersect2(bIt, bVar, fIt, fVar):
    if bVar.POS > fVar.POS:
        print "Out of sync"
        exit(1)

    if bVar == fVar:
        print "match"

    tmp = bIt.next()
    if tmp.POS <= fVar.POS:
        intersect2(bIt, tmp, fIt, fVar)
    else:
        intersect2(fIt, fVar, bIt, tmp)


def intersect1(it1, it2):
    v1 = it1.next()
    v2 = it2.next()

    if v1.POS <= v2.POS:
        intersect2(it1, v1, it2, v2)
    else:
        intersect2(it2, v2, it1, v1)

# add writer
# intersect 3 inputs
# run on result

# merge / send first family of 2
# send mail


def intersectIter2(it1, it2, writer):
    v1 = it1.next()
    v2 = it2.next()
    cnt = 0

    while True:
        print "%s %s %s" %(cnt, v1.POS, v2.POS)

        if v1 == v2:
            print "match %s %s %s" %(cnt, v1.POS, v2.POS)
            cnt += 1
            v1 = it1.next()
            v2 = it2.next()
            #writer.write_record(v1)
        elif v1.POS == v2.POS:
            v1 = it1.next()
            v2 = it2.next()
        else:
            left_inc = 0
            while v1.POS < v2.POS:
                new = it1.next()
                if new.POS < v1.POS:
                    exit(1)
                v1 = new
                left_inc += 1
            if left_inc > 0:
                continue
            while v1.POS > v2.POS:
                new = it2.next()
                if new.POS < v2.POS:
                    exit(1)
                v2 = new
        #v1 = it1.next()
        #v2 = it2.next()



def intersectIter(it1, it2, writer):
    v1 = it1.next()
    v2 = it2.next()
    cnt = 0
    v1start = v1
    v2start = v2

    while True:
        #if not v1 or not v2:
        #    break

        if v1start is v1:
            print "v1 as start"
        else:
            print "v1 switched"

        if v2start is v2:
            print "v2 as start"
        else:
            print "v2 switched"

        if v1.POS > v2.POS:
            tmpV = v1
            tmpIt = it1
            v1 = v2
            it1 = it2
            v2 = tmpV
            it2 = tmpIt

        print "%s %s %s" %(cnt, v1.POS, v2.POS)
        if v1 == v2:
            cnt += 1
            #writer.write_record(v1)

        #try:
        v1 = it1.next()
        #except StopIteration:
        #    exit(0)


class intersection:

    def __init__(self, vcf1, vcf2):

        self.v1 = vcf.Reader(open(vcf1))
        self.v2 = vcf.Reader(open(vcf2))
        #self.it = itertools.product(self.v1, self.v2)

    def intersect(self):
        i = j = 0
        for left in self.v1:
            i += 1
            for right in self.v2:
                j += 1
                if left == right:
                    print "(%d, %d) %s %s %s" % (i, j, left.start, left.end, left.CHROM)
                else:
                    print "(%d, %d)" % (i, j)





if __name__ == "__main__":
    #isec = intersection(sys.argv[1], sys.argv[2])
    #isec.intersect()

    r1 = vcf.Reader(open(sys.argv[1]))
    r2 = vcf.Reader(open(sys.argv[2]))
    w = vcf.VCFWriter(open(sys.argv[3], 'w'), r1)
    intersectIter2(r1, r2, w)


