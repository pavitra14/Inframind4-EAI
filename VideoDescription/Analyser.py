from pprint import pformat as pprint
import time
import boto3
from botocore.exceptions import ClientError
import requests
from VideoDescription.RekognitionVideo import RekognitionVideo
from VideoDescription.utils import VideoInformation
def analyse(video_name, video_url):
    info = VideoInformation()
    info.add('-'*88)
    info.add("EnterpriseAI Video Analyser")
    info.add('-'*88)

    info.add("Creating Amazon S3 bucket and uploading video.")
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.create_bucket(
        Bucket=f'inframind-eai-{time.time_ns()}',
        CreateBucketConfiguration={
            'LocationConstraint': s3_resource.meta.client.meta.region_name
        })
    video_object = bucket.Object(video_name)
    bezos_vogel_video = requests.get(
        video_url, stream=True)
    video_object.upload_fileobj(bezos_vogel_video.raw)

    rekognition_client = boto3.client('rekognition')
    video = RekognitionVideo.from_bucket(video_object, rekognition_client)

    info.add("Creating notification channel from Amazon Rekognition to Amazon SQS.")
    iam_resource = boto3.resource('iam')
    sns_resource = boto3.resource('sns')
    sqs_resource = boto3.resource('sqs')
    video.create_notification_channel(
        'inframind-eai', iam_resource, sns_resource, sqs_resource)

    info.add("Detecting labels in the video.")
    labels = video.do_label_detection()
    info.add(f"Detected {len(labels)} labels, here are the first twenty:")
    for label in labels[:20]:
        info.add(pprint(label.to_dict()))

    info.add("Detecting faces in the video.")
    faces = video.do_face_detection()
    info.add(f"Detected {len(faces)} faces, here are the first ten:")
    for face in faces[:10]:
        info.add(pprint(face.to_dict()))

    info.add("Detecting celebrities in the video.")
    celebrities = video.do_celebrity_recognition()
    info.add(f"Found {len(celebrities)} celebrity detection events. Here's the first "
          f"appearance of each celebrity:")
    celeb_names = set()
    for celeb in celebrities:
        if celeb.name not in celeb_names:
            celeb_names.add(celeb.name)
            info.add(pprint(celeb.to_dict()))

    info.add("Tracking people in the video. This takes a little longer. Be patient!")
    persons = video.do_person_tracking()
    info.add(f"Detected {len(persons)} person tracking items, here are the first five "
          f"for each person:")
    by_index = {}
    for person in persons:
        if person.index not in by_index:
            by_index[person.index] = []
        by_index[person.index].append(person)
    for items in by_index.values():
        for item in items[:5]:
            info.add(pprint(item.to_dict()))

    info.add("Deleting resources created for the demo.")
    video.delete_notification_channel()
    bucket.objects.delete()
    bucket.delete()
    info.add("All resources cleaned up. Thanks for using our service!")
    info.add('-'*88)

    return str(info)