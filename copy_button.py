import streamlit as st

def create_copy_button(text_to_copy):
    button_id = "copyButton" + text_to_copy
    
    button_html = f"""<button id="{button_id}">Copy</button>
    <script>
    document.getElementById("{button_id}").onclick = function() {{
        navigator.clipboard.writeText("{text_to_copy}").then(function() {{
            console.log('Async: Copying to clipboard was successful!');
        }}, function(err) {{
            console.error('Async: Could not copy text: ', err);
        }});
    }}
    </script>"""
    
    st.markdown(button_html, unsafe_allow_html=True)
