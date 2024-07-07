import streamlit as st
import matplotlib.pyplot as plt
import joblib
import numpy as np
import pandas as pd
from joblib import load
import matplotlib.pyplot as plt
st.set_page_config(layout="wide")
model = load('my_model.joblib')
st.markdown("<h1 style = 'color:Gold; Text-align: Center; font-size: 35px;'>Pakistan Super League (PSL) Win Predictor</h1>", unsafe_allow_html=True)

# Display text
st.write("Welcome to your first Streamlit app!")

with st.form("entry_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    Team1 = col1.selectbox(
        'Select Team Batting First',
        ('Islamabad United', 'Karachi Kings', 'Lahore Qalandars', 'Multan Sultans', 'Peshawar Zalmi', 'Quetta Gladiators')
    )

    Team2 = col2.selectbox(
        'Select Team Batting Second',
        ('Karachi Kings', 'Islamabad United', 'Lahore Qalandars', 'Multan Sultans', 'Peshawar Zalmi', 'Quetta Gladiators')
    )


    target = col1.number_input('Target For the Team Batting Second', 110)

    cur_runs = col2.number_input('Current Runs of the Team Batting Second', 10)

    wickets = col1.number_input('Current Wickets of the Team Batting Second', min_value=0, max_value=10, value=3)

    overs = col2.text_input('Current Overs Played by the Team Batting Second', 5.5)
    overs=overs.split(".") # type: ignore
    print(overs)
    if len(overs)==1:
        balls=int(overs[0])*6
    else:
        balls=int(overs[0])*6 + int(overs[1])# type: ignore
    balls_left=120-int(balls)
    runs_left=target-cur_runs
    submitted= st.form_submit_button("Predict Win Percentage")
if submitted:
    current = {
        "wickets": wickets,
        "balls_left" :balls_left,
        "runs_left":runs_left
    }
    
    X_test = pd.DataFrame(current, index=[0])
    
    pred = model.predict_proba(X_test)
    
    # Display the prediction

    win_proba = pred[0][1]
    loss_proba = pred[0][0]
    labels = [Team2+' win %', Team1+' win %'] #type:ignore
    sizes = [win_proba, loss_proba]
    colors = ['springgreen', 'cornflowerblue']
    explode = (0.1, 0)
    fig, ax = plt.subplots(figsize=(4,4))  # Create a figure and axes
    fig.set_facecolor('dimgrey')

    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)

    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
     
        with col2:
            st.success(f"Predicted win percentage is {pred[0][1]*100}%")

            st.pyplot(fig)

            st.success(f"Interpretation: There is a {round(pred[0][0] * 100)}% chance the team batting second ({Team2}) is going to lose (or the first team ({Team1}) is going to win) and a {round(pred[0][1] * 100)}% chance that ({Team2}) will win.")