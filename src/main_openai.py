import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This chatbot analyzes customer reviews and responds appropriately based on sentiment. "
    "Enter a customer review and get a tailored response!"
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": """You are a customer service representative responding to customer reviews. 
                
Your task is to:
1. Analyze the sentiment of each customer review (positive, negative, or neutral)
2. Respond appropriately based on the sentiment:

For POSITIVE reviews:
- Thank the customer warmly
- Express appreciation for their feedback
- Encourage them to continue being a valued customer
- Highlight what they liked if mentioned

For NEGATIVE reviews:
- Acknowledge their concerns with empathy
- Apologize sincerely for any inconvenience
- Offer specific solutions or steps to resolve issues
- Provide contact information for further assistance
- Show commitment to improvement

For NEUTRAL reviews:
- Thank them for their feedback
- Ask clarifying questions if needed
- Offer additional assistance or information

Always maintain a professional, helpful, and empathetic tone. Keep responses concise but personalized."""
            }
        ]

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("Enter a customer review to get a response..."):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
