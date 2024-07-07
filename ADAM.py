import streamlit as st
import pandas as pd
from pickle import load
import pickle
import numpy as np
import math as m
from PIL import Image
import os
from glob import glob

st.header("Advanced corrodeD pipe structurAl integrity systeM (ADAM)")

st.sidebar.header('User Input Parameters')


def user_input_features():
    pipe_thickness = st.sidebar.number_input('Pipe Thickness, t (mm)')
    pipe_diameter = st.sidebar.number_input('Pipe Diameter, D (mm)')
    pipe_length = st.sidebar.number_input('Pipe Length, L (mm)')
    corrosion_length = st.sidebar.number_input('Corrosion Length, Lc (mm)')
    corrosion_depth = st.sidebar.number_input('Corrosion Depth, Dc (mm)')

    UTS_sel = st.sidebar.radio('UTS (MPa)', ('235','355','440')) 
    if UTS_sel=='235': UTS=235
    elif UTS_sel=='355': UTS=355
    elif UTS_sel=='440': UTS=440

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


# Calculate burst pressure Pb_PCORR
Pb_PCORR = (2*t*UTS/(D))


user_input={'t (mm)': "{:.2f}".format(t),
            'D (mm)': "{:.2f}".format(D),
            'L (mm)': "{:.2f}".format(L),
            'Lc (mm)': "{:.2f}".format(Lc),
            'Dc (mm)': "{:.2f}".format(Dc),
            'UTS (MPa)': "{:.2f}".format(UTS)}
user_input_df=pd.DataFrame(user_input, index=[0])
st.subheader('User Input Parameters')
st.write(user_input_df)

calculated_param={'Pb_PCORR (MPa)': "{:.2f}".format(Pb_PCORR)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Calculated Corrorded Pipe Burst Pressure via PCORR Guideline')
st.write(calculated_param_df)

st.subheader('Nomenclature')
st.write('P is the beam load magnitude; L is the beam span length; b is the beam breadth; h is the beam height; E is the beam elastic modulus; Fy is the beam yield strength.')

st.subheader('Reference')
st.write('Merrill C.W. Lee, Rozetta M. Payne, Donald W. Kelly, Rodney S. Thomson b, Determination of robustness for a stiffened composite structure using stochastic analysis, Composite Structures 86 (2008) 78 -84, https://doi:10.1016/j.compstruct.2008.03.036')
st.markdown('[Pre-Test](https://forms.gle/wPvcgnZAC57MkCxN8)', unsafe_allow_html=True)
