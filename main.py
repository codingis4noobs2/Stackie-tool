import requests
import streamlit as st
from PIL import Image
import numpy as np
import io

st.set_page_config(layout="wide", page_title="Stackie Tool")

if "first_time" not in st.session_state:
    st.session_state.first_time = False

if not st.session_state.first_time:
    st.balloons()
    st.session_state.first_time = True

st.write("<h1 style='text-align: center;'>Stackie Tool</h1>", unsafe_allow_html=True)
st.write("<h3 style='text-align: center;'>A tool designed for stackies by stackies :)</h3>", unsafe_allow_html=True)

operation = st.selectbox("What would you like to do?", ("Select an option", "Merge Images", "Access Faucet"))
if operation is not None:
    if operation == "Merge Images":
        img1 = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        img2 = st.file_uploader("Upload another image", type=["png", "jpg", "jpeg"])
        if img1 is not None and img2 is not None:
            i1 = Image.open(img1)
            i2 = Image.open(img2)
            width1, height1 = i1.size
            width2, height2 = i2.size
            new_image = Image.new('RGB', (width1 + width2, height1))
            new_image.paste(i1, (0, 0))
            new_image.paste(i2, (width1, 0))
            img_bytes = io.BytesIO()
            new_image.save(img_bytes, format='PNG')
            st.write("<h1>Merged Image:</h3>", unsafe_allow_html=True)
            st.download_button(label="Download Merged Image", data=img_bytes.getvalue(), file_name="merged_image.png", mime="image/png")
            st.image(new_image, caption="Merged Image", use_column_width=True)
        else:
            pass
    elif operation == "Access Faucet":
        # address = st.text_input("Enter Your Wallet Address")
        # st.write("<h3 style='text-align: center;'>Note: You can request x SepoliaETH every 24hr, If you have more than x SepoliaETH then your request will be denied</h3>", unsafe_allow_html=True)
        # st.write("<h3 style='text-align: center;'>Got any unused SepoliaETH, Donate us at: </h3>", unsafe_allow_html=True)
        # if address is not None:
        #     if len(address) == 42:
        #         if address.startswith("0x"):
        #             pass
        #         else:
        #             st.write("<h3 style='text-align: center;'>Invalid Address</h3>", unsafe_allow_html=True)
        #     else:
        #         st.write("<h3 style='text-align: center;'>Invalid Address</h3>", unsafe_allow_html=True)
        # else:
        #     pass
        st.write("<h3 style='text-align: center;'>Coming soon...</h3>", unsafe_allow_html=True)
else:
    pass
