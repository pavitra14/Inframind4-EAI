import settings
from ImageDescription.Analyser import *
from ImageDescription.utils import ImageEntity
import json
photo = "photo.jpg"
f = open("image_rekognition.txt", "w+")
data = detect_labels_local_file(photo)
imageData = ImageEntity(data)
print(imageData)
f.write(json.dumps(data))
f.close()
