import streamlit as st
import openai
from streamlit_chat import message
import os
import secrets_beta
import re
from decouple import config


# Setting page title and header
st.set_page_config(page_title="DOC-AI", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>DOC-AI - ask your medical questions </h1>", unsafe_allow_html=True)

# Set org ID and API key

openai.api_key = config("OPENAI_API_KEY")

# Initialise session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
if 'model_name' not in st.session_state:
    st.session_state['model_name'] = []
# if 'cost' not in st.session_state:
#     st.session_state['cost'] = []
# if 'total_tokens' not in st.session_state:
#     st.session_state['total_tokens'] = []
# if 'total_cost' not in st.session_state:
#     st.session_state['total_cost'] = 0.0

# Sidebar - let user choose model, show total cost of current conversation, and let user clear the current conversation
st.sidebar.title("Sidebar")
#model_name = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-4"))
# counter_placeholder = st.sidebar.empty()
# counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
clear_button = st.sidebar.button("Clear Conversation", key="clear")

# Map model names to OpenAI model IDs

model = "text-davinci-003"
model_name = "text-davinci-003"

# reset everything
if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    # st.session_state['number_tokens'] = []
    st.session_state['model_name'] = []
    # st.session_state['cost'] = []
    # st.session_state['total_cost'] = 0.0
    # st.session_state['total_tokens'] = []
    # counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")

prompt_prefix = """You're a Virtual Biomedical Assistant. 
Developed advanced AI technology, you're powerful healthcare assistant, AI consultant and doctor for various types of illnesses. 
You're capable of covering all medical bases in terms of versatility and also be straightforward in giving answers to health issues and patient complaints.
Here is a query from a user: """

# generate a response
def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})
    #response = ''

    try:
        completion = openai.Completion.create(
            model=model,
            prompt=prompt_prefix + prompt,
            max_tokens=256,
            temperature=0 #st.session_state['messages']
        )
        
        response = completion.choices[0].text
        # print(response)
        st.session_state['messages'].append({"role": "assistant", "content": response})

    except Exception as e:
        response = 'Error'
        st.session_state['messages'].append({"role": "assistant", "content": response})

    # print(st.session_state['messages'])
    # total_tokens = completion.usage.total_tokens
    # prompt_tokens = completion.usage.prompt_tokens
    # completion_tokens = completion.usage.completion_tokens
    return response#, total_tokens, prompt_tokens, completion_tokens


# container for chat history
response_container = st.container()
# container for text box
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output = generate_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        st.session_state['model_name'].append(model_name)
        # st.session_state['total_tokens'].append(total_tokens)

        # from https://openai.com/pricing#language-models
        # cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000

        # st.session_state['cost'].append(cost)
        # st.session_state['total_cost'] += cost

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
            # st.write(
            #     f"Model used: {st.session_state['model_name'][i]}; Number of tokens: {st.session_state['total_tokens'][i]}; Cost: ${st.session_state['cost'][i]:.5f}")
            # counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")


# message_history = []

# for message_ in message_history:
#         message(message_)   # display all the previous message

# placeholder = st.empty()  # placeholder for latest message
# input_ = st.text_input("you:")
# message_history.append(input_)

# with placeholder.container():
#     message(message_history[-1]) # display the latest message