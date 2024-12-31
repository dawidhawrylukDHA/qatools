import sys
import requests
from requests.auth import HTTPBasicAuth
import json

# Your JIRA Cloud details
email = 'dawid.hawryluk@locon.pl'
token = 'Bn47hMxgmZ79Rl9qOBub2744'
url = 'https://jiralocon.atlassian.net/rest/api/3/issue/'

# Headers
headers = {
   "Accept": "application/json",
   "Content-Type": "application/json"
}

# Function to create a task
def create_task(summary, description, project_key, issuetype, epic_id, app_version, sprint):
    payload = json.dumps({
        "update": {},
        "fields": {
            "summary": summary,
            "issuetype": {
            "id": issuetype
            },
            "project": {
            "id": project_key
            },
            "description": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                "type": "paragraph",
                "content": [
                    {
                    "text": description,
                    "type": "text"
                    }
                ]
                }
            ]
            },
            "priority": {
            "id": "3"
            },
            "customfield_10014": epic_id,
            "customfield_10040": [{
                "value": "Opaska SOS Orange"
            }],
            "customfield_10034": [{
                "name": brVersion
            }],
            "customfield_10020": sprint
        }
    })


    response = requests.post(url, headers=headers, data=payload, auth=HTTPBasicAuth(email, token))
    
    if response.status_code == 201:
        print("Task created successfully.")
        print(f"Task ID: {response.json()['id']}")
    else:
        print("Failed to create task.")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

#Data
brVersion = "BR_Android_7.29.9"
epicLink = "GJD-22705"
iterationNumber = "2"
sprint = 239

#Tasks

create_task("Wykonanie testów regresji aplikacji Bezpieczna Rodzina Android w wersji 7.29.7", "Wykonanie testów regresji aplikacji Bezpieczna Rodzina Android w wersji 7.29.7.", 10001, 10012, epicLink, brVersion, sprint)
create_task("[QA] - Testy eksploracyjne oraz smoke testy iteracja  " + iterationNumber, "Testy eksploracyjne oraz smoke testy", 10001, 10002, epicLink, brVersion, sprint)
create_task("[QA] - Testy urządzeń BS iteracja " + iterationNumber, "Testy urządzeń BS: dodawanie urządzenia, edycja, usuwanie, lokalizacja, historia lokalizacji, SOS, połączenia, budzik, kontakty, nasłuch, shareing lokalizacji, oszczędzanie baterii, automatyczna lokalizacja", 10001, 10002, epicLink, brVersion, sprint)
create_task("[QA] - Testy urządzeń BZ iteracja " + iterationNumber, "Testy urządzeń BZ: dodawanie urządzenia, edycja, usuwanie, lokalizacja, historia lokalizacji, SOS, połączenia, nasłuch, shareing lokalizacji, oszczędzanie baterii, automatyczna lokalizacja", 10001, 10002, epicLink, brVersion, sprint)
create_task("[QA] - Testy urządzeń GJD iteracja " + iterationNumber, "Testy urządzeń GJD: dodawanie urządzenia, edycja, usuwanie, lokalizacja, historia lokalizacji, SOS, połączenia, budzik, kontakty, czat, shareing lokalizacji, oszczędzanie baterii, automatyczna lokalizacja", 10001, 10002, epicLink, brVersion, sprint)
create_task("[QA] - Testy ochrony rodzicielskiej iteracja " + iterationNumber, "Testy związane z bliskim, dla którego została uruchomiona ochrona rodzicielska (BSF).", 10001, 10002, epicLink, brVersion, sprint)
create_task("[QA] - Testy funkcjonalności przypomnienia o lekach iteracja " + iterationNumber, "Testy funkcjonalności przypomnienia o lekach.", 10001, 10002, epicLink, brVersion, sprint)
create_task("[QA] - Testy funkcjonalności karty zdrowia iteracja " + iterationNumber, "Testy ciśnienia, saturacji, temperatury, czujnika upadku.", 10001, 10002, epicLink, brVersion, sprint)
create_task("[QA] - Testy autologowania dla różnych sieci iteracja " + iterationNumber, "Testy autologowania dla sieci Play, Orange, Plus, TMobile", 10001, 10002, epicLink, brVersion, sprint)
create_task("[QA] - Testy pakietów iteracja " + iterationNumber, "Testy kupowania pakietów, weryfikacji limitów dla danego pakietu.", 10001, 10002, epicLink, brVersion, sprint)
create_task("[QA] - Testy stref iteracja " + iterationNumber, "Testy dodawania, usuwania i edycji stref.", 10001, 10002, epicLink, brVersion, sprint)
create_task("[QA] - Testy weryfikacji elementów na ekranie udostępniania lokalizacji  iteracja " + iterationNumber, "Weryfikacja długości czasu oraz wiadomości udostępniania lokalizacji.", 10001, 10002, epicLink, brVersion, sprint)
create_task("[QA] - Testy związane z Bliskim iteracja " + iterationNumber, "Testy związane z Bliskim: dodawanie, usuwanie, edycja, SOS, lokalizacja, historia lokalizacji, shareing lokalizacji", 10001, 10002, epicLink, brVersion, sprint)
create_task("[QA] - Testy związane z HomeWiFi iteracja " + iterationNumber, "Testy związane z HomeWiFi.", 10001, 10002, epicLink, brVersion, sprint)
create_task("[QA] - Testy Pakiet Family iteracja " + iterationNumber, "Opis: https://jiralocon.atlassian.net/wiki/spaces/LOCON/pages/1517879312/Pakiet+Family", 10001, 10002, epicLink, brVersion, sprint)
create_task("[QA] - Testy wideo rozmów dla urządzeń GJD iteracja " + iterationNumber, "Testy związane z wideorozmowami dla urządzeń GJD", 10001, 10002, epicLink, brVersion, sprint)
create_task("[QA] - Testy pushy/deeplinków iteracja " + iterationNumber, "Testy pushy/deeplinków.", 10001, 10002, epicLink, brVersion, sprint)
create_task("[QA] - Testy funkcjonalności przyznawania prezentów - iteracja " + iterationNumber, "Opis: https://jiralocon.atlassian.net/wiki/spaces/LOCON/pages/1575976961/Poprawa+ocen+aplikacji", 10001, 10002, epicLink, brVersion, sprint)
create_task("[QA] - Testy funkcjonalności ZST iteracja " + iterationNumber, "Testy związane z funkcjonalnością Znajdź Swój Telefon: https://jiralocon.atlassian.net/wiki/spaces/LOCON/pages/1623359489/ZNAJD+SW+J+TELEFON", 10001, 10002, epicLink, brVersion, sprint)
create_task("[QA] - Testy funkcjonalności StopHejt iteracja " + iterationNumber, "Testy związane z funkcjonalnością StopHejt: https://jiralocon.atlassian.net/wiki/spaces/LOCON/pages/1649737729/STOP+HEJT", 10001, 10002, epicLink, brVersion, sprint)
create_task("[QA] - Testy przyznawania promocji iteracja " + iterationNumber, "Weryfikacja przyznawania promocji dla różnych sieci: TMPL, OPL, PLK, P4.", 10001, 10002, epicLink, brVersion, sprint)
create_task("[QA] - Testy zbierania adresów email " + iterationNumber, "Weryfikacja zbierania adresów email.", 10001, 10002, epicLink, brVersion, sprint)
create_task("[QA] - Testy elementów na mapie - alerty i statusy teleopieki " + iterationNumber, "Weryfikacja elementów na  mapie - alerty i statusy teleopieki.", 10001, 10002, epicLink, brVersion, sprint)

