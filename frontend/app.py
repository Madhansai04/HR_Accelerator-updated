import streamlit as st
import pandas as pd
import requests
import re
from difflib import SequenceMatcher
from services.jargon import extract_jargon
from services.pdf_loader import load_pdf_text
from services.section_splitter import split_sections
from services.certificate import generate_certificate

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Learning Platform", layout="wide")

@st.cache_data
def load_data():
    text = load_pdf_text("data/retail.pdf")
    sections_dict = split_sections(text)
    return [{"title": k, "content": v} for k, v in sections_dict.items()]

sections = load_data()

if not sections:
    st.error("No content found")
    st.stop()

# -----------------------------
# STATE INIT
# -----------------------------
if "index" not in st.session_state:
    st.session_state.index = 0
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "section_done" not in st.session_state:
    st.session_state.section_done = set()
if "weak_areas" not in st.session_state:
    st.session_state.weak_areas = {}
if "show_final_quiz" not in st.session_state:
    st.session_state.show_final_quiz = False
if "final_quiz_done" not in st.session_state:
    st.session_state.final_quiz_done = False
if "completed" not in st.session_state:
    st.session_state.completed = False

# -----------------------------
# SIMILARITY CHECK
# -----------------------------
def is_copied(user_text, source_text, threshold=0.7):
    user_clean = user_text.lower().strip()
    source_clean = source_text.lower().strip()
    ratio = SequenceMatcher(None, user_clean, source_clean).ratio()
    return ratio >= threshold

# -----------------------------
# NAME GATE
# -----------------------------
if not st.session_state.user_name:
    st.title("🛍 AI Training Platform")
    st.subheader("Welcome! Please enter your name to begin.")
    name_input = st.text_input("Your Full Name")
    if st.button("Start Course"):
        if name_input.strip():
            st.session_state.user_name = name_input.strip()
            st.rerun()
        else:
            st.warning("Please enter your name.")
    st.stop()

# -----------------------------
# API FUNCTIONS
# -----------------------------
def api_speech(text):
    res = requests.post(f"{BASE_URL}/speech", json={"text": text})
    return res.content

def api_summary(content):
    res = requests.post(f"{BASE_URL}/summary", json={"content": content})
    return res.json()["result"]

def api_time(content):
    res = requests.post(f"{BASE_URL}/time", json={"content": content})
    return res.json()["result"]

def api_explain(content):
    res = requests.post(f"{BASE_URL}/explain", json={"content": content})
    return res.json()["result"]

def api_quiz(content, summary):
    res = requests.post(f"{BASE_URL}/quiz", json={"content": content, "summary": summary})
    return res.json()["result"]

def api_evaluate(content, user_summary):
    res = requests.post(f"{BASE_URL}/evaluate", json={"content": content, "user_summary": user_summary})
    return res.json()["result"]

def api_evaluate_quiz(content, quiz, answers):
    res = requests.post(
        f"{BASE_URL}/evaluate-quiz",
        json={"content": content, "quiz": quiz, "answers": answers}
    )
    return res.json()["result"]

def api_final_quiz(weak_areas):
    res = requests.post(f"{BASE_URL}/final-quiz", json={"weak_areas": weak_areas})
    return res.json()["result"]

