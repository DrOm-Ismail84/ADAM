import streamlit as st
import pandas as pd
from pickle import load
import pickle
import numpy as np
import math as m
from PIL import Image
import os
from glob import glob
import matplotlib.pyplot as plt

st.header("Advanced corrodeD pipe structurAl integrity systeM (ADAM)")

st.subheader('Dimensional Parameters')
htp="https://www.researchgate.net/profile/Changqing-Gong/publication/313456917/figure/fig1/AS:573308992266241@1513698923813/Schematic-illustration-of-the-geometry-of-a-typical-corrosion-defect.png"
st.image(htp, caption= "Fig. 1: Schematic illustration of the geometry of a typical corrosion defect.")

st.sidebar.header('User Input Parameters')

def user_input_features():
    pipe_thickness = st.sidebar.number_input('Pipe Thickness, t (mm)', value = 0.01)
    pipe_diameter = st.sidebar.number_input('Pipe Diameter, D (mm)', value = 0.01)
    pipe_length = st.sidebar.number_input('Pipe Length, L (mm)', value = 0.01)
    corrosion_length = st.sidebar.number_input('Corrosion Length, Lc (mm)', value = 0.01)
    corrosion_depth = st.sidebar.number_input('Corrosion Depth, Dc (mm)', value = 0.01)
    UTS = st.sidebar.number_input('Ultimate Tensile Strength, UTS (MPa)', value = 0.01)

    data = {'t (mm)': pipe_thickness,
            'D (mm)': pipe_diameter,
            'L (mm)': pipe_length,
            'Lc (mm)': corrosion_length,
            'Dc (mm)': corrosion_depth,           
            'UTS (MPa)': UTS}
    features = pd.DataFrame(data, index=[0])
    return features


df = user_input_features()

t=df['t (mm)'].values.item()
D=df['D (mm)'].values.item()
L=df['L (mm)'].values.item()
Lc=df['Lc (mm)'].values.item()
Dc=df['Dc (mm)'].values.item()
UTS=df['UTS (MPa)'].values.item()

st.subheader('Nomenclature')
st.write('t is the pipe thickness; D is the pipe diameter; L is the pipe length; Lc is the corrorsion length; Dc is the corrorsion depth; UTS is the pipe material Ultimate Tensile Strength.')

# Calculate burst pressure of intact pipe P Von Mises
Pvm = 4*t*UTS/(m.sqrt(3)*D)

# Calculate burst pressure of intact pipe P Tresca
PTresca = 2*t*UTS/(D)

# Calculate burst pressure of corroded pipe P ASME B31G (2013)
M = m.sqrt(1+0.8*(L/(m.sqrt(D*t)))) #Folias factor

if L < m.sqrt(20*D*t):
    P_ASME_B31G = (2*t*UTS/D)*(1-(2/3)*(Dc/t)/1-(2/3)*(Dc/t)/M)

elif L > m.sqrt(20*D*t):
    P_ASME_B31G = (2*t*UTS/D)*(1-(Dc/t))

# Calculate burst pressure of corroded pipe PDnV
Q = m.sqrt(1+0.31*(Lc)**2/D*t) #Q is the curved fit of FEA results
P_DnV = (2*UTS*t/D-t)*((1-(Dc/t))/(1-(Dc/(t*Q))))

# Calculate burst pressure of corroded pipe P PCORRC Model 
P_PCORRC = (2*t*UTS/D)*(1-Dc/t)

user_input={'t (mm)': "{:.2f}".format(t),
            'D (mm)': "{:.2f}".format(D),
            'L (mm)': "{:.2f}".format(L),
            'Lc (mm)': "{:.2f}".format(Lc),
            'Dc (mm)': "{:.2f}".format(Dc),
            'UTS (MPa)': "{:.2f}".format(UTS)}
user_input_df=pd.DataFrame(user_input, index=[0])
st.subheader('User Input Parameters')
st.write(user_input_df)

# Intact Pipe
calculated_param={'Pvm (MPa)': "{:.2f}".format(Pvm)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Calculated Intact Pipe Burst Pressure via Von Mises')
st.write(calculated_param_df)

calculated_param={'PTresca (MPa)': "{:.2f}".format(PTresca)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Calculated Intact Pipe Burst Pressure via Tresca')
st.write(calculated_param_df)

# Corroded Pipe
calculated_param={'P_ASME_B31G (MPa)': "{:.2f}".format(P_ASME_B31G)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Calculated Corroded Pipe Burst Pressure via ASME_B31G')
st.write(calculated_param_df)

calculated_param={'P_DnV (MPa)': "{:.2f}".format(P_DnV)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Calculated Corrorded Pipe Burst Pressure via DnV')
st.write(calculated_param_df)

calculated_param={'P_PCORRC (MPa)': "{:.2f}".format(P_PCORRC)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Calculated Corrorded Pipe Burst Pressure via PCORRC')
st.write(calculated_param_df)

Pressure = [Pvm, PTresca, P_ASME_B31G, P_DnV, P_PCORRC]
index = ["Pvm (MPa)", "PTresca (MPa)", "P_ASME_B31G (MPa)", "P_DnV (MPa)", "P_PCORRC (MPa)"]
df = pd.DataFrame({"Burst Pressure (MPa)": Pressure}, index=index)

st.pyplot(df.plot.barh(stacked=True).figure)

st.subheader('Reference')
st.write('Xian-Kui Zhu, A comparative study of burst failure models for assessing remaining strength of corroded pipelines, Journal of Pipeline Science and Engineering 1 (2021) 36 - 50, https://doi.org/10.1016/j.jpse.2021.01.008')
st.markdown('[Corroded Pipe Burst Data](https://docs.google.com/spreadsheets/d/1YJ7ziuc_IhU7-MMZOnRmh4h21_gf6h5Z/edit?gid=56754844#gid=56754844)', unsafe_allow_html=True
st.markdown('[Pre-Test](https://forms.gle/wPvcgnZAC57MkCxN8)', unsafe_allow_html=True)
