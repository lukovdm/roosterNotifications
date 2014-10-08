import urllib2, re
from pushbullet import PushBullet
from operator import itemgetter

api_key = "v1vPiFeYJ9xD5ueb9OYzoC20zVE8z4m5BPujxa3ey3kdw"
pb = PushBullet(api_key)

leerlingnummer = 1101625

url = "http://gepro.nl/roosters/rooster.php?leerling=" + str(
    leerlingnummer) + "&type=Leerlingrooster&afdeling=schooljaar2014-2015_OVERIG&wijzigingen=1&school=1814"
htmlPage = urllib2.urlopen(url).read()
parts = []
stage = 0
changePat = re.compile('class="tableCell(New|Removed)">(y([0-9]+)|[a-z]+)')
hourPat = re.compile('width="50" class="tableHeader">([0-9])e uur')
dayPat = re.compile('<td align="left" width="auto" class="tableCell">')
for change in re.finditer(changePat, htmlPage):
    if change.group(1) == "Removed":
        parts.append([change.group(2)])
        for tempHour in re.finditer(hourPat, htmlPage[:change.start()]):
            hour = tempHour
        parts[-1].append(hour.group(1))
        day = re.findall(dayPat, htmlPage[hour.end():change.start()])
        parts[-1].append(len(day))
    else:
        stage += 1
        if stage == 1:
            parts.append([change.group(2)])
        else:
            parts[-1].append(change.group(2))
        if stage == 3:
            stage = 0
            for tempHour in re.finditer(hourPat, htmlPage[:change.start()]):
                hour = tempHour
            parts[-1].append(hour.group(1))
            day = re.findall(dayPat, htmlPage[hour.end():change.start()])
            parts[-1].append(len(day))

days = ["Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag"]
text = ""
parts = sorted(parts, key=itemgetter(-1))
for part in parts:
    text += str(days[part[-1]-1]) + " " + part[-2] + "e uur "
    if len(part) == 5:
        text += part[0] + " " + part[1] + " " + part[2] + "\n"
    else:
        text += part[0] + "\n"

print text
# success, push = pb.push_note("Rooster wijzigingen", text)