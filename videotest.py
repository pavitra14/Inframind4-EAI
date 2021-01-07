import settings
from VideoDescription.Analyser import analyse

video_name = "bezos_vogel.mp4"
video_url = "https://dhei5unw3vrsx.cloudfront.net/videos/bezos_vogel.mp4"
f = open("video_rekognition.txt", "w+")
data = analyse(video_name, video_url)
f.write(data)
f.close()
print(data)