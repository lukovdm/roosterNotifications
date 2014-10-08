import urllib2, re
from pushbullet import PushBullet

api_key = "v1vPiFeYJ9xD5ueb9OYzoC20zVE8z4m5BPujxa3ey3kdw"
pb = PushBullet(api_key)

leerlingnummer = 1102053

url = "http://gepro.nl/roosters/rooster.php?leerling=" + str(leerlingnummer) + "&type=Leerlingrooster&afdeling=schooljaar2014-2015_OVERIG&wijzigingen=1&school=1814"
htmlPage = urllib2.urlopen(url).read()
parts = []
stage = 0
pattern = re.compile('class="tableCell(New|Removed)">(y([0-9]+)|[a-z]+)')
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

text = ""
for part in parts:
    if len(part) == 3:
        text += part[0] + " " + part[1] + " " + part[2] + "\n"
    else:
        text += part + "\n"

success, push = pb.push_note("Rooster wijzigingen", text)