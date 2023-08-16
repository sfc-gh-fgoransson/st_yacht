import streamlit as st
from PIL import Image
import re

image_ferry = Image.open('ferry.png')
image_yacht = Image.open('yacht.png')

ft_to_m = 0.3048

query_strings = st.experimental_get_query_params()
if 'length' in query_strings:
    yacht_length_raw = query_strings['length'][0]
    matches = re.match('([\d,.]*)\W*(ft|m)', yacht_length_raw)
    yacht_length = int(matches[1])
    yacht_length_unit = matches[2]
    st.write(f'{matches[1]} {matches[2]}')
else:
    yacht_length_unit = 'm'
    yacht_length = 30

if not 'yach_length_unit' in st.session_state:
    st.session_state['yach_length_unit'] = 'ft'

if not 'yach_length_ft' in st.session_state:
    st.session_state['yach_length_ft'] = 100

ferry_length_m = 199
ferry_length_ft = round(ferry_length_m / ft_to_m, 0)

st.subheader('Gotland Ferry')
st.image(image_ferry, width=ferry_length_m * 3)
st.markdown(f'**Length**: {ferry_length_m:0.0f} *m* / {ferry_length_ft:0.0f} *ft*')

st.subheader('A very large yacht')
c1, c2 = st.columns([1,5])

with c1:
    yacht_length_unit = st.radio('M or ft', options=['m', 'ft'], label_visibility='collapsed')
with c2:
    yacht_length_min = 1
    yacht_length_max = 400 if yacht_length_unit == 'm' else 1000
    yacht_length_default = yacht_length
    yacht_length = st.slider(f'Yacht length ({yacht_length_unit})', min_value=yacht_length_min, max_value=yacht_length_max, value=yacht_length_default)

    yacht_length_raw = f'{yacht_length}{yacht_length_unit}'
    st.experimental_set_query_params(length=yacht_length_raw)

yacht_length_m = int(yacht_length if yacht_length_unit == 'm' else yacht_length * ft_to_m)
yacht_length_ft = int(max(1, round(yacht_length_m / ft_to_m, 0)))
st.markdown(f'**Length**: {yacht_length_m:0.0f} *m* / {yacht_length_ft:0.0f} *ft*')
st.image(image_yacht, width=max(4, yacht_length_m * 3))

if yacht_length_m < 12:
    st.write('This is a cruiser')
elif yacht_length_m > 220:
    st.write('This is a mega yacht - longer than the worlds largest') 
elif yacht_length_m > 50:
    st.write('This is a mega yacht') 
elif yacht_length_m > 24:
    st.write('This is a superyacht')    
else:
    st.write('This is a yacht')
