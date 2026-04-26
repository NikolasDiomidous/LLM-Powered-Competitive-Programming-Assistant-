import streamlit as st
from src.classifier import classify
from src.hint_engine import get_hint
from src.verifier import verify

st.set_page_config(page_title="CP Assistant", layout="wide")
st.title("Competitive Programming Assistant")

if "problem" not in st.session_state:
    st.session_state.problem = ""
    st.session_state.classification = None
    st.session_state.hints = []
    st.session_state.verification = None


st.header("1. Problem")
problem_input = st.text_area(
    "Paste the problem statement:",
    value=st.session_state.problem,
    height=200,
)

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Classify"):
        if problem_input.strip():
            st.session_state.problem = problem_input
            st.session_state.classification = classify(problem_input)
            st.session_state.hints = []
            st.session_state.verification = None

if st.session_state.classification:
    c = st.session_state.classification
    st.write(f"**Types:** {', '.join(c['types'])}")
    st.write(f"**Confidence:** {c['confidence']:.2f}")
    st.write(f"**Reasoning:** {c['reasoning']}")


st.header("2. Hints")
if st.session_state.problem:
    n_hints = len(st.session_state.hints)
    if n_hints < 4:
        if st.button(f"Get hint level {n_hints + 1}"):
            new_hint = get_hint(
                st.session_state.problem,
                n_hints + 1,
                st.session_state.hints,
            )
            st.session_state.hints.append(new_hint)
    else:
        st.info("All 4 hints revealed.")

    for i, h in enumerate(st.session_state.hints):
        st.markdown(f"**Hint {i + 1}:** {h}")
else:
    st.info("Classify a problem first.")


st.header("3. Verify your approach")
if st.session_state.problem:
    approach_input = st.text_area(
        "Describe your approach in plain English:",
        height=150,
    )
    if st.button("Verify"):
        if approach_input.strip():
            st.session_state.verification = verify(
                st.session_state.problem,
                approach_input,
            )

    if st.session_state.verification:
        v = st.session_state.verification
        outcome_colors = {
            "correct": "green",
            "correct_but_suboptimal": "orange",
            "partially_correct": "orange",
            "wrong_approach": "red",
        }
        color = outcome_colors[v["outcome"]]
        st.markdown(f"**Outcome:** :{color}[{v['outcome']}]")
        st.write(f"**Complexity:** {v['complexity']}")
        st.write(f"**Feedback:** {v['feedback']}")
else:
    st.info("Classify a problem first.")