import json
import time

def hello(event, context):
    
    print("Sleeping for 4 seconds!")
    time.sleep(4)
    print("Done.")

    return "Lambdas are Great!"
