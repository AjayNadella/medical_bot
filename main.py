import streamlit as st
from chains import Chain

bot = Chain()

st.title("Medical Bot: Women's Health and Pregnancy Assistant")
st.markdown("Ask any questions about women's health or pregnancy, and I'll provide accurate and empathetic answers.")

# User Input
user_question = st.text_area("Enter your question here:")

if st.button("Get Answer"):
    if user_question.strip():
        with st.spinner("Fetching answer..."):
            try:
                response = bot.answer_question(user_question)
                st.success("Here is your answer:")
                st.write(response)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a question to get an answer.")
