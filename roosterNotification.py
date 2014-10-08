import urllib2, re

url = "http://gepro.nl/roosters/rooster.php?leerling=1102053&type=Leerlingrooster&afdeling=schooljaar2014-2015_OVERIG&wijzigingen=1&school=1814"
htmlPage = urllib2.urlopen(url).read()

pattern = re.compile('class="tableCell(Removed|New)">(y([0-9]+)|[a-z]+|[0-9])')
for part in re.finditer(pattern, htmlPage):
    print part.group(2)


# done = False
# index = 0
# while not done:
#     index = htmlPage.find('class="tableCellRemoved">vrij', index+1)
#     if index == -1:
#         break
#     print "found one at: " + str(index)

__author__ = 'luko'
