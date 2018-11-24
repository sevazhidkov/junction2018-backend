import os
import dialogflow_v2 as dialogflow

import measures

PROJECT_ID = 'sauna-v3'

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './google_creds.json'

def detect_intent_texts(project_id, session_id, texts, language_code='en'):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(PROJECT_ID, 0)

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))


def analyze_message(text):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(PROJECT_ID, 0)

    text_input = dialogflow.types.TextInput(
        text=text, language_code='en')

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    if response.query_result.intent.display_name == 'karaoke':
        type = 'karaoke'
    else:
        type = 'text'

    text = response.query_result.fulfillment_text

    # TODO: Replacements


    return {'type': type, 'text': text}


# print(analyze_message('how are you'))
