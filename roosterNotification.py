import urllib2, re

url = "http://gepro.nl/roosters/rooster.php?leerling=1102053&type=Leerlingrooster&afdeling=schooljaar2014-2015_OVERIG&wijzigingen=1&school=1814"
htmlPage = urllib2.urlopen(url).read()

parts = []
stage = 0
pattern = re.compile('class="tableCell(Removed|New)">(y([0-9]+)|[a-z]+)')
for string in re.finditer(pattern, htmlPage):
    if string.group(1) == "Removed":
        parts.append(string.group(2))
    else:
        stage += 1
        if stage == 1:
            parts.append([string.group(2)])
        else:
            parts[-1].append(string.group(2))
        if stage == 3:
            stage = 0

for part in parts:
    if len(part) == 3:
        print part[0] + " " + part[1] + " " + part[2]
    else:
        print part