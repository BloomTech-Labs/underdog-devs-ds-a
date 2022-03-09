# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: Python 3.9.5 ('gpu_test-Xfg6MU-e')
#     language: python
#     name: python3
# ---

import requests
import pandas as pd
from dotenv import load_dotenv
from os import getenv


# personal token can be obtained at  
# https://calendly.com/integrations/api_webhooks

class Calendly:
    load_dotenv()
    URL='https://api.calendly.com'
    TOKEN=getenv("TOKEN")
    headers = {"Authorization": f"Bearer {TOKEN}"}
    def __init__(self):
        self.organization = self.get_current_user()['resource']['current_organization']

    def get_user(self,uuid):
        response = requests.get(url=f'{self.URL}/users/{uuid}',
                                headers=self.headers,)
        return response.json()
    
    def get_current_user(self):
        response = requests.get(url=f'{self.URL}/users/me',
                                headers=self.headers)
        return response.json()
    
    def get_event_types(self):
        response = requests.get(url=f'{self.URL}/event_types',
                                headers=self.headers,
                                json={'organization':self.organization})
        return response.json()
    
    def get_event(self):
        response = requests.get(url=f'{self.URL}/scheduled_events',
                                headers=self.headers,
                                json={'organization':self.organization})
  
        return response.json()
    
    def get_event_invitee(self,uuid):
        response = requests.get(url=f'{self.URL}/scheduled_events/',
                                headers=self.headers,
                                json={'organization':self.organization,
                                      'uuid':uuid})
        return response.json()
    
    def get_count_events(self):
        response = requests.get(url=f'{self.URL}/event_types',
                                headers=self.headers,
                                json={'organization':self.organization})
        return f"You have {len(response.json()['collection'])} events today"
    
    def __call__(self):
        return f'You have {self.get_count_events()} events today'


calendly=Calendly()
calendly()

# calendly.get_current_user()
calendly.get_user('')

pd.DataFrame([i for i in calendly.get_event_types()['collection']],
             columns=['active', 'created_at','description_plain', 
                    'duration', 'internal_note', 'kind', 'name',
                    'profile', 'scheduling_url', 'slug', 'type', 'uri'] )

calendly.get_event_invitee('')

calendly.get_event_types()
