import streamlit as st
from PIL import Image
import io

st.set_page_config(layout="wide", page_title="Stackie Tool")

if "first_time" not in st.session_state:
    st.session_state.first_time = False

if not st.session_state.first_time:
    st.balloons()
    st.session_state.first_time = True

st.write("<h1 style='text-align: center;'>Stackie Tool</h1>", unsafe_allow_html=True)
st.write("<h3 style='text-align: center;'>A tool designed for stackies by stackies :)</h3>", unsafe_allow_html=True)

def merge_images(image1, image2, merge_option, adjust_option, color):
    img1 = Image.open(image1)
    img2 = Image.open(image2)

    if adjust_option == 'Crop the biggest':
        if merge_option == 'Horizontally':
            max_width = max(img1.width, img2.width)
            max_height = max(img1.height, img2.height)
            img1 = img1.crop((0, 0, max_width, max_height))
            img2 = img2.crop((0, 0, max_width, max_height))
        else:
            max_width = max(img1.width, img2.width)
            max_height = max(img1.height, img2.height)
            img1 = img1.crop((0, 0, max_width, max_height))
            img2 = img2.crop((0, 0, max_width, max_height))

    if merge_option == 'Horizontally':
        merged_width = img1.width + img2.width
        merged_height = max(img1.height, img2.height)
        merged_img = Image.new('RGB', (merged_width, merged_height), color=color)
        merged_img.paste(img1, (0, 0))
        merged_img.paste(img2, (img1.width, 0))
    else:
        merged_width = max(img1.width, img2.width)
        merged_height = img1.height + img2.height
        merged_img = Image.new('RGB', (merged_width, merged_height), color=color)
        merged_img.paste(img1, (0, 0))
        merged_img.paste(img2, (0, img1.height))

    return merged_img

operation = st.selectbox("What would you like to do?", ("Select an option", "Merge Images", "Access Faucet"))
if operation is not None:
    if operation == "Merge Images":
        file1 = st.file_uploader("Upload the first image file:", type=['png', 'jpg', 'jpeg'])
        file2 = st.file_uploader("Upload the second image file:", type=['png', 'jpg', 'jpeg'])

        # Merge option
        merge_option = st.selectbox("Choose merge option:", ['Horizontally', 'Vertically'])

        # Adjust option
        adjust_option = st.selectbox("Choose image adjustment option:", ['Do not adjust', 'Crop the biggest'])
        color = st.selectbox("Select a background color", ('black', 'white', 'blue', 'red', 'green'))
        submit = st.button("Submit")
        # Check if both files are uploaded
        if submit:
            if file1 and file2:
                # Merge images and display result
                merged_image = merge_images(file1, file2, merge_option, adjust_option, color)
                st.image(merged_image, caption='Merged Image', use_column_width=True)
                st.warning("Don't worry if the images look blurry, they will appear normal once you download them!!")
                # Download button
                merged_img_bytes = io.BytesIO()
                merged_image.save(merged_img_bytes, format='PNG')
                st.download_button('Download Merged Image', data=merged_img_bytes.getvalue(), file_name='merged_image.png')
            else:
                st.warning("Please upload two image files.")
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
