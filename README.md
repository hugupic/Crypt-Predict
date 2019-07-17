# Crypt Predict
The aim of the project is to be able to predict with some degree of accuracy the future prices of Bitcoin, Ethereum and Litecoin. However it is intended to be designed in a manner that it would be simple for any Developer to implement any Cryptocurrency they wish. The process of generating this prediction should be kept as simple as possible to allow for users of all experience to utilise the application.

## Docker
[![](https://images.microbadger.com/badges/image/hugupic/crypt-predict.svg)](https://microbadger.com/images/hugupic/crypt-predict "Get your own image badge on microbadger.com") [![](https://images.microbadger.com/badges/version/hugupic/crypt-predict.svg)](https://microbadger.com/images/hugupic/crypt-predict "Get your own version badge on microbadger.com")

  You can find a docker of this project at hugupic/crypt-predict

## Installation
1. Clone the project.
`git clone https://github.com/hugupic/crypt-predict.git`
2. Navigate to directory
`cd crypt-predict`
3. Install the requirements.
`pip install -r requirements.txt`

## Web Application Startup : Linux Shell
1. Navigate to the directory containing the application.
2. Open a shell window within this directory.
3. Set the environment variable.
`export FLASK_APP="app.py"`
4. Launch the flask application.
`python -m flask run --host=0.0.0.0`

## Data Collection Startup : Linux Shell
1. Navigate to the directory containing the application.
2. Open a shell window within this directory.
3. Start the data collection script.
`python Data_Collection.py`

## Slack Configuration
1. Navigate to the directory containing the application.
2. Write the provided API token for your Slack Workspace in SLACK_TOKEN.txt.
3. The default slack channel is #notifications, you can change that in Slack_notify.


## References
[1] Devavrat Shah, Kang Zhang. *Bayesian Regression and Bitcoin* https://arxiv.org/pdf/1410.1231v1.pdf 
