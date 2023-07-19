import streamlit as st
from PIL import Image
import io
from web3 import Web3
from web3.middleware import construct_sign_and_send_raw_middleware
import time
from streamlit_ws_localstorage import injectWebsocketCode, getOrCreateUID
import streamlit_ace
import re


st.set_page_config(layout="wide", page_title="Stackie Tool")

if "first_time" not in st.session_state:
    st.session_state.first_time = False

if not st.session_state.first_time:
    st.balloons()
    st.session_state.first_time = True

st.write("<h1 style='text-align: center;'>Stackie Tool</h1>",
         unsafe_allow_html=True)
st.write("<h3 style='text-align: center;'>A tool designed for stackies by stackies :)</h3>",
         unsafe_allow_html=True)


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
        merged_img = Image.new(
            'RGB', (merged_width, merged_height), color=color)
        merged_img.paste(img1, (0, 0))
        merged_img.paste(img2, (img1.width, 0))
    else:
        merged_width = max(img1.width, img2.width)
        merged_height = img1.height + img2.height
        merged_img = Image.new(
            'RGB', (merged_width, merged_height), color=color)
        merged_img.paste(img1, (0, 0))
        merged_img.paste(img2, (0, img1.height))

    return merged_img


provider_url = f"https://sepolia.infura.io/v3/{st.secrets['provider']}"
w3 = Web3(Web3.HTTPProvider(provider_url))
conn = injectWebsocketCode(hostPort='linode.liquidco.in', uid=getOrCreateUID())

def get_main_balance(address):
    balance = w3.eth.get_balance(address)
    balance = Web3.from_wei(balance, 'ether')
    return f"{round(balance, 2)} ETH"

def check_balance(address):
    balance = w3.eth.get_balance(address)
    return balance < w3.to_wei(0.1, 'ether')


def check_prev_req_time():
    prev_req_time = conn.getLocalStorageVal(key='time')
    if not prev_req_time:
        return True
    return time.time() > float(prev_req_time)


def process_tx(address):
    if (check_prev_req_time()):
        if(check_balance(address)):
            time_delay = str(time.time() + 86400.0)
            conn.setLocalStorageVal(key='time', val=time_delay)
            w3.middleware_onion.add(
                construct_sign_and_send_raw_middleware(faucet_acct))
            tx_hash = w3.eth.send_transaction({
                "value": w3.to_wei(0.01, 'ether'),
                "to": address
            })
            st.write(
                "<h3 style='text-align: center;'>Transaction sent </h3>", unsafe_allow_html=True)
            st.write(
                f"<div style='text-align: center;'><a target='_blank' href= 'https://sepolia.etherscan.io/tx/{w3.to_hex(tx_hash)}'>{w3.to_hex(tx_hash)}</a></div>", unsafe_allow_html=True)
        else:
            st.write(
                "<h3 style='text-align: center;'>Transaction not processed: your balance is >0.1 ether</h3>", unsafe_allow_html=True)
    else:
        st.write(
            "<h3 style='text-align: center;'>Only 1 request allowed. Try again after 24 hours</h3>", unsafe_allow_html=True)

def bbcode_formatter(input_text):
    """
    Formats BBCode tags in the input text.
    """
    formatted_text = input_text
    
    # Replace [b] tags with <strong>
    formatted_text = formatted_text.replace("[b]", "<strong>")
    formatted_text = formatted_text.replace("[/b]", "</strong>")
    
    # Replace [i] tags with <em>
    formatted_text = formatted_text.replace("[i]", "<em>")
    formatted_text = formatted_text.replace("[/i]", "</em>")
    
    # Replace [u] tags with <u>
    formatted_text = formatted_text.replace("[u]", "<u>")
    formatted_text = formatted_text.replace("[/u]", "</u>")
    
    url_regex = r'\[url=(.+?)\](.+?)\[/url\]'
    formatted_text = re.sub(url_regex, r'<a href="\g<1>">\g<2></a>', formatted_text)

    return formatted_text

operation = st.selectbox("What would you like to do?",
                         ("Select an option", "Merge Images", "Access Faucet", "BBCode Formatter"))
if operation is not None:
    if operation == "Merge Images":
        file1 = st.file_uploader("Upload the first image file:", type=[
                                 'png', 'jpg', 'jpeg'])
        file2 = st.file_uploader("Upload the second image file:", type=[
                                 'png', 'jpg', 'jpeg'])

        # Merge option
        merge_option = st.selectbox("Choose merge option:", [
                                    'Horizontally', 'Vertically'])

        # Adjust option
        adjust_option = st.selectbox("Choose image adjustment option:", [
                                     'Do not adjust', 'Crop the biggest'])
        color = st.selectbox("Select a background color",
                             ('black', 'white', 'blue', 'red', 'green'))
        submit = st.button("Submit")
        # Check if both files are uploaded
        if submit:
            if file1 and file2:
                # Merge images and display result
                merged_image = merge_images(
                    file1, file2, merge_option, adjust_option, color)
                st.image(merged_image, caption='Merged Image',
                         use_column_width=True)
                st.warning(
                    "Don't worry if the images look blurry, they will appear normal once you download them!!")
                # Download button
                merged_img_bytes = io.BytesIO()
                merged_image.save(merged_img_bytes, format='PNG')
                st.download_button('Download Merged Image', data=merged_img_bytes.getvalue(
                ), file_name='merged_image.png')
            else:
                st.warning("Please upload two image files.")
        else:
            pass
    elif operation == "Access Faucet":
        address = st.text_input("Enter Your Ethereum Wallet Address")
        st.write("<h3 style='text-align: center;'>Note: You can request 0.01 SepoliaETH every 24hr, If you have more than 0.1 SepoliaETH then your request will be denied</h3>", unsafe_allow_html=True)
        st.write("<h3 style='text-align: center;'>Got any unused SepoliaETH, Donate us at: 0xA3DE0DB544c3c5F93e701C7B252D9680716F226d</h3>",
                 unsafe_allow_html=True)

        faucet_acct = w3.eth.account.from_key(st.secrets['k'])
        w3.eth.default_account = faucet_acct.address
        current_balance = get_main_balance(faucet_acct.address)
        st.write(f"<h3 style='text-align: center;'>Current Faucet Balance: {current_balance}</h4>", unsafe_allow_html=True)
        
        if len(address) == 42 and address.startswith("0x"):
            process_tx(address)
        else:
            pass
    elif operation == "BBCode Formatter":
        default_text = "This is [b]bold[/b] text. This is [i]italic[/i] text. This is [u]underlined[/u] text."
        code = streamlit_ace.st_ace(
            value=default_text,
            language="plain_text",
            theme="monokai",
            font_size=14,
            height=300,
            key="editor"
        )
        # Format input text on button click
        if st.button("Format"):
            formatted_text = bbcode_formatter(code)
            st.markdown(formatted_text, unsafe_allow_html=True)
else:
    pass
