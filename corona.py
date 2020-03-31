from pathlib import Path
import requests
from bs4 import BeautifulSoup
import os.path
from os import path
import json


def send2slack(payload):
    url = "htt ps://hooks .slack.com/services /TPMAJ1G13/B0115 PL8MHV /RQb9XKGAnDG 8ph5BUYs bJamL"
    url = url.replace(" ", "")
    headers = {
        'Content-type': 'application/json',
        'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text.encode('utf8'))


URL = 'https://www.mohfw.gov.in/'
page = requests.get(URL)


soup = BeautifulSoup(page.content, 'html.parser')
results = soup.findAll("span", {"class": "icount"})

passenger = results[0].text
active = int(results[1].text)
cured = int(results[2].text)
death = int(results[3].text)
migrated = int(results[4].text)

mortality = round((death / (active + cured + death + migrated)) * 100, 1)

total = active + cured + death + migrated
ason = soup.find("div", {"class": "information_block"}
                 ).findNext('p').contents[0].text


x = """ {{ "data":{{ "passenger":"{0}", "active": {1}, "cured": {2}, "death": {3}, "migrated": {4}, "total": {5}, "ason": "{6}" }},
           "slackdata": {{ 
	"blocks": [
		{{
			"type": "section",
			"text": {{
				"type": "mrkdwn",
				"text": "*CORONA UPDATE*\\nUpdated Corona Stats in India:\\n*<https://www.mohfw.gov.in/|*{6}>*"
			}}
		}},
		{{
			"type": "section",
			"fields": [
				{{
					"type": "mrkdwn",
					"text": "*Total Cases:*\\n{5}"
				}},
				{{
					"type": "mrkdwn",
					"text": "*Active:*\\n{1}"
				}},
				{{
					"type": "mrkdwn",
					"text": "*Cured:*\\n{2}"
				}},
				{{
					"type": "mrkdwn",
					"text": "*Death:*\\n{3}"
				}},
				{{
					"type": "mrkdwn",
					"text": "*Migrated:*\\n{4}"
				}},
				{{
					"type": "mrkdwn",
					"text": "*Mortality:*\\n{7}%"
				}}
			]
		}}
	]
           }}
 }} """

x = x.format(passenger, active, cured, death, migrated, total, ason, mortality)
jsonx = json.loads(x)

print(total)
print(ason)
home = str(Path.home()) + "/corona.txt"

if path.exists(home):
    print("File is there")
    with open(home) as f:
        data = json.load(f)
        if int(data['data']['total']) != total:
            # print(jsonx['slackdata'])
            send2slack(json.dumps(jsonx['slackdata']))
        else:
            print("Not supposed to send")
else:
    send2slack(json.dumps(jsonx['slackdata']))


f = open(home, "w")
f.write(x)
f.close()

