# import PyPDF2
import base64
import io
import os
import re
from typing import List

import pandas as pd
import pypdf
import streamlit as st


def getSubjectNames(text):
    pattern = r"\d{6}\s(.+?)\s\s\*"
    subject_codes = re.findall(pattern, text)
    return subject_codes


def getSubjectCodes(text: str,subjectCodeCount:int) -> list:
    pattern = re.findall(r'[1-4]{1}\d{4,6}\w{1}', text)
    # return a list of top 10 element having maximum occurence
    d = {}
    for i in pattern:
        if i in d:
            d[i] += 1
        else:
            d[i] = 1
    return list(dict(sorted(d.items(), key=lambda item: item[1], reverse=True)).keys())[:subjectCodeCount]


def studentDetails(text: str):
    l = []
    pattern = re.findall(
        r'[STB]\d{9}\s*\w*\s*\w*\s*\w*\s*\w*\w*\s*\w*\s*\w*\s*\w*\s*', text)
    d = {'seat_no': [], 'name': []}
    for i in pattern:
        # split the string
        temp = i.split()
        d['seat_no'].append(temp[0])
        d['name'].append(temp[1]+' '+temp[2]+' '+temp[3])
        dataframe = pd.DataFrame(d)
    return dataframe


def studentSgpa(text: str):
    pattern = re.findall(r'SGPA1\W*\d*\W*\d*', text)
    # SGPA1: 8.3
    d = {'sgpa':[],'score':[]}
    for i in pattern:
        temp = i.split()
        d['sgpa'].append(temp[0])
        d['score'].append(temp[1])
    return pd.DataFrame(d)


