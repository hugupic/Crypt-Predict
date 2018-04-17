# Crypt Predict

Crypt Predict is my chosen project for my 4th year of college.

The aim of the project is to be able to predict with some degree of accuracy the future prices of Bitcoin, Ethereum and Litecoin. However it is intended to be designed in a manner that it would be simple for any Developer to implement any Cryptocurrency they wish. The process of generating this prediction should be kept as simple as possible to allow for users of all experience to utilise the application.

## Installation
1. Clone the project.
`git clone https://github.com/AdamsEatin/crypt-predict.git`
2. Navigate to directory
`cd crypt-predict`
3. Install the requirements.
`pip install -r requirements.txt`

## Web Application Startup : Windows Powershell
1. Navigate to the directory containing the application.
2. Open a powershell window within this directory.
3. Set the environment variable.
`$env:FLASK_APP="app.py"`
4. Launch the flask application.
`python -m flask run`

## Data Collection Startup : Windows Powershell
1. Navigate to the directory containing the application.
2. Open a powershell window within this directory.
3. Start the data collection script.
`python Data_Collection.py`

## Slack Configuration
1. Navigate to the directory containing the application.
2. Open 'Slack_Notify.py'.
3. Replace the variable 'slack_token' with the provided API token for your Slack Workspace.
4. Replace the content of the 'channel' string with your chosen Slack channel.


## References
[1] Devavrat Shah, Kang Zhang. *Bayesian Regression and Bitcoin* https://arxiv.org/pdf/1410.1231v1.pdf 
