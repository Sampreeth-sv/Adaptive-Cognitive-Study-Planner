import streamlit as st
import json
import random
from PyPDF2 import PdfReader
from datetime import date

st.set_page_config(page_title="Adaptive Study Planner", layout="wide")

SAVE_FILE = "study_plan.json"

# ---------- Helpers ----------
def parse_portions(text):
    return [t.strip() for t in text.split(",") if t.strip()]

def load_data():
    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "subjects": {},
            "completed": {},
            "revision": {},
            "streak": {"count": 0, "last_date": ""},
            "topic_progress": {},
            "weekly_stats": {"total": 0, "done": 0}
        }

def save_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def extract_pdf_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text[:1500]

def extract_topics_from_text(text):
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        line = line.strip()
        if 6 < len(line) < 80:
            cleaned.append(line)
    return cleaned[:20]

def get_intensity_count(mode):
    if mode == "Light":
        return 1
    if mode == "Balanced":
        return 2
    return 3

def is_hard_topic(topic):
    hard_keywords = ["DP","Graph","Dynamic","Backtracking","Optimization","Probability"]
    return any(k.lower() in topic.lower() for k in hard_keywords)

def update_streak(data):
    today = str(date.today())
    last = data["streak"]["last_date"]

    if last == today:
        return

    if last:
        prev = date.fromisoformat(last)
        if (date.today() - prev).days == 1:
            data["streak"]["count"] += 1
        else:
            data["streak"]["count"] = 1
    else:
        data["streak"]["count"] = 1

    data["streak"]["last_date"] = today


# ---------- Sidebar ----------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["📅 Planner", "📍 Progress Tracker", "💾 Save / Load"])

data = load_data()

# ---------- PAGE 1 ----------
if page == "📅 Planner":
    st.title("📅 Adaptive Weekly Study Planner")

    st.metric("🔥 Study Streak (days)", data["streak"]["count"])

    mode = st.selectbox("Study Mode", ["Light", "Balanced", "Hardcore"])
    num_sub = st.number_input("Number of subjects", 1, 10, 3)

    subjects = {}

    # -------- MAIN SUBJECTS --------
    for i in range(num_sub):
        st.markdown(f"### Subject {i+1}")
        name = st.text_input(f"Name {i}", key=f"sname{i}")
        credits = st.number_input(f"Credits {i}", 1, 5, 3, key=f"scred{i}")
        portions_text = st.text_input(f"Portions {i}", key=f"sport{i}")

        pdf = st.file_uploader(f"Upload syllabus PDF {i}", key=f"pdf{i}")
        auto_portions = []

        if pdf:
            text = extract_pdf_text(pdf)
            st.text_area("Preview", text, height=120, key=f"txt{i}")
            auto_portions = extract_topics_from_text(text)

        if name:
            final_portions = parse_portions(portions_text) if portions_text else auto_portions
            subjects[name] = {"credits": credits, "portions": final_portions}

    # -------- OPTIONAL SUBJECTS --------
    st.subheader("Optional Commitments ( Project / Internship / Course etc.)")

    num_extra = st.number_input("Number of optional areas", 0, 10, 0)

    for i in range(num_extra):
        name = st.text_input(f"Optional Name {i}", key=f"ename{i}")
        portions = st.text_input(f"Optional Portions {i}", key=f"eport{i}")

        if name:
            subjects[name] = {
                "credits": 1,
                "portions": parse_portions(portions)
            }

    # -------- COMPULSORY --------
    subjects["Aptitude"] = {
        "credits": 1,
        "portions": ["Percentages","Ratio","Time Work","Probability"]
    }

    subjects["Coding"] = {
        "credits": 1,
        "portions": ["Arrays","Strings","Recursion","Graphs","DP"]
    }

    # ---------- PLAN ----------
    if st.button("Generate Weekly Plan"):
        intensity = get_intensity_count(mode)
        weekly_plan = {}

        core_subjects = [(s, d) for s, d in subjects.items() if s not in ["Aptitude","Coding"]]

# split main vs optional
        main_subjects = []
        optional_subjects = []

        for s, d in core_subjects:
            if d["credits"] > 1:
                main_subjects.append((s, d))
            else:
                optional_subjects.append((s, d))

# slice only main academic subjects
            if mode == "Light":
                main_subjects = main_subjects[:2]
            elif mode == "Balanced":
                main_subjects = main_subjects[:3]
            else:
                main_subjects = main_subjects[:4]

