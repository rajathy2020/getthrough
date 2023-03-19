from db import conn
import streamlit as st
from recommendation import extract_keywords_from_text, measure_overlap_dict_values, re_write_work_experience

def save_profile(profile):
    name = profile["name"]
    email = profile["email"]
    work_history = profile["work_history"]
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, requests) VALUES (%s, %s, %s)", (name, email,1))
        user_id = cursor.lastrowid

        st.write("user_id", user_id)

        # Insert work history data into the 'work_history' table
        for job in work_history:
            cursor.execute("INSERT INTO work_history (user_id, company, position, responsibilities, start_date, end_date) VALUES (%s, %s, %s, %s, %s, %s)", (user_id, job['company'], job['position'], job["responsibilities"], job['start_date'], job['end_date']))

        conn.commit()
        st.success("Profile saved to MySQL successfully!")
    except Exception as e:
        st.error(f"Error saving profile to MySQL: {str(e)}")
        
def is_old_user(profile):
    return False


res ={
    "work_history_before_kws": {
      "soft_skills": [],
      "technical_skills": [
        "Python",
        "Machine Learning",
        "Excel"
      ],
      "experience": [
        "Data Administrator"
      ],
      "responsibilities": [
        "Managed large volumes of unstructured data",
        "Received public requests in text format and manually categorized them into different types",
        "Built a dashboard using Excel to aggregate key data points and present them in weekly meetings with stakeholders",
        "Using Python and simple machine learning models, built pipeline to transform text-based public requests into digital records",
        "Led a team of three individuals in the development of a running application capable of handling up to 3,000 public requests every day",
        "Continued to evaluate and enhance the machine learning model to improve accuracy and efficiency",
        "Overcame bureaucratic challenges to implement new features and optimize the application"
      ]
    },
    "job_description_kws": {
      "soft_skills": [],
      "technical_skills": [
        "analytics methods",
        "big data",
        "modern software tools",
        "data quality"
      ],
      "experience": [
        "programming"
      ],
      "responsibilities": [
        "solve business-related issues",
        "implement appropriate solutions",
        "accompany SAP-based processes and functions",
        "analyze and process big data",
        "evaluate the knowledge gained to improve data quality"
      ]
    },
    "overlap_before": {
      "soft_skills": 0,
      "technical_skills": 25,
      "experience": 0,
      "responsibilities": 0
    },
    "responsibilities_rewritten": [
      "Managed large volumes of unstructured data and solved business-related issues by implementing appropriate solutions using modern software tools and analytics methods. Evaluated the knowledge gained to improve data quality.",
      "Analyzed and processed big data by applying programming skills and modern software tools. Developed techniques to extract information using OCR-based data pipeline in Python. Continuously evaluated and enhanced the machine learning model to improve accuracy and efficiency.",
      "Led and managed a team of three individuals in the development of a running application capable of handling up to 3,000 public requests every day. Successfully implemented a data-driven approach to improve the efficiency and accuracy of the application. Evaluated the knowledge gained to improve data quality.",
      "Received public requests in text format and manually categorized them into different types. Built a dashboard using Excel to aggregate key data points and present them in weekly meetings with stakeholders. Effectively accompanied SAP-based processes and functions to ensure smooth operations.",
      "Continued to evaluate and enhance the machine learning model to improve accuracy and efficiency, overcoming bureaucratic challenges to implement new features and optimize the application. Applied programming skills and big data knowledge to successfully improve the efficiency and accuracy of the data categorization and aggregation process."
    ],
    "responsibilities_rewritten_kws": {
      "soft_skills": [],
      "technical_skills": [
        "programming",
        "big data",
        "OCR",
        "machine learning"
      ],
      "experience": [
        "data management",
        "software tool implementation",
        "analytics",
        "team management"
      ],
      "responsibilities": [
        "data processing",
        "information extraction",
        "application development",
        "data categorization",
        "dashboard building",
        "process and function accompaniment"
      ]
    },
    "overlap_after": {
      "soft_skills": 0,
      "technical_skills": 33,
      "experience": 12,
      "responsibilities": 16
    }
  }

def analyze(profile, job_description):
    work_history = profile["work_history"]
    responsibilities = [i["responsibilities"] for i in work_history ]
    #st.write(responsibilities)
    work_history_ = ". ".join(responsibilities)
    work_history_kws = extract_keywords_from_text(work_history_)
    #st.write("work_history_kws", work_history_kws)
    job_description_kws = extract_keywords_from_text(job_description)
    #st.write("job_description_kws", job_description_kws)
    overlap_before = measure_overlap_dict_values(work_history_kws, job_description_kws)
    return {
        "work_history_before_kws":work_history_kws,
        "job_description_kws": job_description_kws,
        "overlap_before": overlap_before,
        "responsibilities": responsibilities,
    
    }

def improve_answer(input_request):

    responsibilities = input_request["responsibilities"]
    job_description_kws =  input_request["job_description_kws"]
    work_history_kws =  input_request["work_history_before_kws"]
    overlap_before= input_request["overlap_before"]
    responsibilities_rewritten = re_write_work_experience(responsibilities, job_description_kws)
    #print(st.write("responsibilities_rewritten", responsibilities_rewritten))
    responsibilities_rewritten_ = ". ".join(responsibilities_rewritten)
    responsibilities_rewritten_kws =  extract_keywords_from_text(responsibilities_rewritten_)
    #st.write("work_history_rewritten_kws", work_history_rewritten_kws)
    overlap_after = measure_overlap_dict_values(responsibilities_rewritten_kws, job_description_kws)
    return {
        "work_history_before_kws": work_history_kws,
        "job_description_kws": job_description_kws,
        "overlap_before": overlap_before,
        "responsibilities_rewritten": responsibilities_rewritten,
        "responsibilities_rewritten_kws": responsibilities_rewritten_kws,
        "overlap_after": overlap_after


    }



