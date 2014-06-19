class Variant():
    def __init__(self, record):
        self.start = record.start
        self.end = record.end
        self.chr = record.CHROM
        self.type = record.var_subtype

    def overlaps(self, tss):
        # overlap of any "region" (either a Variant or TSS)
        region_overlap = (self.end >= tss.start and self.end <= tss.end) or \
                         (self.start >= tss.start and self.start <= tss.end)
        if not region_overlap:
            return False
        # special case for variants that are inserts
        if isinstance(tss, TSS) and self.type == 'ins':
            return self.start > tss.start
        return region_overlap