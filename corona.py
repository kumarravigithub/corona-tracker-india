from pathlib import Path
import requests
from bs4 import BeautifulSoup
import os.path
from os import path
import json

def send2slack(payload):
    url = "https://hooks.slack.com/services/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"

    # payload = "{\n\t\"blocks\": [\n\t\t{\n\t\t\t\"type\": \"section\",\n\t\t\t\"text\": {\n\t\t\t\t\"type\": \"mrkdwn\",\n\t\t\t\t\"text\": \"Updated Corona Stats in India:\\n*<https://www.mohfw.gov.in/|*As on 30 March 2020, 09.30 PM & District wise details awaited.>*\"\n\t\t\t}\n\t\t},\n\t\t{\n\t\t\t\"type\": \"section\",\n\t\t\t\"fields\": [\n\t\t\t\t{\n\t\t\t\t\t\"type\": \"mrkdwn\",\n\t\t\t\t\t\"text\": \"*Total Cases:*\\n1251\"\n\t\t\t\t},\n\t\t\t\t{\n\t\t\t\t\t\"type\": \"mrkdwn\",\n\t\t\t\t\t\"text\": \"*Active:*\\n1117\"\n\t\t\t\t},\n\t\t\t\t{\n\t\t\t\t\t\"type\": \"mrkdwn\",\n\t\t\t\t\t\"text\": \"*Cured:*\\n101\"\n\t\t\t\t},\n\t\t\t\t{\n\t\t\t\t\t\"type\": \"mrkdwn\",\n\t\t\t\t\t\"text\": \"*Death:*\\n32\"\n\t\t\t\t},\n\t\t\t\t{\n\t\t\t\t\t\"type\": \"mrkdwn\",\n\t\t\t\t\t\"text\": \"*Migrated:*\\n1\"\n\t\t\t\t},\n\t\t\t\t{\n\t\t\t\t\t\"type\": \"mrkdwn\",\n\t\t\t\t\t\"text\": \"*Mortality:*\\n2.3%\"\n\t\t\t\t}\n\t\t\t]\n\t\t}\n\t]\n}"
    headers = {
    'Content-type': 'application/json',
    'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data = payload)

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


