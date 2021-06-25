import csv
import json
import os

name_list = []
umlaute = { "Ä":"Ae", 
            "ä":"ae",
            "Ö":"Oe",
            "ö":"oe",
            "Ü":"Ue",
            "ü":"ue",
            "ß":"ss",
        }


with open ("Chatbot IT-Anwenderprobleme - dialogflow.csv", encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=",")
    for row in csv_reader:
        name_list.append(row)
        #print(row['Name Intent / Problem'])

#print(name_list)

#Wenn der Ordner "data" noch nicht existiert, wird er angelegt
if not os.path.exists('./data/'):
    os.makedirs('./data/')

for entry in name_list:
    intentname = ""
    intentname = entry['Name Intent / Problem']
    
    #Entfernen von Spaces
    # Bulk Upload via ZIP funktioniert nicht, wenn ein Intentname Leerzeichen enthält
    #if intentname != "Default Fallback Intent":
    intentname = intentname.replace(" ", "")
    #Entfernen von Umlauten bzw Sonderzeichen
    for umlaut in umlaute:
        intentname = intentname.replace(umlaut, umlaute[umlaut])
        
    #Fragestellungen sind zwecks Übersichtlichkeit in zwei Kategorien aufgeteilt, Dialogflow behandelt später alle Fragen gleich    
    grundlegend = ""
    grundlegend = entry['Grundlegende Fragestellungen']
    
    training = ""
    training = entry['Alternative Frageformulierungen (Training Phrases)']
    training = training.split("\n")
    
    all_questions = []
    all_questions.append(grundlegend)
    for question in training:
        all_questions.append(question)

    #Antworten, mehrere Antworten sind durch \n\n getrennt
    response = entry["Antwort (Textform)"]
    response = response.split("\n\n")
    print(response)

    # Aufbau von messages
    '''
    "messages" : [
    {
        "type": 0,
        "lang" : "de",
        "speech" : ""
    }
    ],
    '''
    response_list = []
    for line in response:
        response_list.append({"type": 0, "lang": "de", "speech": line })
    
    intentdict = {}
    
    if intentname:
        try:

            with open ("./data/" + intentname + ".json", mode='w') as jsonf:
                #Antworten
                intentdict = {
    
                'id' : "" ,
                'name' : intentname,
                'auto' : True,
                'contexts' : [],
                "responses" : [
                {
                    'resetContexts': False,
                    'action' : intentname,
                    'affectedContexts' : [],
                    'parameters' : [],
                    "messages" : response_list,
                    "defaultResponsePlatforms": {},
                    "speech": []
                }
                ],
                "priority": 500000,
                  "webhookUsed": False,
                  "webhookForSlotFilling": False,
                  "fallbackIntent": False,
                  "events": [],
                  "conditionalResponses": [],
                  "condition": "",
                  "conditionalFollowupEvents": []
                }

                json.dump(intentdict, jsonf, indent=2)
    
        except FileNotFoundError:
            continue
        
        if intentname != "DefaultFallbackIntent":
            with open ("./data/" + intentname + "_usersays_de.json", mode='w') as jsonf:
                #Grundfrage + Training Phrases
                all_questions_json = []
                for entry in all_questions:
                    questiondict = {
                    "id": "",
                    "data": [
                        {
                            "text": entry,
                            "userDefined": False
                         }
                    ],
                    "isTemplate": False,
                    "count": 0,
                    "lang": "de",
                    "updated": 0
                    }
                    all_questions_json.append(questiondict)

                json.dump(all_questions_json, jsonf, indent=2)