def getTabledownloadLink(df: pd.DataFrame,fileName=str):
    """Generates a link allowing the data in a given panda dataframe to be downloaded as an Excel file.
    """
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)
    b64 = base64.b64encode(excel_buffer.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{fileName}">Download Excel file</a>'
    return href


def cleanText(text: str,year: str = 'SE') -> str:
    SE_SUBJECTS_END = [
    "Discrete Mathematics",
    "Digital Electronics and Logic Design",  # Previously "LOGIC DESIGN & COMP. ORG."
    "Fundamentals of Data Structures",       # Previously "DATA STRUCTURES & ALGO."
    "Object Oriented Programming",           # Previously "OBJECT ORIENTED PROGRAMMING"
    "Audit Course 3",                        # Previously "BASIC OF COMPUTERNETWORK"
    "Digital Electronics Lab",               # Previously "LOGIC DESIGN COMP. ORG. LAB"
    "Data Structures Lab",                   # Previously "DATA STRUCTURES & ALGO. LAB"
    "OOP and COMPUTERGraphics Lab",         # Previously "OBJECT ORIENTED PROG. LAB"
    "Skills Lab",                            # Previously "SOFT SKILL LAB"
    "Audit Course 4",                        # Previously "CYBER SECURITY AND LAW"
    "Mathematics III",                       # Previously "ENGINEERING MATHEMATICS-III"
    "Microprocessor",                        # Previously "PROCESSOR ARCHITECTURE"
    "Database Management System",            # Previously "DATABASE MANAGEMENT SYSTEM"
    "COMPUTERGraphics",                     # Previously "COMPUTERGRAPHICS"
    "Software Engineering",                  # Previously "SOFTWARE ENGINEERING"
    "Principles of Programming Languages",   # Previously "PROG. SKILL DEVELOPMENT LAB"
    "Data Structures and Algorithms Lab",    # Previously "DATABASE MGMT. SYSTEM LAB"
    "Microprocessor Lab",                    # Previously "COMPUTERGRAPHICS LAB"
    "Project Based Learning"                 # Previously "PROJECT BASED LEARNING"
]

    
    subjects = [    'DISCRETE MATHEMATICS', 
    'FUND. OF DATA STRUCTURES', 
    'OBJECT ORIENTED PROGRAMMING', 
    'COMPUTERGRAPHICS', 
    'DIGITAL ELEC. & LOGIC DESIGN', 
    'DATA STRUCTURES & ALGO. LAB.', 
    'OOP & COMP. GRAPHICS LAB.', 
    'DIGITAL ELEC. LABORATORY', 
    'BUSINESS COMMUNICATION SKILLS', 
    'HUMANITY & SOCIAL SCIENCE', 
    'ENVIRONMENTAL STUDIES',
    'ENGINEERING MATHEMATICS III', 
    'ENGINEERING MATHEMATICS III', 
    'DATA STRUCTURES & ALGO.', 
    'SOFTWARE ENGINEERING', 
    'MICROPROCESSOR', 
    'PRINCIPLES OF PROG. LANG.', 
    'DATA STRUCTURES & ALGO. LAB.', 
    'MICROPROCESSOR LABORATORY', 
    'PROJECT BASED LEARNING II', 
    'CODE OF CONDUCT', 
    'WATER MANAGEMENT']
    
    # first remove second year subject names
    if year == 'SE':
        for subject in SE_SUBJECTS_END:
            text = text.replace(subject,'')

        for i in subjects:
            text = text.replace(i, '')   
    else:
        for i in subjects:
            text = text.replace(i, '')
        for subject in SE_SUBJECTS_END:
            text = text.replace


    # 
    # BE subjects
    text = text.replace('Design and Analysis of Algorithms', '')
    text = text.replace('Machine Learning', '')
    text = text.replace('Blockchain Technology', '')
    text = text.replace('Cyber Security And Digital Forensics', '')
    text = text.replace('Software Testing And Quality Assurance', '')
    text = text.replace('Laboratory Practice III', '')
    text = text.replace('Laboratory Practice IV', '')
    text = text.replace('Project Stage I', '')
    text = text.replace('Audit Course 7', '')
    text = text.replace('High Performance Computing', '')
    text = text.replace('Deep Learning', '')
    text = text.replace('Natural Language Processing', '')
    text = text.replace('Pattern Recognition', '')
    text = text.replace('Buisness Intelligence', '')
    text = text.replace('Laboratory Practice V', '')
    text = text.replace('Laboratory Practice VI', '')
    text = text.replace('Project Stage II', '')
    text = text.replace('Audit Course 8', '')

    text = text.replace('TOTAL GRADE POINTS / TOTAL CREDITS','')
    text = text.replace('FOURTH YEAR','')
    text = text.replace('SE SGPA','')
    text = text.replace('FE SGPA','')
    text = text.replace('TE SGPA','')
    text = text.replace('FIRST CLASS WITH DISTINCTION','')
    text = text.replace('CGPA','')

    
    # TE subject names
    text = text.replace('DATABASE MANAGEMENT SYSTEMS', '')
    text = text.replace('THEORY OF COMPUTATION', '')
    text = text.replace('SYSTEMS PROGRAMMING AND OPERATING SYSTEM', '')
    text = text.replace('COMPUTERNETWORKS AND SECURITY', '')
    text = text.replace('INTERNET OF THINGS AND EMBEDDED SYSTEMS', '')
    text = text.replace('SOFTWARE PROJECT MANAGEMENT', '')
    text = text.replace('DATABASE MANAGEMENT SYSTEMS LABORATORY', '')
    text = text.replace('COMPUTERNETWORKS AND SECURITY LABORATORY', '')
    text = text.replace('LABORATORY PRACTICE I', '')
    text = text.replace('SEMINAR AND TECHNICAL COMMUNICATION', '')
    text = text.replace('AUDIT COURSE 5', '')
    text = text.replace('DATA SCIENCE AND BIG DATA ANALYTICS', '')
    text = text.replace('WEB TECHNOLOGY', '')
    text = text.replace('ARTIFICIAL INTELLIGENCE', '')
    text = text.replace('CLOUD COMPUTING', '')
    text = text.replace('SOFTWARE MODELING AND ARCHITECTURES', '')
    text = text.replace('INTERNSHIP', '')
    text = text.replace('DATA SCIENCE AND BIG DATA ANALYTICS LABORATORY', '')
    text = text.replace('WEB TECHNOLOGY LABORATORY', '')
    text = text.replace('LABORATORY PRACTICE II', '')
    text = text.replace('AUDIT COURSE 6', '')
    text = text.replace('LAB', '')

    text = text.replace(
        'SAVITRIBAI PHULE PUNE UNIVERSITY ,S.E.(2019 CREDIT PAT.) EXAMINATION, OCT/NOV 2021', '')
    text = text.replace(
        'COLLEGE: [CEGP010530] - D.Y. PATIL COLLEGE OF ENGINEERING,  PUNE', '')
    text = text.replace(
        'BRANCH CODE:  29-S.E.(2019 PAT.)(COMPUTER)', '')
    text = text.replace('DATE : 21 APR 2022 ', '')
    text = text.replace(
        'COURSE NAME                      ISE      ESE     TOTAL      TW       PR       OR    Tot% Crd  Grd   GP  CP  P&R ORD', '')
    text = text.replace(
        'SAVITRIBAI PHULE PUNE UNIVERSITY, S.E.(2015 COURSE) EXAMINATION,MAY 2018', '')
    text = text.replace(
        'SAVITRIBAI PHULE PUNE UNIVERSITY ,T.E.(2019 COURSE) EXAMINATION, OCT/NOV 2021', '')
    text = text.replace(
        'COLLEGE    : D.Y. PATIL COLLEGE OF ENGINEERING,  PUNE', '')
    text = text.replace(
        'COLLEGE: [CEGP010530] - D.Y. PATIL COLLEGE OF ENGINEERING,  PUNE', '')
    text = text.replace(
        'BRANCH CODE: 29-S.E.(2015 PAT.)(COMPUTER)', '')
    text = text.replace(
        'BRANCH CODE: 60-T.E.(2019 PAT.)(COMPUTER)', '')
    text = text.replace('DATE       : 23 JUL 2018', '')
    text = text.replace('DATE : 06 MAY 2022', '')
    text = text.replace(
        '............CONFIDENTIAL- FOR VERIFICATION AND RECORD ONLY AT COLLEGE, NOT FOR DISTRIBUTION.......................................', '')
    text = text.replace(
        '....................................................................................................', '')
    text = text.replace(
        '............                  .......  .......  .......  .......  .......  .......  ...  ...  ...   ... ...  ... ...', '')

    text = text.replace('PAGE :-', '')
    text = text.replace('SEAT NO.', '')
    text = text.replace('SEAT NO.:', '')
    text = text.replace('NAME :', '')
    text = text.replace('MOTHER :', '')
    text = text.replace('PRN :', '')
    text = text.replace('CLG.: DYPP[8]', '')

    text = text.replace('..............................', '')
    text = text.replace('SEM.:1', '')
    text = text.replace('SEM.:2', '')
    text = text.replace(
        'ISE ESE TOTAL TW PR OR TUT Tot% Crd Grd GP CP P&R ORD', '')
    text = text.replace(
        'ISE ESE TOTAL TW PR OR TUT Tot% Crd Grd GP CP P&R ORD', '')
    text = text.replace('DYPP', '')
    text = text.replace('Grd   Crd', '')
    text = text.replace('SEM. 2', '')
    text = text.replace('SEM. 1', '')
    text = text.replace('~', '')
    text = text.replace(' .', '')
    text.replace('~', 'nan')
    text = text.replace('*', ' ')
    text = text.replace(':', ' ')
    text = text.replace('-', 'n')
    text = text.replace('SECOND YEAR SGPA', '')
    text = text.replace('TOTAL CREDITS EARNED ', '')

    text = text.strip()
    return text
# function to display pdf


def displayPDF(file):
    """
    Function to display PDF in Streamlit

    """
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    # Embedding PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

# Issue: https://github.com/Suraj1089/SPPU-Result-Convertor/security/dependabot/17
# Migrate to pypdf
# @st.cache_resource
# def pdfToText(path):
#     pdfreader = PyPDF2.PdfReader(path) 
#     no_of_pages = len(pdfreader.pages)
#     with open('final_txt.txt', 'w') as f:
#         for i in range(0, no_of_pages):
#             # pagObj = pdfreader.getPage(i) # deprecated
#             pagObj = pdfreader.pages[i]
#             f.write(pagObj.extract_text())
#     with open('final_txt.txt', 'r') as f:
#         text = f.read()
#     if os.path.exists("final_txt.txt"):
#         # os.remove("final_txt.txt")
#         return text


@st.cache_resource
def pdfToText(path):
    reader = pypdf.PdfReader(path)
    noOfPages = len(reader.pages)
    with open('extractedText.txt','w') as file:
        for line in range(0,noOfPages):
            page = reader.pages[line]
            file.write(page.extract_text())
    with open('extractedText.txt','r') as file:
        text = file.read()
    if os.path.exists('extractedText.txt'):
        os.remove('extractedText.txt')
        pass
    return text


def showUploadedFile(file):
    f = pd.read_csv(file)
    return f


def cleanMarks(text: str, subject_codes) -> dict:
    """
    This function will clean the marks from the pdf file.
    """
    # 
    for codes in subject_codes.keys():
        # Marks pattern
        pattern = re.findall(
            fr'{codes}[A-Z]?\s+\w+[\/!#&$@ \*~]*\w*\s*\w*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\+]*\w*\s*\+*\w*\s*\+*\w*\s*\w*\+*\s*\w*\s*\+*\w*\s', text)

        # dataframe column names
        d = {'subject': [], 'ISE': [], 'ESE': [], 'TOTAL': [], 'TW': [], 'PR': [], 'OR': [], 'TUT': [], 'Tot%': [], 'Crd': [], 'Grd': [], 'GP': [], 'CP': [], 'P&R': [], 'ORD': []}

        
        # uncomment to log the data
        # with open('patern.txt', 'w') as patt:
        #     patt.write(str(pattern))
        for index,i in enumerate(pattern):
            temp = i.split()
            # print(len(temp))
            # max_lenght = 
            if len(temp) < 13:
                while len(temp)!=13:
                    temp.append(' ')
            
        
            d['subject'].append(temp[0])
            d['ISE'].append(temp[1])
            d['ESE'].append(temp[2])
            d['TOTAL'].append(temp[3])
            d['TW'].append(temp[4])
            d['PR'].append(temp[5])
            d['OR'].append(temp[6])
            d['TUT'].append(temp[7])
            d['Tot%'].append(temp[8])
            d['Crd'].append(temp[9])
            d['Grd'].append(temp[10])
            d['GP'].append(temp[11])
            d['CP'].append(temp[12])
            d['P&R'].append(temp[13])
            d['ORD'].append(temp[14])

        dataframe = pd.DataFrame(d)
        subject_codes[codes] = dataframe

    return subject_codes

        