# -----------------------------
# CERTIFICATE PAGE
# -----------------------------
if st.session_state.completed:
    st.balloons()
    st.success("🎉 Congratulations! You have completed the entire course.")
    st.markdown(f"### 🏆 Your Certificate is Ready, {st.session_state.user_name}!")
    pdf_bytes = generate_certificate(st.session_state.user_name)
    st.download_button(
        label="📄 Download Certificate (PDF)",
        data=pdf_bytes,
        file_name=f"Certificate_{st.session_state.user_name.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )
    st.stop()

# -----------------------------
# FINAL QUIZ PAGE
# -----------------------------
if st.session_state.show_final_quiz:
    st.title("🏁 Final Assessment")
    st.markdown("This quiz is based on topics you found difficult across all sections.")
    st.divider()

    if "final_quiz_text" not in st.session_state:
        with st.spinner("Generating your personalized final quiz..."):
            weak_list = list(st.session_state.weak_areas.values())
            st.session_state.final_quiz_text = api_final_quiz(weak_list)

    quiz_text = st.session_state.final_quiz_text
    parts = quiz_text.split("Subjective")
    mcq_part = parts[0]
    subjective_part = parts[1] if len(parts) > 1 else ""

    st.subheader("🧠 MCQ Questions")
    questions = mcq_part.split("\n\n")
    final_mcq_answers = {}

    for i, q in enumerate(questions):
        lines = q.strip().split("\n")
        if len(lines) > 1:
            st.write(f"**{lines[0]}**")
            final_mcq_answers[i] = st.radio("Choose answer", lines[1:], key=f"fq{i}")

    st.subheader("✍️ Subjective Questions")
    subj_lines = [q.strip() for q in subjective_part.split("\n") if q.strip()]
    final_subj_answers = []

    for i, q in enumerate(subj_lines):
        if ":" in q:
            st.write(f"**{q}**")
            ans = st.text_area(f"Your answer {i+1}", key=f"fsubj{i}")
            st.session_state[f"final_subj_ans_{i}"] = ans
            final_subj_answers.append(st.session_state.get(f"final_subj_ans_{i}", ""))

    if st.button("✅ Submit Final Quiz & Get Certificate"):
        final_subj_answers = [st.session_state.get(f"final_subj_ans_{i}", "") for i in range(len(subj_lines))]
        all_answered = all(a.strip() for a in final_subj_answers)
        if not all_answered:
            st.warning("Please answer all subjective questions before submitting.")
        else:
            st.session_state.final_quiz_done = True
            st.session_state.completed = True
            st.rerun()

    st.stop()

# -----------------------------
# HEADER
# -----------------------------
current = sections[st.session_state.index]

st.title("🛍 AI Training Platform")
st.markdown(f"👤 **Learner:** {st.session_state.user_name}")

progress = (st.session_state.index + 1) / len(sections)
st.progress(progress)
st.caption(f"Section {st.session_state.index+1} of {len(sections)}")

idx = st.session_state.index
if idx in st.session_state.section_done:
    st.success("✅ This section is complete!")
else:
    st.info("⚠️ Complete the Summary Evaluation and Quiz to unlock the next section.")

st.divider()

# -----------------------------
# FETCH SECTION DATA (cached)
# -----------------------------
section_key = f"section_{idx}"
if section_key not in st.session_state:
    st.session_state[section_key] = {
        "summary": api_summary(current["content"]),
        "time": api_time(current["content"])
    }

summary = re.sub(r"<.*?>", "", st.session_state[section_key]["summary"])
time = st.session_state[section_key]["time"]

# -----------------------------
# CONTENT CARD
# -----------------------------
st.markdown(f"### 📘 {current['title']}")

st.markdown(
    f"""
    <div style="
        background:#F7FBFC;
        padding:20px;
        border-radius:12px;
        border-left:6px solid #769FCD;
        margin-bottom:10px;
    ">
        <p style="font-size:16px; line-height:1.6;">{summary}</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(f"#### ⏱ Estimated Time: {time}")

if st.button("🔊 Listen to Summary"):
    audio_bytes = api_speech(summary)
    st.audio(audio_bytes, format="audio/mp3")

if st.button("Show Jargon"):
    jargon_text = extract_jargon(current["content"])
    rows = []
    for line in jargon_text.split("\n"):
        if "|" in line:
            parts = line.split("|")
            if len(parts) >= 2:
                rows.append({"Term": parts[0].strip(), "Meaning": parts[1].strip()})
    if rows:
        st.table(pd.DataFrame(rows))
    else:
        st.warning("No jargon extracted. Try again.")

st.divider()

# -----------------------------
# AI EXPLANATION
# -----------------------------
st.subheader("🤖 AI Explanation")
if st.button("Explain Section"):
    explanation = api_explain(current["content"])
    st.success(explanation)

# -----------------------------
# SUMMARY EVALUATION (MANDATORY)
# -----------------------------
st.subheader("✍️ Your Understanding (Required)")
st.caption("Write what you understood in your own words. Do not copy from the content above.")

# FIX 1: key is section-specific so text resets on section change
user_summary = st.text_area(
    "Write what you understood...",
    key=f"user_summary_{idx}"
)

eval_key = f"eval_done_{idx}"

if st.button("Evaluate Summary"):
    if not user_summary.strip():
        st.warning("Write something first.")
    # FIX 2: copy-paste detection against raw section content
    elif is_copied(user_summary, current["content"]):
        st.error("❌ Your response appears to be copied directly from the content. Please write in your own words.")
    # FIX 2: copy-paste detection against the AI summary too
    elif is_copied(user_summary, summary):
        st.error("❌ Your response is too similar to the section summary. Please write in your own words.")
    else:
        with st.spinner("Evaluating..."):
            result = api_evaluate(current["content"], user_summary)
        st.success(result)
        st.session_state[eval_key] = True
        st.session_state.weak_areas[idx] = result

if st.session_state.get(eval_key):
    st.caption("✅ Summary evaluated.")

# -----------------------------
# SMART QUIZ (MANDATORY)
# -----------------------------
st.subheader("🧠 Smart Quiz (Required)")

quiz_key = f"quiz_done_{idx}"

if not st.session_state.get(eval_key):
    st.warning("⚠️ Please evaluate your summary first before taking the quiz.")
else:
    if st.button("Generate Smart Quiz"):
        if user_summary.strip():
            with st.spinner("Generating quiz..."):
                quiz_text = api_quiz(current["content"], user_summary)
            st.session_state[f"quiz_{idx}"] = quiz_text
        else:
            st.warning("Write summary first.")

    if f"quiz_{idx}" in st.session_state:
        quiz_text = st.session_state[f"quiz_{idx}"]
        parts = quiz_text.split("Subjective")
        mcq_part = parts[0]
        subjective_part = parts[1] if len(parts) > 1 else ""

        st.subheader("🧠 MCQ Questions")
        questions = mcq_part.split("\n\n")
        mcq_answers = {}

        for i, q in enumerate(questions):
            lines = q.strip().split("\n")
            if len(lines) > 1:
                st.write(f"**{lines[0]}**")
                mcq_answers[i] = st.radio("Choose answer", lines[1:], key=f"q{idx}_{i}")

        st.subheader("✍️ Subjective Questions")
        subj_lines = [q.strip() for q in subjective_part.split("\n") if q.strip()]
        subj_answers = []

        for i, q in enumerate(subj_lines):
            if ":" in q:
                st.write(f"**{q}**")
                ans = st.text_area(f"Your answer {i+1}", key=f"subj{idx}_{i}")
                st.session_state[f"subj_ans_{idx}_{i}"] = ans
                subj_answers.append(st.session_state.get(f"subj_ans_{idx}_{i}", ""))

        if st.button("Submit Quiz"):
            subj_answers = [st.session_state.get(f"subj_ans_{idx}_{i}", "") for i in range(len(subj_lines))]
            all_answered = all(a.strip() for a in subj_answers)
            if not all_answered:
                st.warning("Please answer all subjective questions.")
            else:
                with st.spinner("Evaluating quiz..."):
                    result = api_evaluate_quiz(
                        current["content"],
                        quiz_text,
                        str({"mcq": mcq_answers, "subjective": subj_answers})
                    )
                st.session_state[f"quiz_result_{idx}"] = result
                st.session_state[quiz_key] = True
                st.session_state.section_done.add(idx)

        if st.session_state.get(f"quiz_result_{idx}"):
            st.markdown("### 📝 Quiz Feedback")
            st.info(st.session_state[f"quiz_result_{idx}"])

    if st.session_state.get(quiz_key):
        st.caption("✅ Quiz completed.")

st.divider()

# -----------------------------
# NAVIGATION
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("⬅ Previous"):
        if st.session_state.index > 0:
            st.session_state.index -= 1
            st.rerun()

with col2:
    if idx not in st.session_state.section_done:
        st.button("Next ➡", disabled=True, help="Complete evaluation and quiz first.")
    else:
        if st.button("Next ➡"):
            if st.session_state.index < len(sections) - 1:
                st.session_state.index += 1
                st.rerun()
            else:
                st.session_state.show_final_quiz = True
                st.rerun()