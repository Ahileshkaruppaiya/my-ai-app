import streamlit as st
from openai import OpenAI

# 1. Page Configuration
st.set_page_config(page_title="My AI Assistant", page_icon="🤖", layout="centered")
st.title("🤖 Personal AI Assistant")
st.write("Ask me anything!")

# 2. Initialize the AI Client
# Streamlit will securely fetch the API key from environment variables/secrets
api_key = st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.warning("Please configure your OPENAI_API_KEY in the app settings/secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

# 3. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]

# 4. Display Past Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 5. Handle User Input
if user_input := st.chat_input("Type your message here..."):
    # Add user message to state and display it
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Generate AI response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Call the AI model (using gpt-4o-mini as a fast, cost-effective default)
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            
            # Stream the response back to the UI in real-time
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            
            # Save the AI response to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
