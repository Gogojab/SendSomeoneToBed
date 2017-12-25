"""
SendSomeoneToBed

"""

from __future__ import print_function
import random

# 
response_options = [
	"Good night, {name}, sweet dreams",
	"Time for bed, {name}",
        "That's it.  I've had enough.  Everyone has to go to bed. <emphasis level='strong'>NOW!</emphasis>",
        "<amazon:effect name='whispered'> Let's all be quiet so {name} can go to sleep. </amazon:effect>",
        "OK, {name}, up the wooden hill to bedfordshire.",
        "OK, {name}, you can have 5 more minutes",
        "Hey, {name}, come to bed.",
        "Bedtime on the count of 10. <prosody rate='x-slow'>1, 2, 3, 4, 5,</prosody><prosody rate='x-fast'>6 7 8 9 10</prosody>",
        "For the last time, {name}, I said go to <say-as interpret-as='expletive'>bleep</say-as> bed.",
        "{name}, <say-as interpret-as='spell-out'>BED</say-as>, immediately.",
        "<say-as interpret-as='interjection'>aw man</say-as>, time for bed, {name}",
        "<say-as interpret-as='interjection'>good golly</say-as> it is bed for {name}",
        "<say-as interpret-as='interjection'>hip hip hooray</say-as>it is bed time!",
        "bed time, {name}. <break time='3s'/>, <say-as interpret-as='interjection'>just kidding</say-as>",
        "<say-as interpret-as='interjection'>oh my giddy aunt</say-as>, everyone called {name}, go to bed",
        "<say-as interpret-as='interjection'>spoiler alert</say-as>, it is bed time for {name}",
        "<say-as interpret-as='interjection'>tick tock</say-as>, bed isn't going to go to itself",

	]

# --------------- Helpers that build all of the responses ----------------------
def clean_text(text):
    s_list = list(text)
    i = 0
    j = 0
	
    while i < len(s_list):
        # iterate until a left-angle bracket is found
        if s_list[i] == '<':
            while s_list[i] != '>':
                # pop everything from the the left-angle bracket until the right-angle bracket
                s_list.pop(i)
				
            # pops the right-angle bracket, too
            s_list.pop(i)
        else:
            i=i+1
			
    # convert the list back into text
    join_char=''
    return join_char.join(s_list)


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    clean_output = clean_text(output)
    print(clean_output)
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': "<speak>" + output + "</speak>"
        },
        'card': {
            'type': 'Simple',
            'title': "SendSomeoneToBed - " + title,
            'content': "SendSomeoneToBed - " + clean_output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "OK, what is the name of the person to send to bed?"
    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Good night!" 
    session_attributes = {}
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def handle_help_request():
    card_title = "Help Requested"
    speech_output = "Tell me their name, for example, their name is Bob"
    session_attributes = {}
    should_end_session =  False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def list_all_bed_options():
    print("ListAllBedOptions")

    card_title = "ListAllBedOptions"
    speech_output = "Bed options are as follows: "

    for x in response_options:
        speech_output += x + ". break. "

    print(speech_output)

    session_attributes = {}
    should_end_session =  True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))



def get_beddee_response():
    speech_output = "Time for bed, {name}"

    print(str(response_options))

    speech_output = random.choice(response_options)

    return speech_output


def send_someone_to_bed(intent, session):
    session_attributes = {}
    card_title = "Dispatched: " 

    speech_output = get_beddee_response()

    print("speech_output is: " + speech_output)
    print("intent is: " + str(intent))

    if "beddee" in intent["slots"]:

        if "value" in intent["slots"]["beddee"]:
            beddee = intent["slots"]["beddee"]["value"]
            print("beddee =" + beddee)
        else:
            print("no beddee value")
            return(handle_help_request())
    else:
        print("no beddee")
        return(handle_help_request())
   
    card_title = card_title + beddee
    speech_output = speech_output.format(name = beddee)
    
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))



# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == "SendSomeoneToBed":
	return send_someone_to_bed(intent, session)
    elif intent_name == "AMAZON.CancelIntent":
        return handle_session_end_request()
    elif intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name == "AMAZON.HelpIntent":
        return handle_help_request()
    elif intent_name == "ListAllBedOptions":
        return list_all_bed_options()
    else:
        print("invalid intent name=" + intent_name)
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.dd227f04-22dc-4c19-9aa5-e815af9130e4"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
