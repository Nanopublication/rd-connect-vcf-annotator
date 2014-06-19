__author__ = 'Rajaram Kaliyaperumal'
__author__ = 'Mark Thompson'
__author__ = 'Eelke van der Horst'

class TSS():
    def __init__(self, cageClusterURI, chromosome, start, end, orientation):
        self.cageClusterURI = cageClusterURI
        self.start = start
        self.end = end
        self.chromosome = chromosome
        self.orientation = orientation