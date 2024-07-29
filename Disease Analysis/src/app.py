import json
import time
import streamlit as st
import pandas as pd
from utils import analyze_symptoms


st.header('Disease Analysis', divider='red')

col1, col2 = st.columns([1,1])

with col1:
    age = st.number_input(label="Enter your age:",min_value=1,max_value=100)
with col2:
    gender = st.radio(
        "Select your gender:",
        ["Male","Female"],
        index=None,
    )
symptoms = st.text_input("Enter your symptoms:")
if st.button("Analyze",type="primary"):
    st.title("Result")
    try:
        prediction = analyze_symptoms(gender,age,symptoms)
        if prediction:
            prediction = json.loads(prediction)
            st.title("Description")
            st.write(prediction.get("diseaseDescription"))
            st.title("Side Effects")
            for side_effect in prediction.get("sideEffects"):
                st.markdown("- " + side_effect)
            st.title("Statistics")
            plot1, plot2 = st.columns([1,1])
            with plot1:

                x = list(prediction.get("cases").keys())
                y = list(prediction.get("cases").values())
                st.write(f"Cases over last {len(x)-1} years")
                st.line_chart(pd.DataFrame(y,x))

            with plot2:
                st.write(f"Deaths over last {len(x)-1} years")
                x = list(prediction.get("deaths").keys())
                y = list(prediction.get("deaths").values())
                st.scatter_chart(pd.DataFrame(y,x))
            st.markdown(f'**Recovery rate:** {prediction.get("recoveryRate")}')
            st.title("Treatment")
            st.write(prediction.get("treatment"))
            st.divider()
            st.caption(prediction.get("fact"))

    except ValueError:
        pass
