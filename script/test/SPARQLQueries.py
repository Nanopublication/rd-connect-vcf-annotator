__author__ = 'Eelke'
__author__ = 'Mark'
__author__ = 'Rajaram'

import sparql


class sparqlQueries():

    def getTSS (self, endpoint, variantStart, variantEnd, variantChromosome):

        file = open("fantom5TSSForGenomicLocation", "r")
        query = file.read()
        query = query.replace("?variantStart", str(variantStart))
        query = query.replace("?variantEnd", str(variantEnd))
        query = query.replace("?variantChromosome", str("hg19:"+variantChromosome))

        #print query

        result = sparql.query(endpoint, query)

        #for row in result:
           #print 'row:', row
         #  values = sparql.unpack_row(row)
          # print values[1], "-", values[2], "-", values[3], "-", values[4]

        return result



#test = sparqlQueries()
#test.getTSS('http://ep.dbcls.jp/fantom5/sparql', 31350184, 31350186, 'chr20')
