import requests

'''
Create this script in the root directory of your project.

Use the test_data.json file: [{"text": "...", "true_label": "positive"}, ...]. (Provided at the end of this page)

Your script must read the file, loop through each item, send the text to the running FastAPI service's /predict endpoint (e.g., at http://localhost:8000/predict), and print a final accuracy score.

You may use the requests library from Python to do this.
'''