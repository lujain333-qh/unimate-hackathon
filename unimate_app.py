
import streamlit as st

st.set_page_config(
    page_title="UniMate",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------
st.markdown("""
<style>
    .stApp { background: #f7f9fc; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #061a3a 0%, #082653 100%);
    }
    [data-testid="stSidebar"] * { color: white !important; }
    .brand {
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 24px;
    }
    .subtitle { color: #64748b; margin-top: -10px; }
    .card {
        background: white;
        padding: 22px;
        border-radius: 16px;
        border: 1px solid #e8edf5;
        box-shadow: 0 4px 16px rgba(20, 40, 80, 0.05);
        height: 100%;
    }
    .metric {
        font-size: 28px;
        font-weight: 800;
        color: #102a56;
    }
    .label {
        color: #64748b;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: .4px;
    }
    .available {
        color: #15803d;
        background: #dcfce7;
        padding: 6px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
    }
    .busy {
        color: #a16207;
        background: #fef3c7;
        padding: 6px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
    }
    .offline {
        color: #475569;
        background: #e2e8f0;
        padding: 6px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
    }
    .prof-name { font-size: 20px; font-weight: 800; color: #102a56; }
    .prof-role { color: #64748b; margin-bottom: 12px; }
    .tag {
        display: inline-block;
        background: #eff6ff;
        color: #2563eb;
        padding: 5px 9px;
        border-radius: 8px;
        margin: 2px;
        font-size: 12px;
    }
    .ai-box {
        background: linear-gradient(135deg, #081d42, #123b7a);
        color: white;
        padding: 24px;
        border-radius: 18px;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Data ----------
professors = [
    {
        "name": "Dr. Ahmed Al-Salem",
        "role": "Programming Instructor",
        "department": "Computer Science",
        "status": "Available Now",
        "status_class": "available",
        "hours": "2:00 PM – 4:00 PM",
        "days": "Sun, Tue, Thu",
        "tags": ["Programming", "Software Development", "Data Structures"],
    },
    {
        "name": "Dr. Sara Mohammed",
        "role": "Mathematics Instructor",
        "department": "Mathematics",
        "status": "Available Now",
        "status_class": "available",
        "hours": "1:00 PM – 3:00 PM",
        "days": "Mon, Wed",
        "tags": ["Calculus", "Linear Algebra", "Statistics"],
    },
    {
        "name": "Dr. Emily Vance",
        "role": "Data Science Instructor",
        "department": "Computer Science",
        "status": "Busy",
        "status_class": "busy",
        "hours": "10:00 AM – 12:00 PM",
        "days": "Mon, Wed, Fri",
        "tags": ["Data Science", "Machine Learning", "Artificial Intelligence"],
    },
    {
        "name": "Dr. Robert Chen",
        "role": "Computer Networks Instructor",
        "department": "Network Engineering",
        "status": "Available Now",
        "status_class": "available",
        "hours": "12:00 PM – 2:00 PM",
        "days": "Sun, Tue",
        "tags": ["Computer Networks", "Cybersecurity", "Network Systems"],
    },
    {
        "name": "Dr. Jessica Alba",
        "role": "UI/UX Design Instructor",
        "department": "Design",
        "status": "Offline",
        "status_class": "offline",
        "hours": "11:00 AM – 1:00 PM",
        "days": "Tue, Thu",
        "tags": ["UI/UX Design", "Human-Computer Interaction", "Design Thinking"],
    },
    {
        "name": "Dr. Omar Khalid",
        "role": "Database Systems Instructor",
        "department": "Computer Science",
        "status": "Available Now",
        "status_class": "available",
        "hours": "3:00 PM – 5:00 PM",
        "days": "Mon, Wed",
        "tags": ["Databases", "SQL", "Data Management"],
    },
]

# ---------- Sidebar ----------
st.sidebar.markdown('<div class="brand">🎓 UniMate ✨</div>', unsafe_allow_html=True)
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "AI Assistant", "My Progress", "Professors", "Clubs"],
    label_visibility="collapsed",
)
st.sidebar.markdown("---")
st.sidebar.caption("Logged in as")
st.sidebar.markdown("**Lujain Abdullah**")
st.sidebar.caption("Network Engineering")

# ---------- Dashboard ----------
if page == "Dashboard":
    st.title("Welcome back, Lujain! 👋")
    st.markdown('<p class="subtitle">Here is your academic overview for the semester.</p>', unsafe_allow_html=True)

    cols = st.columns(4)
    metrics = [
        ("Overall GPA", "3.84", "Top 5% of class"),
        ("Credits Completed", "96 / 120", "80% degree progress"),
        ("Assessments Due", "5 Tasks", "2 due within 48 hours"),
        ("Attendance Rate", "94.6%", "Slight improvement this week"),
    ]
    for col, (label, value, note) in zip(cols, metrics):
        with col:
            st.markdown(f'<div class="card"><div class="label">{label}</div><div class="metric">{value}</div><div class="subtitle">{note}</div></div>', unsafe_allow_html=True)

    st.write("")
    left, right = st.columns([1.55, 1])

    with left:
        st.markdown('<div class="card"><h3>Course Progress</h3><p class="subtitle">Your active curriculum milestones</p>', unsafe_allow_html=True)
        for course, pct in [("Machine Learning & Neural Networks", 78), ("Advanced Data Structures", 92), ("Linear Algebra & Systems", 60), ("UI/UX Interaction Design", 85)]:
            st.write(f"**{course}** — {pct}%")
            st.progress(pct / 100)
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown("""
        <div class="ai-box">
            <h3>🤖 UniMate AI Companion</h3>
            <p>Your personalized academic mentor & advisor.</p>
            <b>Suggested next step</b>
            <p>Review recursion and practice two programming problems before your next assessment.</p>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card"><h3>Upcoming Assessments</h3>', unsafe_allow_html=True)
        for item, date, urgency in [
            ("Midterm Examination", "Due Oct 14", "URGENT"),
            ("Binary Tree Implementation", "Due Oct 18", "SOON"),
            ("Portfolio Case Study Presentation", "Due Oct 24", "LATER"),
            ("Problem Set 4: Matrices", "Due Oct 29", "LATER"),
        ]:
            st.markdown(f"**{item}**  \n{date}  ·  `{urgency}`")
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown('<div class="card"><h3>Professor Availability</h3>', unsafe_allow_html=True)
        for p in professors[:3]:
            icon = "🟢" if p["status"] == "Available Now" else "🟡"
            st.markdown(f"**{p['name']}**  \n{p['role']}  \n{icon} {p['status']}")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------- My Progress ----------
elif page == "My Progress":
    st.title("My Progress")
    st.markdown('<p class="subtitle">Track your academic performance and stay on top of your goals.</p>', unsafe_allow_html=True)

    cols = st.columns(4)
    metrics = [
        ("Semester GPA", "3.84", "Top 5% of class"),
        ("Credits Earned", "96 / 120", "80% degree progress"),
        ("Courses Completed", "14 / 18", "77% completion rate"),
        ("Academic Standing", "Dean's List", "Excellent standing"),
    ]
    for col, (label, value, note) in zip(cols, metrics):
        with col:
            st.markdown(f'<div class="card"><div class="label">{label}</div><div class="metric">{value}</div><div class="subtitle">{note}</div></div>', unsafe_allow_html=True)

    st.write("")
    left, right = st.columns([1.5, 1])

    with left:
        st.markdown('<div class="card"><h3>Active Course Breakdown</h3>', unsafe_allow_html=True)
        courses = [("Programming", 78), ("Mathematics", 86), ("Chemistry", 91), ("Psychology", 84)]
        for course, pct in courses:
            st.write(f"**{course}** — {pct}%")
            st.progress(pct / 100)
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown('<div class="card"><h3>Areas Needing Attention</h3>', unsafe_allow_html=True)
        st.warning("Programming: review recursion before the next assessment.")
        st.info("Mathematics: practice the topics from the latest quiz.")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card"><h3>Upcoming Assessments</h3>', unsafe_allow_html=True)
        st.write("🔴 Programming Quiz — Tomorrow")
        st.write("🟡 Mathematics Assignment — Sep 28")
        st.write("🟢 Chemistry Lab — Sep 30")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------- Professors ----------
elif page == "Professors":
    st.title("Professor Directory")
    st.markdown('<p class="subtitle">Find the right professor and get academic support when you need it.</p>', unsafe_allow_html=True)

    search = st.text_input("🔍 Search professor or course", placeholder="e.g. Programming or Dr. Ahmed")
    c1, c2, c3 = st.columns(3)
    with c1:
        course_filter = st.selectbox("Course", ["All Courses", "Programming", "Mathematics", "Computer Networks", "Data Science"])
    with c2:
        availability = st.selectbox("Availability", ["All", "Available Now", "Busy", "Offline"])
    with c3:
        sort = st.selectbox("Sort by", ["Name (A-Z)", "Availability"])

    filtered = professors
    if search:
        s = search.lower()
        filtered = [p for p in filtered if s in p["name"].lower() or s in p["role"].lower() or any(s in t.lower() for t in p["tags"])]
    if course_filter != "All Courses":
        filtered = [p for p in filtered if any(course_filter.lower() in t.lower() for t in p["tags"])]
    if availability != "All":
        filtered = [p for p in filtered if p["status"] == availability]

    st.write("")
    for i in range(0, len(filtered), 2):
        row = st.columns(2)
        for j, col in enumerate(row):
            if i + j >= len(filtered):
                break
            p = filtered[i + j]
            with col:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(f'<div class="prof-name">{p["name"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="prof-role">{p["role"]}</div>', unsafe_allow_html=True)
                st.write(f"🏛️ {p['department']} Department")
                st.markdown(f'<span class="{p["status_class"]}">● {p["status"]}</span>', unsafe_allow_html=True)
                st.write(f"🕒 Office Hours: {p['hours']} — {p['days']}")
                st.markdown(" ".join([f'<span class="tag">{t}</span>' for t in p["tags"]]), unsafe_allow_html=True)
                if st.button("View Profile →", key=f"profile_{p['name']}"):
                    st.session_state["selected_professor"] = p["name"]
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
                st.write("")

    if "selected_professor" in st.session_state:
        selected = next((p for p in professors if p["name"] == st.session_state["selected_professor"]), None)
        if selected:
            st.divider()
            st.subheader(selected["name"])
            st.write(selected["role"])
            st.write(f"**Department:** {selected['department']}")
            st.write(f"**Availability:** {selected['status']}")
            st.write(f"**Office Hours:** {selected['hours']} — {selected['days']}")
            st.info("Demo action: a future version can connect this button to real university scheduling.")

# ---------- AI Assistant ----------
elif page == "AI Assistant":
    st.title("AI Assistant 🤖")
    st.markdown('<p class="subtitle">Ask UniMate for help with your course materials.</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="ai-box">
        <h3>UniMate AI Companion</h3>
        <p>Ask a question about your course, request an explanation, or practice a concept.</p>
    </div>
    """, unsafe_allow_html=True)

    prompt = st.chat_input("Ask UniMate something...")
    if prompt:
        st.chat_message("user").write(prompt)
        st.chat_message("assistant").write(
            "Demo response: I can explain this step by step and, in the full version, "
            "ground the answer in the professor's uploaded course materials using RAG."
        )

# ---------- Clubs ----------
elif page == "Clubs":
    st.title("Clubs & Activities")
    st.markdown('<p class="subtitle">Personalized recommendations based on your interests and courses.</p>', unsafe_allow_html=True)
    for name, reason in [
        ("AI Club", "Recommended because of your interest in artificial intelligence."),
        ("Cybersecurity Club", "Matches your Network Engineering background."),
        ("Programming Club", "Recommended based on your current programming course."),
    ]:
        st.markdown(f'<div class="card"><h3>{name}</h3><p>{reason}</p></div>', unsafe_allow_html=True)
        st.write("")
