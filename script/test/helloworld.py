__author__ = 'rajaram'


print("Hello ")

file = open("fantom5TSSForGenomicLocation", "r")

content = file.read()

content = content.replace("?variantStart", str(1234))

print(content)