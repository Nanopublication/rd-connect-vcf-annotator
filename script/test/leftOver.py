__author__ = 'rajaram'

#Reference : https://pypi.python.org/pypi/pyliftover
#Left over data : http://hgdownload.cse.ucsc.edu/gbdb/hg38/liftOver/

from pyliftover import LiftOver
#lo = LiftOver('hg38', 'hg19')
lo = LiftOver('hg38ToHg19.over.chain.gz')
for x in range(0, 100):
    data = lo.convert_coordinate('chr1', 1000000+x)
    print data
    data2 = data.pop()
    print data2[0]
