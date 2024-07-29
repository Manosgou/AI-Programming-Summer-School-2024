import os
from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=os.environ.get("API_KEY"),project=os.environ.get("PROJECT"))

def analyze_symptoms(gender,age,symptoms):
    response = client.chat.completions.create(
         model="gpt-3.5-turbo",
        messages=[
                    {"role": "system", "content": '''Analyze the helath symptoms depending on the gender and the age of the given person.
                        And generate a JSON response with the following fiels diseaseDescription,list of sideEffects,dictionary of yearly cases ,dictionary of yearly deaths,recoveryRate,treatment,fact.
                        The response format should be as follows:
                        {
                        "diseaseDescription": "A small description about the disease depending on the symptoms",
                        "sideEffects":["side effect1","side effect2","side effect3"]
                        "cases":{"2012":"Number of cases","2013":"Number of cases":"2014":"Number of cases"}(Continue until the current year,this must be a dictionary),
                        "deaths":"{"2012":"Number of cases","2013":"Number of cases":"2014":"Number of cases"}(Continue until the current year,this must be a dictionary),
                        "recoveryRate":"Percentage of recovery rate(this must be a number followed by the percentage symbol)"
                        "treatment": "A treatment recomendation for the disease",
                        "fact":"A fact about the disease"
                        }'''},
                    {"role": "user", "content": f"A {age} years old {gender} person, with the following symptoms:{symptoms}"}
                    ]
            )
    return response.choices[0].message.content
