__author__ = 'Rajaram Kaliyaperumal'
__author__ = 'Mark Thompson'
__author__ = 'Eelke van der Horst'

from vcf.parser import _Info as VcfInfo, field_counts as vcf_field_counts
import vcf
import Fantom5Nanopublication
import sparql
import sys
import time
"""
<p>
Takes VCF file has a input, adds extra annotation to the VCF #INFO column.
</p>
"""

class VCFAnnotator:

    """
    <p>
    Class Constructor
    </p>

    @params inputFile   :   Input VCF file name with full path
    @params outputFile  :   Output VCF file name with full path
    """
    def __init__(self, inputFile, outputFile):

        self.inputFile = inputFile
        self.outputFile = outputFile
        self.fantom5NP = Fantom5Nanopublication.Fantom5Nanopublication('http://145.100.57.2:8890/sparql')

    """
    <p>
    Read the input VCF file, add annotations to the #INFO column and write it back to the output VCF file.
    </p>
    """
    def add_annotation(self):

        vcfReader = vcf.Reader(open(self.inputFile, 'r'))
        """
        How to add info header
         <http://www.1000genomes.org/wiki/Analysis/Variant%20Call%20Format/vcf-variant-call-format-version-41>
        """
        vcfReader.infos['TSSOL'] = VcfInfo('TSSOL', vcf_field_counts['A'], 'String',
                                            'Info indicates whether the variant overlapping with the'
                                            ' transcription start site(TSS)')

        vcfWriter = vcf.VCFWriter(open(self.outputFile, 'w'), vcfReader)

        varTSSOL = 0
        varNoTSSOL = 0
        cnt = 0
        cnt_block = 10
        t1 = time.time()

        for record in vcfReader:
            isOverlapping =  self.is_overlapping_with_tss(record)

            if (isOverlapping):
                varTSSOL = varTSSOL+1
            else:
                varNoTSSOL = varNoTSSOL+1



            record.add_info('TSSOL', [isOverlapping])
            vcfWriter.write_record(record)

            print "Variant checked = "+str(varTSSOL+varNoTSSOL)
            print "Variant TSS overlaps = "+str(varTSSOL)

            if cnt % cnt_block == 1:
                print "counter"
                t2 = time.time()
                ips = cnt_block / (t2-t1)
                print "speed: %.2f iters/s = %d iters p/h = %.1f hours/million iters" % (ips, ips*3600, 1000000/ips/3600)
                t1 = time.time()
            cnt += 1

        vcfWriter.close()

    """
    <p>
    Check if the variant is overlapping with the transcription start site (TSS).

    <i>Note: No overlapping rule => If the variant is of type insert(ins) and the variant start is before TSS start</i>
    </p>
    """
    def is_overlapping_with_tss(self, record):

        isOverlapping = False

        variantStart = record.start+1
        variantEnd = record.end
        variantChromosome = record.CHROM
        variantSubType = record.var_subtype

        # Adding chr prefix to the chromosome
        if "chr" not in variantChromosome:
            variantChromosome = "chr"+str(record.CHROM)

        # SPARQL query
        result = self.fantom5NP.get_tss(variantChromosome, variantStart, variantEnd)

        for row in result:

            values = sparql.unpack_row(row)
            cageStart = values[1]
            cageEnd = values[2]

            if ((variantSubType == 'ins') & ( variantStart > cageStart )):
                isOverlapping = True
                break
            elif ((variantSubType != 'ins')):
                isOverlapping = True
            break

        return isOverlapping






#test = VCFAnnotator('/home/rajaram/work/rd-connect-vcf-annotator/input/UseCases/DNC0040.allchr.snpEff.p.vcf.gz', '/home/rajaram/work/rd-connect-vcf-annotator/output/output1.vcf')
test = VCFAnnotator('/Users/mark/rdconnect/input/UseCases/DNC0040.allchr.snpEff.p.vcf.gz', '/tmp/output1.vcf')

#test = VCFAnnotator(argv[1], argv[2])
test.add_annotation()