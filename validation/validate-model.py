import os
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

print('ML model validation')
print()

# Get the users prediction key and URL
print('What is your prediction key?')
prediction_key = input().strip()
print('What is your prediction URL?')
prediction_url = input().strip()

# Decompose the prediction URL
parts = prediction_url.split('/')
endpoint = 'https://' + parts[2]
project_id = parts[6]
iteration_name = parts[9]

# Create the image classifier predictor
prediction_credentials = ApiKeyCredentials(in_headers={'Prediction-key': prediction_key})
predictor = CustomVisionPredictionClient(endpoint, prediction_credentials)

directory = '../model-images/testing-images'

pass_count = 0
fail_count = 0

for entry in os.scandir(directory):
    tag = entry.name[:entry.name.rfind('-')]

    with open(entry.path, 'rb') as image:
        results = predictor.classify_image(project_id, iteration_name, image)

        best_prediction = results.predictions[0]
        
        if best_prediction.tag_name == tag:
            pass_count += 1
        else:
            fail_count += 1

print()

if fail_count > 0:
    print('Validation failed - please check your model')
else:
    print('Validation passed!')
