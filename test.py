from sys import argv, exit
import settings


if(len(argv) < 2):
    print("Not Enough arguments: ", len(argv))
    exit()

action = argv[1]
if(action == "train_social"):
    from TextSentiment.train import train_social
    from TextSentiment.utils import *
    print("Starting social training...")
    model = train_social()
    saveModel = "social_model.data"
    print("Saving Model as: ", saveModel)
    storeModel(saveModel, model)
    print("Saved, exiting...")
elif (action == "test_social"):
    from TextSentiment.offline import analyse_sentiment
    text = input("Enter text to analyse: ")
    print(analyse_sentiment(text))
elif(action == "test_aws"):
    from TextSentiment.aws.comprehend import analyse_sentiment
    text = input("Enter text to analyse: ")
    print(analyse_sentiment(text))
elif(action == "summary"):
    from TextSummary.Summariser import *
    data = input("Enter Text to Summarise: ")
    print("Summarising....")
    print(generate_summary(data, True, 2))