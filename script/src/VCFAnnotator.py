__author__ = 'Rajaram Kaliyaperumal'
__author__ = 'Mark Thompson'
__author__ = 'Eelke van der Horst'

from vcf.parser import _Info as VcfInfo, field_counts as vcf_field_counts
import vcf
import Fantom5Nanopublication
import sparql

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
        self.fantom5NP = Fantom5Nanopublication.Fantom5Nanopublication('http://ep.dbcls.jp/fantom5/sparql')

    """
    <p>
    Read the input VCF file, add annotations to the #INFO column and write it back to the output VCF file.
    </p>
    """
    def add_annotation(self):

        vcf_reader = vcf.Reader(open(self.inputFile, 'r'))
        vcf_reader.infos['TSSOL'] = VcfInfo('TSSOL', vcf_field_counts['A'], 'Boolean',
                                            'Info indicates whether the variant overlapping with the'
                                            ' transcription start site(TSS)')

        vcf_writer = vcf.VCFWriter(open(self.outputFile, 'w'), vcf_reader)


        for record in vcf_reader:

            isOverlapping =  self.is_overlapping_with_tss(record)
            record.add_info('TSSOL', [isOverlapping])
            vcf_writer.write_record(record)

        vcf_writer.close()

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






test = VCFAnnotator('../test/example.vcf', '../test/output1.vcf')
test.add_annotation()