# final = main + optional + aptitude + coding
            final_subjects = (
                main_subjects
                + optional_subjects
                + [("Aptitude", subjects["Aptitude"]),
                ("Coding", subjects["Coding"])]
                )

        for sub, details in final_subjects:
            all_topics = details["portions"]
            done = data["completed"].get(sub, [])
            remaining = [t for t in all_topics if t not in done]

            weight = details["credits"]
            count = max(1, min(intensity + weight//2, len(remaining)))

            if remaining:
                chosen = []
                for topic in remaining:
                    prog = data["topic_progress"].get(f"{sub}-{topic}",0)

                    if is_hard_topic(topic) and prog < 1:
                        chosen.append(topic)
                    else:
                        chosen.append(topic)

                    if len(chosen) >= count:
                        break

                weekly_plan[sub] = chosen
            else:
                if all_topics:
                    weekly_plan[sub] = [f"Revise → {random.choice(all_topics)}"]

        st.session_state["weekly_plan"] = weekly_plan
        st.session_state["subjects"] = subjects
        data["weekly_stats"] = {"total":0,"done":0}
        save_data(data)

    # ---------- DISPLAY ----------
    if "weekly_plan" in st.session_state:
        st.header("📘 This Week’s Study Plan")

        total, done_count = 0,0

        for sub, topics in st.session_state["weekly_plan"].items():
            st.subheader(sub)

            for topic in topics:
                col1, col2 = st.columns([4,1])
                clean_topic = topic.replace("Revise → ","")
                key = f"{sub}-{clean_topic}"

                total += 1

                if clean_topic in data["completed"].get(sub, []):
                    col1.markdown(f"~~📖 {topic}~~ ✅")
                    done_count += 1
                else:
                    col1.write(f"📖 {topic}")

                    if col2.button("✔ Done", key=key):
                        data["topic_progress"][key] = data["topic_progress"].get(key,0) + 1

                        if is_hard_topic(clean_topic):
                            if data["topic_progress"][key] >= 2:
                                data["completed"].setdefault(sub, []).append(clean_topic)
                        else:
                            data["completed"].setdefault(sub, []).append(clean_topic)

                        data["revision"].setdefault(sub, []).append(clean_topic)

                        update_streak(data)
                        save_data(data)
                        st.rerun()

        data["weekly_stats"]["total"] = total
        data["weekly_stats"]["done"] = done_count

        st.divider()
        st.write(f"Completed this week: **{done_count}/{total}**")

        if total > 0:
            percent = int((done_count/total)*100)
            st.progress(percent/100)
            st.write(f"Weekly Completion: {percent}%")

        st.divider()
        st.subheader("📈 Subject Progress")

        for sub, details in st.session_state["subjects"].items():
            all_topics = details["portions"]
            if not all_topics:
                continue

            completed = data["completed"].get(sub, [])
            true_completed = [t for t in completed if t in all_topics]
            progress = len(true_completed)/len(all_topics)

            st.write(sub)
            st.progress(progress)


# ---------- PROGRESS TRACKER ----------
elif page == "📍 Progress Tracker":
    st.title("📍 Update Completed Portions")

    subjects = st.session_state.get("subjects",{})

    if not subjects:
        st.warning("Generate a plan first.")
    else:
        sub = st.selectbox("Subject", list(subjects.keys()))
        all_topics = subjects[sub]["portions"]
        completed = data["completed"].get(sub,[])
        remaining = [t for t in all_topics if t not in completed]

        if not remaining:
            st.info("All topics completed.")
        else:
            topic = st.selectbox("Topic", remaining)
            if st.button("Mark as Completed"):
                data["completed"].setdefault(sub, []).append(topic)
                data["revision"].setdefault(sub, []).append(topic)
                update_streak(data)
                save_data(data)
                st.success("Saved!")

    st.write(data["completed"])


# ---------- SAVE/LOAD ----------
elif page == "💾 Save / Load":
    st.title("💾 Save / Load Setup")

    if st.button("Save"):
        subjects = st.session_state.get("subjects",{})
        data["subjects"]=subjects
        save_data(data)
        st.success("Saved!")

    if st.button("Load"):
        st.session_state["subjects"]=data.get("subjects",{})
        st.success("Loaded!")
