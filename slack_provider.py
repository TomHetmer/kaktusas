# this file implements a basic kaktusas Slack provider
import requests, json

# Set the SECRET_URL to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
SECRET_URL='https://hooks.slack.com/services/'

def alarma(aux=''):

  slack_data = {'text': aux}

  response = requests.post(
      SECRET_URL, data=json.dumps(slack_data),
      headers={'Content-Type': 'application/json'},
      timeout=30
  )

  if response.status_code != 200:
      raise ValueError(
          'Request to slack returned an error %s, the response is:\n%s'
          % (response.status_code, response.text)
      )


if __name__ == "__main__":
  alarma('Testing')
