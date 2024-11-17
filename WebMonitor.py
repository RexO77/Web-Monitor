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
    
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #1a1a2e 100%);
        }
        
        /* Clean form layout */
        [data-testid="stForm"] > div:first-child {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        /* Gradient search bar */
        .stTextInput {
            flex: 1;
        }
        
        .stTextInput > div > div {
            padding: 2px;
            position: relative;
            z-index: 1;
            background-image: linear-gradient(43deg, #4158D0 0%, #C850C0 46%, #FFCC70 100%);
            border-radius: 10px;
        }

        .stTextInput > div > div:before {
            z-index: -1;
            position: absolute;
            content: "";
            width: 100%;
            height: 100%;
            left: 0;
            top: 0;
            background-image: linear-gradient(43deg, #4158D0 0%, #C850C0 46%, #FFCC70 100%);
            filter: blur(20px);
        }

        .stTextInput input {
            background-color: #0b090a !important;
            border: none !important;
            color: white !important;
            font-size: 16px;
            padding: 15px !important;
            border-radius: 8px;
            width: 100%;
        }

        /* Simple button */
        .stButton button {
            background: #4a90e2;
            border: none;
            color: white;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.3s ease;
            min-width: 120px;
        }

        .stButton button:hover {
            background: #357abd;
            transform: translateY(-2px);
        }

        h1, p {
            color: white !important;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
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
            submit_button = st.form_submit_button(label='Check')  # Removed key parameter
        
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