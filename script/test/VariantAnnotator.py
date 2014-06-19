from vcf.parser import _Info as VcfInfo, field_counts as vcf_field_counts
import vcf
import SPARQLQueries
import sparql
from pyliftover import LiftOver

class VCFTssAnnotation():

    def addTSSInfo(self, vcfInputFile):
        vcf_reader = vcf.Reader(open(vcfInputFile, 'r'))
        vcf_reader.infos['TSSOL'] = VcfInfo('TSSOL', vcf_field_counts['A'], 'String',
                                            'Info indicates whether the variant overlapping with the'
                                            ' transcription start site(TSS)')

        vcf_writer = vcf.VCFWriter(open('output.vcf', 'w'), vcf_reader)

        query = SPARQLQueries.sparqlQueries()

        totalVar = 0
        tssOLVar = 0

        lo = LiftOver('hg38ToHg19.over.chain.gz')

        for record in vcf_reader:
            variantStart = record.start
            variantEnd = record.end
            variantChromosome = record.CHROM
            variantSubType = record.var_subtype
            isOverlapping = False



            # Adding chr prefix to the chromosome
            if "chr" not in variantChromosome:
                variantChromosome = "chr"+str(record.CHROM)

            #liftover from hg20 to hg19
            data = lo.convert_coordinate(variantChromosome, variantStart)

            #print variantChromosome
            print variantStart
            print variantEnd


            if ((data != None)):
                data2 = data.pop()

                variantChromosomehg19 = data2[0]
                variantStarthg19 = data2[1]



                data = lo.convert_coordinate(variantChromosome, variantEnd)
                data2 = data.pop()

                variantEndhg19 = data2[1]



                # SPARQL query
                result = query.getTSS('http://ep.dbcls.jp/fantom5/sparql', variantStarthg19, variantEndhg19, variantChromosomehg19)

                for row in result:

                    values = sparql.unpack_row(row)
                    cageStart = values[1]
                    cageEnd = values[2]

                    if ((variantSubType == 'ins') & ( variantStart > cageStart )):
                        isOverlapping = True
                        tssOLVar = tssOLVar+1
                        break
                    elif ((variantSubType != 'ins') & (cageStart > 0)):
                       isOverlapping = True
                       tssOLVar = tssOLVar+1
                    break

                totalVar = totalVar+1
                record.add_info('TSSOL', [isOverlapping])
            else:
                print "No liftover found for this pos = "+record.ID

            vcf_writer.write_record(record)

            print "No of variants = "+str(totalVar)
            print "No of tss overlapping variants = "+str(tssOLVar)

test = VCFTssAnnotation()
test.addTSSInfo('example.vcf')



