import urllib2, re
from pushbullet import PushBullet

api_key = "v1vPiFeYJ9xD5ueb9OYzoC20zVE8z4m5BPujxa3ey3kdw"
pb = PushBullet(api_key)

leerlingnummer = 1102053

url = "http://gepro.nl/roosters/rooster.php?leerling=" + str(leerlingnummer) + "&type=Leerlingrooster&afdeling=schooljaar2014-2015_OVERIG&wijzigingen=1&school=1814"
htmlPage = urllib2.urlopen(url).read()
parts = []
stage = 0
changePat = re.compile('class="tableCell(New|Removed)">(y([0-9]+)|[a-z]+)')
hourPat = re.compile('width="50" class="tableHeader">([0-9])e uur')
for change in re.finditer(changePat, htmlPage):
    if change.group(1) == "Removed":
        parts.append([change.group(2)])
        hour = re.findall(hourPat, htmlPage[:change.start()])[-1]
        parts[-1].append(hour)
    else:
        stage += 1
        if stage == 1:
            parts.append([change.group(2)])
        else:
            parts[-1].append(change.group(2))
        if stage == 3:
            stage = 0
            hour = re.findall(hourPat, htmlPage[:change.start()])[-1]
            parts[-1].append(hour)

text = ""
for part in parts:
    if len(part) == 4:
        text += part[-1] + "e uur " + part[0] + " " + part[1] + " " + part[2] + "\n"
    else:
        text += part[-1] + "e uur " + part[0] + "\n"

print text
#success, push = pb.push_note("Rooster wijzigingen", text)