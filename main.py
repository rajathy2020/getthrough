import streamlit as st
import random
from db import conn
from utils import improve_answer, save_profile, is_old_user, analyze


css = """
h1 {
        color: #008080;
        font-size: 36px;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .section {
        margin-top: 20px;
    }
    .label {
        font-size: 18px;
        font-weight: bold;
        margin-right: 20px;
        color: #5e5e5e;
    }
    .value {
        font-size: 24px;
        padding: 10px;
        margin: 10px;
        border-radius: 10px;
        background-color: #f0f0f0;
        display: inline-block;
    }
    .positive {
        color: green;
    }
    .negative {
        color: red;
    }
"""

def app():
    st.set_page_config(page_title="Get Through", page_icon=":pencil:")
    st.write(f"<style>{css}</style>", unsafe_allow_html=True)
    st.write("<h1>Get Through</h1>", unsafe_allow_html=True)


    profile = {}
    name = st.text_input("Enter your name:")
    email = st.text_input("Enter your email:")
    
    profile["name"] = name
    profile["email"] = email

    if not is_old_user(profile):
        work_history = []
        while True:
            with st.expander("Work History"):
                company = st.text_input("Company Name:", key = "name"+ str(len(work_history)))
                position = st.text_input("Position:", key = "position"+ str(len(work_history)))
                responsibilities = st.text_input("Responsibilities:", key = "responsibilities"+ str(len(work_history)))
                start_date = st.date_input("Start Date:", key = "start_date"+ str(len(work_history)))
                end_date = st.date_input("End Date:", key = "end_date"+str(len(work_history)))
                work_history.append({
                    "company": company,
                    "position": position,
                    "start_date": start_date,
                    "end_date": end_date,
                    "responsibilities": responsibilities
                })
            
            add_another = st.button("Add Another Work History", key = str(len(work_history)))
            if not add_another:
                break
    
        profile["work_history"] = work_history

        if st.button("Save Profile"):
            save_profile(profile)

        st.session_state.profile = profile

    job_description = st.text_input("Add job description here:", key = "job_description")
    res = {}
    if st.button("Analyze"):
        try:
            with st.spinner('Wait for it...'):
                res = analyze(profile, job_description)  

                st.session_state.analyze_res = res
                with st.container():
                    for key, value in res['overlap_before'].items():
                        st.write(f"<div class='section'><span class='label'>{key.title()}</span><span class='value'>{value}</span></div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f'This is an error.Please try again {e}', icon="🚨")

    if st.button("Improve Answer"):
        try:
            with st.spinner('Wait for it...'):
                input_req = st.session_state.analyze_res
                res = improve_answer(input_req)  
                with st.container():
                    for key, value in res['overlap_after'].items():
                        st.write(f"<div class='section'><span class='label'>{key.title()}</span><span class='value'>{value}</span></div>", unsafe_allow_html=True)
                st.balloons()

        except Exception as e:
            st.error(f'This is an error.Please try again {e}', icon="🚨")


if __name__ == '__main__':
    app()