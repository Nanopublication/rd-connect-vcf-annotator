__author__ = 'rajaram'


import urllib2
import xml.etree.ElementTree as ET

nameSpace = "{http://www.w3.org/2005/Atom}"
positionGenomicIndex = 3
cDNAChangeIndex = 4
dbIDIndex = 5
url = 'http://databases.lovd.nl/shared/api/rest.php/variants/FKTN/unique'
response = urllib2.urlopen(url).read()


#tree = ET.ElementTree(ET.fromstring(response))
tree = ET.parse('lovd_gene.xml')
root = tree.getroot()

file = open("geneList.tsv", "w")
for entry in tree.findall(nameSpace+'entry'):
    text = entry.find(nameSpace+'content').text
    datas = text.split("\n")
    for data in datas:

        if "entrez_id:" in data:
            entrezID = data.replace("entrez_id:", "")

        elif "symbol:" in data:
            geneSymbol = data.replace("symbol:", "")

        elif "id:" in data:
            id = datas[1].replace("id:", "")

        elif "position_start:" in data:
            tempChromosome = data.replace("position_start:", "")
            chromosome = tempChromosome.split(":")[0]
            geneStart = tempChromosome.split(":")[1]

        elif "position_end:" in data:
            tempChromosome = data.replace("position_end:", "")
            geneEnd = tempChromosome.split(":")[1]

    finalData =  (entrezID+"\t"+geneSymbol+"\t"+chromosome+"\t"+geneStart+"\t"+geneEnd)
    finalData = finalData.replace("      ","")
    print finalData
    file.write(finalData)
    file.write("\n")

file.close()




# for entry in tree.findall(nameSpace+'entry'):
#     text = entry.find(nameSpace+'content').text
#     data = text.split("\n")
#     chromosome = data[positionGenomicIndex].replace("position_genomic:", "").split(":")[0]
#     gLocation = data[positionGenomicIndex].replace("position_genomic:", "").split(":")[1]
#     cDNAChange = data[cDNAChangeIndex].replace("Variant/DNA:", "")
#     dbID = data[dbIDIndex].replace("Variant/DBID:", "")
#     #print(dbID+"\t"+cDNAChange+"\t"+chromosome+"\t"+gLocation)