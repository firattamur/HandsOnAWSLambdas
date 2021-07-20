import json


def hello(event, context):
    
    print("First Lambda Function")
    print("Updated with -> sls deploy function -f hello -> it will just update function not entire stack.")

    return "Lambdas are Great!"
