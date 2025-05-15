import streamlit as st

st.title("🎓 CurveMyPath")
st.write("A simple course recommender for OVGU students.")

goal = st.selectbox("Select your career goal:", ["Data Scientist", "Product Management", "AI/ML Developer"])
if st.button("Recommend Courses"):
    st.write(f"Recommended for {goal}: Human-Centered AI, Statistics I")
st.write("Why? These courses align with your goal’s core skills.")