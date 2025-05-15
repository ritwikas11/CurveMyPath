import streamlit as st

st.title("🎓 CurveMyPath")
st.write("A simple course recommender for OVGU students.")

st.warning("🚧 Dashboard is under construction: This is an MVP. We're actively working to improve it! Feedback is welcome.")

goal = st.selectbox("Select your career goal:", ["Data Scientist", "Product Management", "AI/ML Developer"])
if st.button("Recommend Courses"):
    st.write(f"Recommended for {goal}: Human-Centered AI, Statistics I")
st.write("Why? These courses align with your goal’s core skills.")

if st.button("💬 Give feedback"):
    st.write("Email us at: team@curvemypath.com")