import requests
import openai as ai
import smtplib
import ssl
from email.message import EmailMessage

LAT = 69
LONG = 69
WEATHER_KEY = "Weather Key"
TEMP_THRESHOLD = -100
HUMIDITY_THRESHOLD = 0
CREATIVITY = 0.7 ## number between 0-2. Lower tends to be a more formal email and higher is more relaxed and gramatically loose
BOSS_NAME='Manager Boss'
MY_NAME='Good Employee'
SENDER='Sending Email'
RECEIVER='Receiving Email'
EMAIL_AUTH='Email Key'
ai.api_key = "sk-Open AI Key"

def main():
    try:
        if not is_good_day(): return "Not a good day to skip work"
    except:
        return "Bad response getting the weather"
    excuse = get_excuse()
    if excuse == '': return "Bad response from GPT"
    send_email(excuse)
    return "Sent email"

def is_good_day():
    global LAT, LONG, WEATHER_KEY, TEMP_THRESHOLD
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LONG}&appid={WEATHER_KEY}'
    response = requests.get(url, {'units': 'imperial'})
    if response.status_code != 200: raise Exception('Bad Response')
    data = response.json()
    if data['main']['temp_min'] > TEMP_THRESHOLD and data['main']['humidity'] > HUMIDITY_THRESHOLD:
        ## and if the sky is clear
        return True
    return False

def generate_gpt_response(prompt):
    global CREATIVITY
    completions = ai.Completion.create(
        engine='text-davinci-003', ## best model from openai
        temperature=CREATIVITY,           
        prompt=prompt,          
        max_tokens=100,           
        n=1,                        
        stop=None,                 
    )
    return completions.choices[0].text

def get_excuse():
    prompt = f"Please make up a non-illness related excuse and write me a colloquial email to my manager, {BOSS_NAME}, informing them that I, {MY_NAME}, \
                cannot work remotely today. Please provide the body of the email only."
    try:
        excuse = generate_gpt_response(prompt)    
    except:
        excuse = ''
    return excuse

def send_email(excuse):
    msg = EmailMessage()
    msg['From'] = SENDER
    msg['To'] = RECEIVER
    msg['Subject'] = "Unable to work today"
    msg.set_content(excuse)

    context = ssl.create_default_context() ## establish a secure connection
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(SENDER, EMAIL_AUTH)
        smtp.sendmail(SENDER, RECEIVER, msg.as_string())
    
    ## tell yourself that you don't have work today here
    ## TODO

if __name__=="__main__":
    response = main()
    print(response)