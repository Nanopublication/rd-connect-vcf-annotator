__author__ = 'Rajaram Kaliyaperumal'
__author__ = 'Mark Thompson'
__author__ = 'Eelke van der Horst'

import TSS

class Variant():
    def __init__(self, record):
        self.start = record.start
        self.end = record.end
        self.chromosome = record.CHROM
        self.type = record.var_subtype

        # Adding chr prefix to the chromosome
        if "chr" not in self.chromosome:
            self.chromosome = "chr"+str(record.CHROM)

    def overlaps(self, tss):
        # overlap of any "region" (either a Variant or TSS)
        region_overlap = (self.end >= tss.start and self.end <= tss.end) or \
                         (self.start >= tss.start and self.start <= tss.end) or \
                         (self.start < tss.start and self.end > tss.end)


        if not region_overlap:
            return False
        # special case for variants that are inserts
        if isinstance(tss, TSS.TSS) and self.type == 'ins':
            return self.start > tss.start
        return region_overlap