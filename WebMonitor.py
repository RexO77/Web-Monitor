import streamlit as st
import requests
import time

def check_website_status(url):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        response = requests.get(url, timeout=5)
        status_code = response.status_code

        if response.history:
            redirected_urls = [resp.url for resp in response.history] + [response.url]
            redirect_chain = ' ➔ '.join(redirected_urls)
            if status_code == 200:
                return f"Up (Redirected: {redirect_chain})"
            else:
                return f"Down (Status Code: {status_code}, Redirected: {redirect_chain})"
        else:
            if status_code == 200:
                return 'Up'
            elif status_code == 404:
                return 'Down (Not Found)'
            elif status_code == 403:
                return 'Down (Forbidden)'
            elif status_code == 500:
                return 'Down (Internal Server Error)'
            else:
                return f'Down (Status Code: {status_code})'
    except requests.exceptions.RequestException as e:
        return f'Down ({e})'

def main():
    st.set_page_config(page_title="Website Status Monitor", layout="centered")
    
    # Custom CSS with glowing gradient border for the search bar
    st.markdown("""
        <style>
        /* Background and general styles */
        .stApp {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #1a1a2e 100%);
        }

        /* Glowing gradient border container */
        .gradient-border {
            background: #0b090a;
            padding: 2px;
            border-radius: 10px;
            background-image: linear-gradient(43deg, #4158D0 0%, #C850C0 46%, #FFCC70 100%);
            filter: brightness(120%);
            box-shadow: 0 0 20px rgba(65, 88, 208, 0.6), 
                        0 0 20px rgba(200, 80, 192, 0.6), 
                        0 0 20px rgba(255, 204, 112, 0.6);
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /* Inner container to hold the form elements */
        .inner-container {
            background-color: #0b090a;
            border-radius: 8px;
            padding: 10px 15px;
            display: flex;
            align-items: center;
            width: 100%;
        }

        /* Style for the text input */
        .styled-input {
            flex: 1;
            background-color: rgba(255, 255, 255, 0.05);
            border: none;
            border-radius: 8px;
            padding: 10px;
            color: white;
            font-size: 16px;
            outline: none;
        }

        /* Style for the submit button */
        .styled-button {
            background: linear-gradient(90deg, #4a90e2 0%, #67b26f 100%);
            border: none;
            border-radius: 8px;
            color: white;
            padding: 10px 20px;
            margin-left: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 16px;
        }

        .styled-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }

        /* Titles and descriptions */
        h1, p {
            color: white !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            text-align: center;
        }

        /* Spinner color */
        div[data-testid="stSpinner"] {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Title and description
    st.markdown("<h1 style='padding-top: 2rem;'>🌐 Website Status Monitor</h1>", unsafe_allow_html=True)
    st.markdown("<p style='margin-bottom: 2rem;'>Check if a website is up or down</p>", unsafe_allow_html=True)

    # Center the search bar
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.markdown('<div class="gradient-border">', unsafe_allow_html=True)
        st.markdown('<div class="inner-container">', unsafe_allow_html=True)
        
        with st.form(key='website_form'):
            website_input = st.text_input(
                label="",
                placeholder="Enter website URL (e.g., google.com)",
                label_visibility="collapsed",
                key="search_input"
            )
            submit_button = st.form_submit_button(label='Check', key='submit_button')
        
        st.markdown('</div></div>', unsafe_allow_html=True)
        
        if submit_button:
            if website_input:
                with st.spinner('Checking website status...'):
                    time.sleep(0.5)
                    status = check_website_status(website_input.strip())
                    
                    if 'Up' in status:
                        st.success(f"✅ **{website_input}** is **Up**")
                        if 'Redirected' in status:
                            st.info(f"🔀 {status.split('Up ')[1]}")
                    else:
                        st.error(f"❌ **{website_input}** is **{status}**")
            else:
                st.warning("⚠️ Please enter a website URL")

if __name__ == "__main__":
    main()