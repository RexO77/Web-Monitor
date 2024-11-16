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
            else:
                return f'Down (Status Code: {status_code})'
    except requests.exceptions.RequestException as e:
        return f'Down ({e})'

def main():
    st.set_page_config(page_title="Website Status Monitor", layout="centered")
    
    # Custom CSS with dark gradient and animations
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #1a1a2e 100%);
        }
        div[data-testid="stToolbar"] {
            display: none;
        }
        .stTextInput > div > div {
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
        }
        .stTextInput input {
            color: white;
        }
        .stButton > button {
            background: linear-gradient(90deg, #4a90e2 0%, #67b26f 100%);
            border: none;
            border-radius: 10px;
            color: white;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        h1, p {
            color: white !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        div[data-testid="stSpinner"] {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Title and description
    st.markdown("<h1 style='text-align: center; padding-top: 2rem;'>🌐 Website Status Monitor</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-bottom: 2rem;'>Check if a website is up or down</p>", unsafe_allow_html=True)

    # Create three columns for centering
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        # Input field with proper label
        website_input = st.text_input(
            label="Website URL",
            placeholder="Enter website URL (e.g., google.com)",
            label_visibility="collapsed"
        )
        
        if st.button("Check Status", use_container_width=True):
            if website_input:
                with st.spinner('Checking website status...'):
                    # Add artificial delay for better UX
                    time.sleep(0.5)
                    status = check_website_status(website_input.strip())
                    
                    # Status display with custom styling
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