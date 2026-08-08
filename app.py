import streamlit as st
from src.db import init_db, save_session, get_history
from src.ai_engine import AIEngine

st.set_page_config(page_title="Interview OS", page_icon="🎯", layout="wide")
init_db()

st.markdown("""
<style>
.block-container {padding-top: 2rem; max-width: 1200px;}
.hero {padding: 28px; border-radius: 18px; background: linear-gradient(135deg,#171717,#292929); color:white; margin-bottom:20px;}
.metric-card {padding:18px;border:1px solid #333;border-radius:14px;background:#111;}
.small {color:#999;font-size:13px;}
</style>
""", unsafe_allow_html=True)

if "screen" not in st.session_state:
    st.session_state.screen = "home"
if "history" not in st.session_state:
    st.session_state.history = []
if "candidate" not in st.session_state:
    st.session_state.candidate = {}
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "last_evaluation" not in st.session_state:
    st.session_state.last_evaluation = None
if "report" not in st.session_state:
    st.session_state.report = None

with st.sidebar:
    st.title("🎯 Interview OS")
    st.caption("Adaptive interview intelligence")
    page = st.radio("Navigate", ["Home", "Start Interview", "History"])
    st.divider()
    provider = st.selectbox("AI Provider", ["OpenAI", "Ollama"])
    model = st.text_input("Model", value="gpt-4o-mini" if provider == "OpenAI" else "llama3.2:3b")
    st.session_state.provider = provider
    st.session_state.model = model

if page == "Home":
    st.markdown("""
    <div class="hero">
      <h1>Interview OS</h1>
      <p>An adaptive interviewer that remembers your weaknesses and changes the next interview around you.</p>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    with c1:
        st.metric("Adaptive Interviewer", "ON")
    with c2:
        st.metric("Candidate Memory", "ON")
    with c3:
        st.metric("Interview Evaluator", "ON")

    st.subheader("What makes it different?")
    st.write("""
    Instead of generating random interview questions, Interview OS builds a live
    candidate profile from your answers. It detects weak areas, asks targeted
    follow-ups, and creates a personalized report at the end.
    """)

    st.info("Start with 5 questions for the demo. The interviewer adapts after every answer.")

elif page == "Start Interview":
    if not st.session_state.current_question and not st.session_state.messages:
        st.title("Start an Interview")
        with st.form("setup"):
            name = st.text_input("Candidate name")
            role = st.selectbox("Target role", ["Python Developer", "Software Engineer", "Data Analyst", "Frontend Developer", "General"])
            difficulty = st.select_slider("Difficulty", ["Beginner", "Intermediate", "Advanced"], value="Intermediate")
            focus = st.multiselect("Focus areas", ["DSA", "Python", "SQL", "System Design", "Communication", "Behavioral"], default=["DSA","Python"])
            count = st.slider("Questions", 3, 10, 5)
            resume = st.text_area("Optional resume / background", height=120)
            start = st.form_submit_button("🚀 Start Adaptive Interview")

        if start:
            if not name.strip():
                st.error("Enter your name.")
                st.stop()
            st.session_state.candidate = {
                "name": name, "role": role, "difficulty": difficulty,
                "focus": focus, "resume": resume, "question_count": count,
                "answers": [], "evaluations": []
            }
            st.session_state.messages = []
            st.session_state.last_evaluation = None
            st.session_state.report = None
            engine = AIEngine(st.session_state.provider, st.session_state.model)
            q = engine.first_question(st.session_state.candidate)
            st.session_state.current_question = q
            st.rerun()

    else:
        cand = st.session_state.candidate
        st.title(f"🎤 Interview: {cand['role']}")
        progress = len(cand["answers"]) / cand["question_count"]
        st.progress(min(progress, 1.0), text=f"Question {len(cand['answers']) + 1} of {cand['question_count']}")

        if st.session_state.last_evaluation:
            ev = st.session_state.last_evaluation
            st.subheader("Live feedback")
            a,b,c = st.columns(3)
            a.metric("Answer", f"{ev.get('score',0)}/10")
            b.metric("Technical", f"{ev.get('technical_score',0)}/10")
            c.metric("Clarity", f"{ev.get('clarity_score',0)}/10")
            st.caption(ev.get("brief_feedback",""))

        st.subheader(st.session_state.current_question or "Interview complete")

        with st.form("answer_form", clear_on_submit=True):
            answer = st.text_area("Your answer", height=180, placeholder="Explain your thinking. You can include examples.")
            submitted = st.form_submit_button("Submit Answer")

        if submitted:
            if not answer.strip():
                st.warning("Please enter an answer.")
                st.stop()

            engine = AIEngine(st.session_state.provider, st.session_state.model)
            ev = engine.evaluate_answer(cand, st.session_state.current_question, answer)
            cand["answers"].append({"question": st.session_state.current_question, "answer": answer})
            cand["evaluations"].append(ev)
            st.session_state.last_evaluation = ev

            if len(cand["answers"]) >= cand["question_count"]:
                report = engine.final_report(cand)
                st.session_state.report = report
                save_session(cand, report)
                st.session_state.current_question = None
                st.rerun()
            else:
                next_q = engine.next_question(cand, ev)
                st.session_state.current_question = next_q
                st.rerun()

        if st.session_state.report:
            report = st.session_state.report
            st.success("Interview completed!")
            st.header("🧬 Your Interview DNA")
            a,b,c,d = st.columns(4)
            a.metric("Overall", f"{report.get('overall_score',0)}/100")
            b.metric("Technical", f"{report.get('technical_score',0)}/100")
            c.metric("Communication", f"{report.get('communication_score',0)}/100")
            d.metric("Problem Solving", f"{report.get('problem_solving_score',0)}/100")

            st.subheader("Your pattern")
            st.write(report.get("candidate_pattern",""))

            x,y = st.columns(2)
            with x:
                st.markdown("### Strengths")
                for item in report.get("strengths", []):
                    st.write("✅", item)
            with y:
                st.markdown("### Improve next")
                for item in report.get("weaknesses", []):
                    st.write("🎯", item)

            st.subheader("Interviewer Quality")
            st.write(f"Adaptive quality: **{report.get('interviewer_quality',0)}/100**")
            st.caption(report.get("interviewer_feedback",""))

            st.subheader("Next Interview Strategy")
            st.write(report.get("next_interview_strategy",""))

            if st.button("Start New Interview"):
                for k in ["messages","candidate","current_question","last_evaluation","report"]:
                    st.session_state[k] = [] if k in ["messages"] else ({} if k=="candidate" else None)
                st.rerun()

elif page == "History":
    st.title("📚 Interview History")
    rows = get_history()
    if not rows:
        st.info("No interviews saved yet.")
    else:
        for row in rows:
            with st.expander(f"{row['name']} · {row['role']} · Score {row['score']}/100 · {row['created_at']}"):
                st.write(row["summary"])
