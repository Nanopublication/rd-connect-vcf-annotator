__author__ = 'Rajaram Kaliyaperumal'
__author__ = 'Mark Thompson'
__author__ = 'Eelke van der Horst'

from vcf.parser import _Info as VcfInfo, field_counts as vcf_field_counts
import vcf
import Fantom5Nanopublication
import Variant
import sys
import time


class VCFAnnotator:
    """Takes VCF file has a input, adds extra annotation to the VCF #INFO column."""

    def __init__(self, inputFile, outputFile, endpoint):
        """VCFAnnotator Constructor
    
        @params inputFile   :   Input VCF file name with full path
        @params outputFile  :   Output VCF file name with full path
        """
        self.inputFile = inputFile
        self.outputFile = outputFile
        self.fantom5NP = Fantom5Nanopublication.Fantom5Nanopublication(endpoint)

    def add_annotation(self):
        """
        <p>
        Read the input VCF file, add annotations to the #INFO column and write it back to the output VCF file.
        </p>
        """

        vcfReader = vcf.Reader(open(self.inputFile, 'r'))
        """
        How to add info header
         <http://www.1000genomes.org/wiki/Analysis/Variant%20Call%20Format/vcf-variant-call-format-version-41>
        """
        vcfReader.infos['TSSOL'] = VcfInfo('TSSOL', vcf_field_counts['A'], 'String',
                                            'Info indicates whether the variant overlapping with the'
                                            ' transcription start site(TSS)')
        vcfReader.infos['CCURI'] = VcfInfo('CCURI', vcf_field_counts['A'], 'String',
                                            'Info includes the URL of the cage cluster to which the'
                                            ' variant overlapping')
        vcfReader.infos['SAMPURI'] = VcfInfo('SAMPURI', vcf_field_counts['A'], 'String',
                                            'Info includes the URL of the samples with to which the'
                                            ' variant overlapping')

        vcfWriter = vcf.VCFWriter(open(self.outputFile, 'w'), vcfReader)

        varTSSOL = 0
        varNoTSSOL = 0
        cnt = 0
        cnt_block = 10
        t1 = time.time()

        for record in vcfReader:
            isOverlapping = False
            urlList =  self.get_overlapping_tss_urls(record)

            if (len(urlList) == 0):
                varNoTSSOL = varNoTSSOL+1

            else:
                varTSSOL = varTSSOL+1
                isOverlapping = True

            if isOverlapping:
                record.add_info('CCURI', urlList)
                record.add_info('SAMPURI', self.get_samples_url(urlList))




            record.add_info('TSSOL', [isOverlapping])
            vcfWriter.write_record(record)

            print "Variant checked = "+str(varTSSOL+varNoTSSOL)
            print "Variant overlaps with TSS  = "+str(varTSSOL)

            if cnt % cnt_block == 1:
                print "counter"
                t2 = time.time()
                ips = cnt_block / (t2-t1)
                print "speed: %.2f iters/s = %d iters p/h = %.1f hours/million iters" % (ips, ips*3600, 1000000/ips/3600)
                t1 = time.time()
            cnt += 1

        vcfWriter.close()
        

    def get_overlapping_tss_urls(self, record):
        """
        <p>
        Check if the variant is overlapping with the transcription start site (TSS).
    
        <i>Note: No overlapping rule => If the variant is of type insert(ins) and the variant start is before TSS start</i>
        </p>
        """

        isOverlapping = False

        variant = Variant.Variant(record)
        
        resultList = []
        
        # SPARQL query
        tssList = self.fantom5NP.get_tss(variant.chromosome, variant.start, variant.end)

        for tss in tssList:
            isOverlapping = variant.overlaps(tss)
            
            if isOverlapping:
                resultList.append(tss.cageClusterURI)
            
        return resultList


    def get_samples_url(self, tssUriList):
        resultList = []
        samples = set()

        for cageCluster in tssUriList:
            # SPARQL query
            sampleList = self.fantom5NP.get_sample(cageCluster)
            for sample in sampleList:
                samples.add(sample)

        return samples


if __name__ == "__main__":
    """VCFAnnotator main"""

    #test = VCFAnnotator('/home/rajaram/work/rd-connect-vcf-annotator/input/UseCases/DNC0040.allchr.snpEff.p.vcf.gz', '/home/rajaram/work/rd-connect-vcf-annotator/output/output1.vcf')
    #test = VCFAnnotator('/Users/mark/rdconnect/input/UseCases/DNC0040.allchr.snpEff.p.vcf.gz', '/tmp/output1.vcf')
    test = VCFAnnotator(sys.argv[1], sys.argv[2], sys.argv[3])
    test.add_annotation()
