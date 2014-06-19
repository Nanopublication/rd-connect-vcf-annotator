__author__ = 'Rajaram Kaliyaperumal'
__author__ = 'Mark Thompson'
__author__ = 'Eelke van der Horst'

import sparql

"""
<p>
To query the FANTOM5 nanopublications via SPARQL endpoint.
</p>
"""

class Fantom5Nanopublication:

    """
    <p>
    Class Constructor
    </p>

    @params endpoint    :   URL of the SPARQL endpoint
    """

    def __init__(self, endpoint):
        self.endpoint = endpoint

    """
    <p>
    Get transcription start site (TSS) for the given genomic region.
    </p>

    @params chromosome  :   Chromosome number with prefix chr. (Eg. chr18)
    @params start       :   Region start position. (Eg. 23400)
    @params end         :   Region end position.   (Eg. 25607)
    """
    def get_tss (self, chromosome, start, end):

        queryTemplatefile = open("../resources/sparqlQueries/fantom5TSSForGenomicLocation", "r")

        query = queryTemplatefile.read()
        query = query.replace("?variantStart", str(start))
        query = query.replace("?variantEnd", str(end))
        query = query.replace("?variantChromosome", str("hg19:"+chromosome))

        #print query

        # Quering the SPARQL endpoint
        result = sparql.query(self.endpoint, query)

        return result
