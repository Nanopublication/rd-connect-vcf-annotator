
__author__ = 'Rajaram Kaliyaperumal'
__author__ = 'Mark Thompson'
__author__ = 'Eelke van der Horst'

import sparql
import TSS
from SPARQLWrapper import SPARQLWrapper, JSON


class Fantom5Nanopublication:
    """
    <p>
    To query the FANTOM5 nanopublications via SPARQL endpoint.
    </p>"""


    def __init__(self, endpoint):
        """
        <p>
        Class Constructor
        </p>
    
        @params endpoint    :   URL of the SPARQL endpoint
        """

        self.endpoint = endpoint
        

    def get_tss(self, chromosome, start, end):
        """<p>
        Get transcription start site (TSS) for the given genomic region.
        </p>
    
        @params chromosome  :   Chromosome number with prefix chr. (Eg. chr18)
        @params start       :   Region start position. (Eg. 23400)
        @params end         :   Region end position.   (Eg. 25607)
        """

        queryTemplatefile = open("../resources/sparqlQueries/fantom5TSSForGenomicLocation", "r")

        query = queryTemplatefile.read()
        query = query.replace("?variantStart", str(start))
        query = query.replace("?variantEnd", str(end))
        query = query.replace("?variantChromosome", str("hg19:"+chromosome))

        #print query

        # Quering the SPARQL endpoint
        queryResult = sparql.query(self.endpoint, query)

        tssList = []

        for row in queryResult:

            values = sparql.unpack_row(row)

            cageClusterURL = values[0]
            cageStart = values[1]
            cageEnd = values[2]
            cageChromosome = values[3]
            cageOrientation = values[4]

            tss = TSS.TSS(cageClusterURL, cageChromosome, cageStart, cageEnd, cageOrientation)
            tssList.append(tss)

        return tssList


    def get_sample(self, cageClusterURI):
        """<p>
        Get samples with tpmValue > 0 for the given cage cluster URI.
        </p>

        @params cageClusterURI  :   Cage cluster URI
                                    (Eg. http://rdf.biosemantics.org/resource/riken/fantom5/cage_cluster_43878)
        """
        sampleList = []
        sparql = SPARQLWrapper(self.endpoint)
        queryTemplatefile = open("../resources/sparqlQueries/fantom5SamplesForCageCluster", "r")
        query = queryTemplatefile.read()
        query = query.replace("?cageCluster", "<"+str(cageClusterURI)+">")
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        # Quering the SPARQL endpoint
        results = sparql.query().convert()


        for result in results["results"]["bindings"]:
            sample = result["sample"]["value"]
            sampleList.append(sample)

        return sampleList