import csv
import json

name_list = []

with open ("Chatbot IT-Anwenderprobleme - Sammlung IT-Anwenderprobleme.csv") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=",")
    for row in csv_reader:
        name_list.append(row)
        print(row['Name Intent / Problem'])

print(name_list)

for entry in name_list:
    intentname = ""
    intentname = entry['Name Intent / Problem']
    
    grundlegend = ""
    grundlegend = entry['Grundlegende Fragestellungen']
    
    training = ""
    training = entry['Alternative Frageformulierungen (Training Phrases)']
    training = training.split("\n")
    
    all_questions = []
    all_questions.append(grundlegend)
    for question in training:
        all_questions.append(question)
    
    speech = []
    speech.append(entry['Antwort (Textform)'])
    
    intentdict = {}
    
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
                "messages" : [
                    {
                        "type": 0,
                        "lang" : "de",
                        "speech" : speech
                    }
                ],
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
             

            
