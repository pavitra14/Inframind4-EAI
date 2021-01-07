from collections import defaultdict
class ImageEntity:
    def __init__(self, response) -> None:
        self.response = response
        self.people = []
        self.entities = defaultdict(list)
        self.summary = ""
        self.analyze()

    def analyze(self):
        status_code = int(self.response['ResponseMetadata']['HTTPStatusCode'])
        if(status_code != 200):
            self.summary = "Request Invalid: Status Code: " + str(status_code)
            return

        for label in self.response['Labels']:
            if label['Name'] == "Person":
                self.people.append((label['Name'], label['Confidence']))
            self.entities[label['Name']].append(label)
        text = "We have found {} person/human entities in the provided image.\n".format(len(self.people))
        text += "There were a total of {} entites found in the image. \n".format(len(self.entities))
        text += "They are as follows: \n"
        i=1
        for entity,data in self.entities.items():
            text+="{}.) {} -> Confidence: {} \n".format(i, entity, data[0]['Confidence'])
            i+=1
        text += "Request ID: {}\n".format(self.response['ResponseMetadata']['RequestId'])
        self.summary = text
    def __str__(self) -> str:
        return self.summary
