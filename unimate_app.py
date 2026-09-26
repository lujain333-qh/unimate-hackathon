import streamlit as st
import calendar

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

st.set_page_config(page_title='UniMate | AI Campus Companion', page_icon='🎓', layout='wide')

# -------------------- DATA --------------------
COURSES = {
'CNE 100': dict(name='Data Comm & Networks', section='Section 1', room='B-21', time='Sun & Wed · 09:30–11:00', prof='Dr. Hussein Al Bazar', absence=1, pct=3.33, assess='Quizzes 20% · Assignments/Project 20% · Midterm 20% · Final 40%', result='Quiz 1 · 4.50 / 7.00 (64.3%)'),
'CIS 202': dict(name='Data Structures', section='Section 1', room='A-21', time='Sun & Wed · 11:00–12:20', prof='Mrs. Lubna Tahlawi', absence=1, pct=3.33, assess='Quizzes 15% · Labs/Assignments 20% · Midterm 25% · Final 40%', result='Assessment data not provided'),
'MTH 104': dict(name='Calculus I', section='Section 2', room='D-11', time='Sun & Wed · 13:20–14:40', prof='Dr. Ahmad Mugbil', absence=1, pct=3.33, assess='ALEKS 15% · Quizzes 15% · Midterm 30% · Final 40%', result='Assessment data not provided'),
'AIE 101': dict(name='AI Essentials', section='Section 1', room='D-23', time='Mon & Thu · 09:30–10:50', prof='Dr. Iman Hassan Ferjani', absence=0, pct=0, assess='Quizzes 15% · Python AI Labs 25% · Midterm 20% · Final 40%', result='Assessment data not provided'),
'SLM 101': dict(name='Foundation of Islamic Culture', section='Section 1', room='COED-11', time='Tue · 11:00–12:50 & Thu · 14:40–16:30', prof='Mr. Alaa Saber Gaber Ali', absence=0, pct=0, assess='Research/Participation 20% · Midterm 30% · Final 50%', result='Assessment data not provided')}

FACULTY = [
('Mrs. Lubna Tahlawi','Computer Engineering','D-2605 · Building D · 2nd Floor','L_tahlawi@yu.edu.sa','Sun–Thu · 09:30–10:30','CIS 202 · CIS 103 · CIS 321',True),
('Dr. Ahmad Mugbil','Mathematics & Natural Sciences','C-2604','a_mugbil@yu.edu.sa','Sun, Mon, Wed, Thu · 11:00–13:10 · Tue · 11:00–12:00','MTH 104 · MTH 106 · MTH 301',True),
('Dr. Hussein Al Bazar','Computer Engineering','B-2602 · Building B · 2nd Floor','h_albazar@yu.edu.sa','Sun · 11:00–12:30 · Mon/Tue · 10:30–11:30 · Wed · 12:30–13:20 · Thu · 11:00–12:30','CNE 100 · CNE 200 · NES 341 · NES 212 · MIS 328',False),
('Dr. Iman Hassan Ferjani','Computer Engineering','D-2609 · Building D · 2nd Floor','i_Hassan@yu.edu.sa','Sun–Thu · 08:00–09:00; Sun/Wed · 09:00–12:00; Mon/Thu · 11:00–12:00; Tue · 09:00–16:00','AIE 101 · CIS 103 · CIS 351 · SWE 411',False),
('Mr. Alaa Saber Gaber Ali','Humanities & Islamic Studies','A-1611','A_ALI@YU.EDU.SA','Sun/Mon · 11:00–12:00 · Wed · 12:00–13:00 · Thu · 11:00–13:00','SLM 101 · SLM 102 · ARB 101 · ARB 102',False)]

PLANNER = {
'Sunday':[('09:30','CNE 100','Lecture'),('11:00','CIS 202','Lecture'),('13:20','MTH 104','Lecture')],
'Monday':[('09:30','AIE 101','Lecture')],
'Tuesday':[('11:00','SLM 101','Lecture')],
'Wednesday':[('09:30','CNE 100','Lecture'),('11:00','CIS 202','Lecture'),('13:20','MTH 104','Lecture'),],
'Thursday':[('09:30','AIE 101','Lecture'),('14:40','SLM 101','Lecture')],
'Friday':[], 'Saturday':[]}

# -------------------- STYLE --------------------
st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root{--navy:#071A3D;--blue:#2F6FED;--pale:#EAF2FF;--bg:#F6F8FC;--text:#15213B;--muted:#6D7890;--line:#E4EAF3;--green:#20A46B}
html,body,[class*="css"]{font-family:Inter,sans-serif}.stApp{background:var(--bg);color:var(--text)}#MainMenu,footer{visibility:hidden}.block-container{padding:1.5rem 2.2rem 2.5rem;max-width:1500px}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#071A3D,#0A2450)}section[data-testid="stSidebar"]>div{padding:.9rem .8rem}section[data-testid="stSidebar"] *{color:#EAF1FF}
.logo{font-size:26px;font-weight:800;padding:8px 10px 18px}.logo span{color:#72A1FF}.profile{background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.1);padding:13px;border-radius:16px;margin-bottom:16px}.avatar{width:42px;height:42px;border-radius:50%;background:#DCE9FF;color:var(--navy);display:flex;align-items:center;justify-content:center;font-weight:800;float:left;margin-right:10px}.profile small{color:#AFC1E5}.navlabel{color:#8FA7D0;font-size:10px;text-transform:uppercase;letter-spacing:1.2px;margin:12px 9px 7px}
div.stButton>button{border-radius:11px;border:1px solid var(--line);font-weight:600;background:white;color:var(--text);min-height:40px}
section[data-testid="stSidebar"] div.stButton>button{background:#FFFFFF !important;color:#071A3D !important;text-align:left;padding-left:15px}
section[data-testid="stSidebar"] div.stButton>button p{color:#071A3D !important}
section[data-testid="stSidebar"] div.stButton>button:hover{background:#EAF2FF !important;color:#2F6FED !important;border-color:#2F6FED}.hero{background:linear-gradient(135deg,#071A3D,#123D83 60%,#2F6FED);color:white;border-radius:24px;padding:27px 30px;margin-bottom:18px;box-shadow:0 14px 35px rgba(7,26,61,.13)}.hero h1{font-size:30px;margin:0 0 7px;font-weight:800}.hero p{margin:0;color:#D9E6FF;font-size:13px}.badge{display:inline-block;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.18);border-radius:20px;padding:6px 11px;font-size:10px;margin-bottom:13px}
.metric,.card{background:white;border:1px solid var(--line);border-radius:18px;padding:17px;box-shadow:0 5px 18px rgba(20,40,80,.04)}.metric{min-height:120px}.icon{font-size:19px;background:var(--pale);border-radius:11px;padding:8px;display:inline-block}.label{font-size:11px;color:var(--muted);margin-top:11px}.value{font-size:24px;font-weight:800;color:var(--navy)}.muted{color:var(--muted);font-size:11px}.section-title{font-size:19px;font-weight:800;margin:23px 0 11px}.section-sub{color:var(--muted);font-size:11px;margin-top:-7px;margin-bottom:11px}.card h3{font-size:15px;margin:0 0 6px;color:var(--navy)}.code{color:var(--blue);font-weight:800;font-size:11px}.course{font-weight:700;font-size:14px;margin:3px 0 8px}.tag{display:inline-block;background:var(--pale);color:#255CC3;border-radius:20px;padding:5px 9px;font-size:9px;font-weight:700;margin:2px 3px 2px 0}.green{color:var(--green);font-weight:700}.event{border-left:4px solid var(--blue);background:#F3F7FF;padding:11px 13px;border-radius:10px;margin-bottom:8px}.event small{display:block;color:var(--muted);margin-top:3px}.progress-bg{height:8px;background:#E9EEF6;border-radius:99px;overflow:hidden;margin:8px 0 5px}.progress{height:100%;background:linear-gradient(90deg,#2F6FED,#6A98F5);border-radius:99px}.donut{width:145px;height:145px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:conic-gradient(#2F6FED 0 26.2%,#E7ECF5 26.2% 100%);margin:12px auto}.donutin{width:108px;height:108px;border-radius:50%;background:white;display:flex;flex-direction:column;align-items:center;justify-content:center}.donutin b{font-size:23px;color:var(--navy)}.donutin span{font-size:9px;color:var(--muted)}.prof{display:flex;gap:11px;align-items:flex-start}.profav{width:42px;height:42px;border-radius:13px;background:#E6EEFF;color:var(--blue);display:flex;align-items:center;justify-content:center;font-weight:800}.ai{background:linear-gradient(135deg,#EDF4FF,#F8FAFF);border:1px solid #D6E4FF;border-radius:18px;padding:17px}.day{background:white;border:1px solid var(--line);border-radius:13px;padding:10px;min-height:110px}.day h4{margin:0;color:var(--navy);font-size:12px}.slot{background:#EEF4FF;border-left:3px solid #2F6FED;border-radius:7px;padding:6px;margin-top:7px}.slot b{font-size:10px}.slot small{display:block;color:#6D7890;font-size:9px}.priority{display:flex;gap:10px;padding:9px 0;border-bottom:1px solid #EDF0F5}.priority:last-child{border-bottom:0}.picon{width:30px;height:30px;border-radius:9px;background:#EAF2FF;display:flex;align-items:center;justify-content:center}

/* AI CHAT - high contrast */
.ai-chat{background:#FFFFFF;border:1px solid #DDE5F2;border-radius:18px;padding:16px;margin-top:12px}
.ai-user{background:#071A3D;color:#FFFFFF;border-radius:14px 14px 4px 14px;padding:12px 14px;margin:9px 0 9px 12%;font-size:13px;line-height:1.6}
.ai-assistant{background:#EEF4FF;color:#071A3D;border:1px solid #D6E4FF;border-radius:14px 14px 14px 4px;padding:13px 14px;margin:9px 12% 9px 0;font-size:13px;line-height:1.7}
.ai-assistant *{color:#071A3D !important}
.ai-title{font-size:15px;font-weight:800;color:#071A3D;margin-bottom:6px}
.ai-hint{background:#F6F8FC;border:1px solid #E4EAF3;border-radius:12px;padding:10px 12px;color:#52617A;font-size:11px;margin-top:8px}
div[data-testid="stTextInput"] input{color:#071A3D !important;background:#FFFFFF !important;border:1px solid #BFCBE0 !important}
div[data-testid="stTextInput"] input::placeholder{color:#71809A !important}
</style>''',unsafe_allow_html=True)

# -------------------- NAV --------------------
if 'page' not in st.session_state: st.session_state.page='Dashboard'
with st.sidebar:
    st.markdown('<div class="logo">Uni<span>Mate</span></div>',unsafe_allow_html=True)
    st.markdown('<div class="profile"><div class="avatar">LA</div><b>Lana Alghamdi</b><br><small>Computer Network Engineering</small></div>',unsafe_allow_html=True)
    st.markdown('<div class="navlabel">Workspace</div>',unsafe_allow_html=True)
    nav=[('🏠','Dashboard'),('📈','My Progress'),('🗓️','Planner'),('📚','Courses'),('👩‍🏫','Professors'),('📅','Calendar'),('🤖','AI Assistant'),('🧠','Practice Prep'),('🎯','Clubs')]
    for icon,name in nav:
        if st.button(f'{icon}  {name}',key='nav_'+name,use_container_width=True): st.session_state.page=name
    st.markdown('---');st.caption('Fall Semester 2026/2027');st.caption('AI Campus Companion · Prototype')

def metric(icon,label,value,sub):
    st.markdown(f'<div class="metric"><span class="icon">{icon}</span><div class="label">{label}</div><div class="value">{value}</div><div class="muted">{sub}</div></div>',unsafe_allow_html=True)

def hero(badge,title,text):
    st.markdown(f'<div class="hero"><div class="badge">{badge}</div><h1>{title}</h1><p>{text}</p></div>',unsafe_allow_html=True)

def prof_card(p):
    name,dept,office,email,hours,cs,fav=p
    initials=''.join(x[0] for x in name.split()[:2])
    st.markdown(f'<div class="card"><div class="prof"><div class="profav">{initials}</div><div><h3>{name}</h3><div class="muted">{dept}</div></div></div><div style="margin-top:10px"><span class="tag">{"★ Bookmarked" if fav else "Faculty"}</span></div><div class="muted" style="margin-top:9px">📍 {office}</div><div class="muted" style="margin-top:5px">✉️ {email}</div><div class="muted" style="margin-top:5px">🕒 {hours}</div><div style="margin-top:8px"><b style="font-size:10px">Courses</b><br><span class="muted">{cs}</span></div></div>',unsafe_allow_html=True)

# -------------------- AI CONTEXT + CHAT --------------------
def build_student_context():
    course_lines = []
    for code, c in COURSES.items():
        course_lines.append(
            f"{code} — {c['name']} | {c['time']} | {c['room']} | Instructor: {c['prof']} | Absence: {c['absence']} ({c['pct']}%) | Assessment: {c['assess']} | Record: {c['result']}"
        )
    schedule_lines = []
    for day, items in PLANNER.items():
        if items:
            schedule_lines.append(day + ': ' + '; '.join(f'{tm} {code}' for tm, code, _ in items))
        else:
            schedule_lines.append(day + ': No classes')
    return """Student: Lana Alghamdi
Major: Bachelor of Science in Computer Network Engineering
Degree progress: 37 / 141 credits (26.2%)
Current load: 5 courses / 14 credit hours
Active club: Data Science Club
DN threshold: 20% absence rate

COURSES:
""" + "\n".join(course_lines) + "\n\nWEEKLY SCHEDULE:\n" + "\n".join(schedule_lines) + """

UPCOMING EVENTS:
- Tue Sep 29, 2026, 09:30–15:00: Industrial Field Trip to Sadara Chemical Company. Conflicts with SLM 101; departmental excuse policy applies.
- Wed Sep 30, 2026: Scheduled Course Quiz.

ROLE: You are UniMate, a friendly academic planning assistant. Use only the supplied student context for factual claims about Lana's schedule. Help her compare days, spot schedule conflicts, organize study time, and discuss course workload. Do not invent deadlines, grades, textbooks, or university policies. If information is missing, say so. Never invent classes, deadlines, grades, or textbook details. When the user asks about planning, use the supplied class times and identify real free periods before suggesting study blocks. Keep answers practical and concise.
"""


def get_openai_client():
    """Return an OpenAI client when a Streamlit secret is configured."""
    if OpenAI is None:
        return None
    try:
        api_key = st.secrets.get("OPENAI_API_KEY")
    except Exception:
        api_key = None
    if not api_key:
        return None
    try:
        return OpenAI(api_key=api_key)
    except Exception:
        return None


def ask_unimate_ai(user_message):
    """Ask the AI using the student's UniMate context.

    Returns None if the API is not configured or an API error occurs,
    so the app can always fall back to deterministic schedule answers.
    """
    client = get_openai_client()
    if client is None:
        return None

    history = st.session_state.get("ai_messages", [])[-8:]
    conversation = [{"role": "developer", "content": build_student_context()}]
    conversation.extend(history)
    conversation.append({"role": "user", "content": user_message})

    try:
        response = client.responses.create(
            model="gpt-5.6-luna",
            input=conversation,
        )
        text = getattr(response, "output_text", None)
        return text.strip() if text else None
    except Exception:
        return None


def schedule_text():
    return (
        "**Lana's Weekly Schedule**\n\n"
        "**Sunday**\n"
        "• 09:30–11:00 — CNE 100 — Data Comm & Networks — B-21\n"
        "• 11:00–12:20 — CIS 202 — Data Structures — A-21\n"
        "• 13:20–14:40 — MTH 104 — Calculus I — D-11\n\n"
        "**Monday**\n"
        "• 09:30–10:50 — AIE 101 — AI Essentials — D-23\n\n"
        "**Tuesday**\n"
        "• 11:00–12:50 — SLM 101 — Foundation of Islamic Culture — COED-11\n\n"
        "**Wednesday**\n"
        "• 09:30–11:00 — CNE 100 — Data Comm & Networks — B-21\n"
        "• 11:00–12:20 — CIS 202 — Data Structures — A-21\n"
        "• 13:20–14:40 — MTH 104 — Calculus I — D-11\n\n"
        "**Thursday**\n"
        "• 09:30–10:50 — AIE 101 — AI Essentials — D-23\n"
        "• 14:40–16:30 — SLM 101 — Foundation of Islamic Culture — COED-11\n\n"
        "**Friday:** No classes in the supplied schedule.\n\n"
        "**Saturday:** No classes in the supplied schedule."
    )


def prototype_answer(question):
    """Reliable schedule-aware fallback that works even without an API key."""
    q=question.strip().lower()

    planning_intent=any(x in q for x in ['study plan','study','study time','مذاكرة','ذاكر','أذاكر','خطة مذاكرة','رتب لي','ساعدني','help me'])
    if any(x in q for x in ['send my schedule','show my schedule','my schedule','weekly schedule','schedule','جدولي','الجدول','جدولك','جدولي الجامعي']) and not planning_intent:
        return schedule_text()
    if any(x in q for x in ['sunday','الأحد']):
        return '**الأحد:** CNE 100 من 09:30–11:00 في B-21، ثم CIS 202 من 11:00–12:20 في A-21، ثم MTH 104 من 13:20–14:40 في D-11.'
    if any(x in q for x in ['monday','الاثنين']):
        return '**الاثنين:** AIE 101 من 09:30–10:50 في D-23.'
    if any(x in q for x in ['tuesday','الثلاثاء']):
        return '**الثلاثاء:** SLM 101 من 11:00–12:50 في COED-11. ويوجد أيضًا Field Trip إلى Sadara يوم 29 سبتمبر من 09:30–15:00، وهو يتعارض مع SLM 101.'
    if any(x in q for x in ['wednesday','الأربعاء']):
        return '**الأربعاء:** CNE 100 من 09:30–11:00، CIS 202 من 11:00–12:20، وMTH 104 من 13:20–14:40.'
    if any(x in q for x in ['thursday','الخميس']):
        return '**الخميس:** AIE 101 من 09:30–10:50، ثم SLM 101 من 14:40–16:30.'
    if any(x in q for x in ['friday','الجمعة']):
        return '**الجمعة:** لا توجد محاضرات في الجدول المقدم.'
    if any(x in q for x in ['saturday','السبت']):
        return '**السبت:** لا توجد محاضرات في الجدول المقدم.'
    if any(x in q for x in ['free time','free period','free periods','وقت فراغ','فترة فراغ']):
        return 'عندك فترات فراغ واضحة: **الأحد/الأربعاء 12:20–13:20** بين CIS 202 وMTH 104، **الاثنين 10:50–** نهاية اليوم بعد AIE 101، و**الخميس 10:50–14:40** بين AIE 101 وSLM 101. أقدر أستخدم هذه الفترات كخيارات للمذاكرة.'
    if any(x in q for x in ['conflict','overlap','clash','تعارض','متعارض']):
        return 'في جدول المحاضرات الأسبوعي لا توجد محاضرتان في نفس الوقت. **التعارض الموجود في بيانات UniMate هو يوم 29 سبتمبر:** رحلة Sadara من 09:30–15:00 تتعارض مع SLM 101، وتطبق سياسة الاعتذار التابعة للقسم.'
    if any(x in q for x in ['study plan','study','study time','مذاكرة','ذاكر','أذاكر','خطة مذاكرة','رتب لي']):
        if 'cne 100' in q or 'cne' in q:
            return ('أكيد. بناءً على جدولك، أقدر أرتب CNE 100 حول محاضراتك بدون ما أضع جلسة داخل وقت محاضرة.\n\n'
                    '• **الأحد:** بعد MTH 104، جلسة مراجعة 30–45 دقيقة.\n'
                    '• **الاثنين:** عندك فترة مفتوحة بعد 10:50؛ مناسبة لجلسة CNE 100 أطول.\n'
                    '• **الثلاثاء:** SLM 101 الساعة 11:00–12:50، لذلك يمكن وضع جلسة قصيرة قبلها أو بعدها.\n'
                    '• ركزي حاليًا على **Network Layer** و**Guided vs Unguided Transmission Media** لأن سجل CNE 100 الموجود يبين Quiz 1 = 4.50/7.00 (64.3%).')
        return 'أقدر أبني لك خطة مذاكرة حول جدولك. عندك أكبر نافذة واضحة يوم الخميس بين 10:50 و14:40، وكذلك نافذة الأحد/الأربعاء من 12:20 إلى 13:20. إذا حددتِ المادة، سأربطها بهذه الفترات.'
    if any(x in q for x in ['workload','busy','ضغط','ضغط الأيام','أكثر يوم']):
        return 'من ناحية عدد المحاضرات في الجدول المقدم: **الأحد والأربعاء** هما الأكثر ازدحامًا، بثلاث محاضرات لكل يوم. الخميس فيه محاضرتان وبينهما فترة طويلة، والاثنين والثلاثاء محاضرة واحدة لكل يوم.'
    if any(x in q for x in ['cne 100','cne100']) and any(x in q for x in ['teach','prof','instructor','دكتور','يدرس']):
        return 'CNE 100 يدرّسه **Dr. Hussein Al Bazar**، Section 1، Room B-21، يومي الأحد والأربعاء 09:30–11:00.'
    if any(x in q for x in ['dn','absence','غياب']):
        return 'حد الـDN في البيانات الحالية هو **20%**. CNE 100 وCIS 202 وMTH 104 عند 3.33%، بينما AIE 101 وSLM 101 عند 0%.'
    if any(x in q for x in ['sadara','trip','رحلة']):
        return 'رحلة Sadara يوم **الثلاثاء 29 سبتمبر 2026 من 09:30 إلى 15:00**، وتتعارض مع SLM 101 حسب البيانات الموجودة.'
    if any(x in q for x in ['quiz','كويز']):
        return 'المسجل حاليًا: **CNE 100 Quiz 1 = 4.50/7.00 (64.3%)**، ويوجد أيضًا Scheduled Course Quiz بتاريخ 30 سبتمبر.'
    if 'cne 100' in q:
        return 'CNE 100 هو Data Comm & Networks، يومي الأحد والأربعاء 09:30–11:00 في B-21 مع Dr. Hussein Al Bazar. Quiz 1 المسجل هو 4.50/7.00 (64.3%).'
    if 'cis 202' in q:
        return 'CIS 202 هو Data Structures، يومي الأحد والأربعاء 11:00–12:20 في A-21 مع Mrs. Lubna Tahlawi.'
    if 'mth 104' in q or 'calculus' in q:
        return 'MTH 104 هو Calculus I، يومي الأحد والأربعاء 13:20–14:40 في D-11 مع Dr. Ahmad Mugbil.'
    if 'aie 101' in q:
        return 'AIE 101 هو AI Essentials، يومي الاثنين والخميس 09:30–10:50 في D-23 مع Dr. Iman Hassan Ferjani.'
    if 'slm 101' in q:
        return 'SLM 101 هو Foundation of Islamic Culture، الثلاثاء 11:00–12:50 والخميس 14:40–16:30 في COED-11 مع Mr. Alaa Saber Gaber Ali.'
    return 'أفهم جدولك الجامعي وأقدر أساعدك فيه. جربي سؤالًا مثل: **«أرسل لي جدولي»**، **«وش عندي الأحد؟»**، **«وين أقدر أذاكر CNE 100؟»**، **«هل عندي تعارض؟»**، أو **«وش أكثر يوم عندي فيه محاضرات؟»**'

page=st.session_state.page

# -------------------- DASHBOARD --------------------
if page=='Dashboard':
    hero('AI CAMPUS COMPANION · FALL 2026/2027','Good afternoon, Lana 👋','Your academic command center — degree progress, classes, attendance, faculty and next steps in one place.')
    a,b,c,d=st.columns(4)
    with a: metric('🎓','Degree Progress','26.2%','37 of 141 credits completed')
    with b: metric('📚','Completed Credits','37 / 141','Bachelor of Science')
    with c: metric('🗂️','Current Load','5 courses','14 credit hours')
    with d: metric('⭐','Club Membership','Active','Data Science Club')
    st.markdown('<div class="section-title">Academic Snapshot</div>',unsafe_allow_html=True)
    left,right=st.columns([1.3,.7])
    with left:
        st.markdown('<div class="card"><h3>Current Courses</h3><div class="section-sub">Fall 2026/2027 registration</div>',unsafe_allow_html=True)
        for code,c in COURSES.items():
            st.markdown(f'<div style="padding:9px 0;border-bottom:1px solid #E9EDF4"><span class="code">{code}</span><span class="muted" style="float:right">{c["time"]}</span><div class="course">{c["name"]}</div><span class="tag">{c["room"]}</span><span class="tag">{c["prof"]}</span></div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="card"><h3>Degree Progress</h3><div class="section-sub">Computer Network Engineering</div><div class="donut"><div class="donutin"><b>26.2%</b><span>completed</span></div></div><div style="text-align:center" class="muted">37 completed · 104 remaining</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="section-title">Attendance & DN Safety</div><div class="section-sub">DN threshold: 20% absence rate</div>',unsafe_allow_html=True)
    cols=st.columns(5)
    for col,(code,c) in zip(cols,COURSES.items()):
        with col:
            width=max(c['pct']/20*100,2)
            st.markdown(f'<div class="card"><span class="code">{code}</span><h3 style="margin-top:5px">{c["absence"]} absence{"s" if c["absence"]!=1 else ""}</h3><div class="progress-bg"><div class="progress" style="width:{width}%"></div></div><span class="green">{c["pct"]:.2f}% · Safe</span></div>',unsafe_allow_html=True)
    x,y=st.columns(2)
    with x: st.markdown('<div class="ai"><h3>🤖 AI Insight · CNE 100</h3><p style="font-size:12px">Quiz 1 is <b>4.50 / 7.00 (64.3%)</b>. Focus your next review on network-layer concepts and transmission media.</p><span class="tag">Network Layer</span><span class="tag">Transmission Media</span></div>',unsafe_allow_html=True)
    with y: st.markdown('<div class="card"><h3>📅 Upcoming</h3><div class="event"><b>Sep 29 · Industrial Field Trip</b><small>09:30–15:00 · Sadara Chemical Company · Conflicts with SLM 101.</small></div><div class="event"><b>Sep 30 · Scheduled Course Quiz</b><small>Academic assessment.</small></div></div>',unsafe_allow_html=True)

# -------------------- MY PROGRESS --------------------
elif page=='My Progress':
    hero('STUDENT PROGRESS','My Progress','A clear view of degree completion and current academic indicators.')
    a,b,c=st.columns(3)
    with a: metric('🎓','Degree Completion','26.2%','37 / 141 credits')
    with b: metric('📖','Current Courses','5','14 credit hours')
    with c: metric('🧪','CNE 100 Quiz 1','64.3%','4.50 / 7.00')
    l,r=st.columns([.7,1.3])
    with l: st.markdown('<div class="card"><h3>Degree Completion</h3><div class="donut"><div class="donutin"><b>26.2%</b><span>37 credits</span></div></div><p class="muted" style="text-align:center">104 credits remaining</p></div>',unsafe_allow_html=True)
    with r:
        rows=''.join(f'<tr><td>{code}</td><td>{c["result"]}</td><td>{"Safe" if c["pct"]<20 else "Review"}</td></tr>' for code,c in COURSES.items())
        st.markdown(f'<div class="card"><h3>Academic Indicators</h3><table><tr><th>Course</th><th>Record</th><th>Attendance</th></tr>{rows}</table></div>',unsafe_allow_html=True)
    st.markdown('<div class="section-title">Degree Plan Matches</div>',unsafe_allow_html=True)
    p,q=st.columns(2)
    with p: st.markdown('<div class="card"><h3>★ Mrs. Lubna Tahlawi</h3><div class="muted">Bookmarked · Computer Engineering</div><p><b>Upcoming alignment:</b> CIS 321 — Operating Systems</p><span class="tag">Junior Year</span><span class="tag">CIS 321</span></div>',unsafe_allow_html=True)
    with q: st.markdown('<div class="card"><h3>★ Dr. Ahmad Mugbil</h3><div class="muted">Bookmarked · Mathematics & Natural Sciences</div><p><b>Upcoming alignment:</b> MTH 301 — Linear Algebra · MTH 204 — Calculus II</p><span class="tag">Prerequisites</span></div>',unsafe_allow_html=True)

# -------------------- PLANNER --------------------
elif page=='Planner':
    hero('SMART STUDY PLANNER','Weekly Planner','See your classes, important dates and study priorities together.')
    a,b,c,d=st.columns(4)
    with a: metric('📚','Classes','5','14 credit hours')
    with b: metric('🎯','Priority Tasks','2','Quiz + field trip')
    with c: metric('⏰','Next Event','Sep 29','Industrial Field Trip')
    with d: metric('🧠','Focus Course','CNE 100','Quiz 1 · 64.3%')
    st.markdown('<div class="section-title">This Week</div><div class="section-sub">Your class schedule in planner view</div>',unsafe_allow_html=True)
    cols=st.columns(7)
    for col,day in zip(cols,PLANNER):
        html=f'<div class="day"><h4>{day}</h4>'
        if PLANNER[day]:
            for tm,code,kind in PLANNER[day]:
                html+=f'<div class="slot"><b>{tm} · {code}</b><small>{kind} · {COURSES[code]["room"]}</small></div>'
        else: html+='<div class="muted" style="margin-top:12px">No classes</div>'
        html+='</div>'; col.markdown(html,unsafe_allow_html=True)
    st.markdown('<div class="section-title">Today’s Priorities</div>',unsafe_allow_html=True)
    p,q=st.columns([1,1])
    with p:
        st.markdown('''<div class="card"><h3>🎯 Priority Board</h3><div class="priority"><div class="picon">🧪</div><div><b style="font-size:12px">Review CNE 100</b><div class="muted">Network layer + transmission media · Based on Quiz 1 result</div></div></div><div class="priority"><div class="picon">📅</div><div><b style="font-size:12px">Prepare for Sep 29 field trip</b><div class="muted">09:30–15:00 · Sadara · SLM 101 conflict</div></div></div><div class="priority"><div class="picon">📝</div><div><b style="font-size:12px">Check Sep 30 quiz details</b><div class="muted">Confirm course and assessment requirements.</div></div></div></div>''',unsafe_allow_html=True)
    with q:
        st.markdown('''<div class="ai"><h3>🧠 AI Study Suggestion</h3><p style="font-size:12px">Use your next focused study block for <b>CNE 100</b>. Start with the network layer, then compare guided and unguided transmission media. Finish with a short practice question.</p><span class="tag">25–30 min focus</span><span class="tag">CNE 100</span><span class="tag">Practice Prep</span></div>''',unsafe_allow_html=True)
    st.markdown('<div class="section-title">Upcoming Timeline</div>',unsafe_allow_html=True)
    st.markdown('<div class="card"><div class="event"><b>Tue · Sep 29 · 09:30–15:00</b><small>Industrial Field Trip to Sadara Chemical Company · SLM 101 conflict · Departmental excuse policy applies.</small></div><div class="event"><b>Wed · Sep 30</b><small>Scheduled Course Quiz.</small></div></div>',unsafe_allow_html=True)

# -------------------- COURSES --------------------
elif page=='Courses':
    hero('COURSE SYLLABUS DIRECTORY','Courses & Syllabi','Pick a course to view its instructor, schedule and assessment structure.')
    code=st.selectbox('Select a course',list(COURSES)); c=COURSES[code]; prof=next(p for p in FACULTY if p[0]==c['prof'])
    st.markdown(f'<div class="card"><span class="code">{code}</span><h2 style="margin:5px 0">{c["name"]}</h2><span class="tag">{c["section"]}</span><span class="tag">Room {c["room"]}</span><p class="muted">🕒 {c["time"]}</p></div>',unsafe_allow_html=True)
    a,b=st.columns(2)
    with a: st.markdown(f'<div class="card"><h3>Instructor</h3><p><b>{prof[0]}</b></p><p class="muted">{prof[1]}</p><p class="muted">📍 {prof[2]}</p><p class="muted">✉️ {prof[3]}</p><p class="muted">🕒 {prof[4]}</p></div>',unsafe_allow_html=True)
    with b: st.markdown(f'<div class="card"><h3>Assessment Breakdown</h3><p>{c["assess"]}</p><hr><p class="muted">Textbook metadata is not included in the supplied prototype dataset.</p></div>',unsafe_allow_html=True)

# -------------------- PROFESSORS --------------------
elif page=='Professors':
    hero('FACULTY DIRECTORY','Professors','Find faculty contacts, offices, office hours and course connections.')
    search=st.text_input('🔎 Search faculty',placeholder='Name, department or course...')
    filtered=[p for p in FACULTY if not search or search.lower() in (' '.join(map(str,p))).lower()]
    for i in range(0,len(filtered),2):
        cols=st.columns(2)
        for col,p in zip(cols,filtered[i:i+2]):
            with col: prof_card(p)

# -------------------- CALENDAR --------------------
elif page=='Calendar':
    hero('SEPTEMBER 2026','Academic Calendar','Important dates and schedule conflicts at a glance.')
    st.markdown('<div class="card"><h3>September 2026</h3><div class="section-sub">Monthly overview</div>',unsafe_allow_html=True)
    cols=st.columns(7)
    for col,w in zip(cols,['Sun','Mon','Tue','Wed','Thu','Fri','Sat']): col.markdown(f'<div style="text-align:center;font-size:10px;font-weight:800;color:#6D7890;padding:5px">{w}</div>',unsafe_allow_html=True)
    for week in calendar.monthcalendar(2026,9):
        cols=st.columns(7)
        for col,day in zip(cols,week):
            if day==0: col.markdown('<div style="min-height:78px"></div>',unsafe_allow_html=True)
            else:
                label='Field Trip' if day==29 else ('Course Quiz' if day==30 else '')
                cls='event-day' if day in (29,30) else ''
                col.markdown(f'<div class="day {cls}"><div class="daylabel">Sep</div><div class="daynum">{day}</div><div class="event-dot">{label}</div></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)
    a,b=st.columns(2)
    with a: st.markdown('<div class="event"><b>Tue, Sep 29 · 09:30–15:00</b><small>Industrial Field Trip to Sadara Chemical Company · Conflicts with SLM 101; departmental excuse policy applies.</small></div>',unsafe_allow_html=True)
    with b: st.markdown('<div class="event"><b>Wed, Sep 30</b><small>Scheduled Course Quiz.</small></div>',unsafe_allow_html=True)

# -------------------- AI ASSISTANT --------------------
elif page=='AI Assistant':
    hero('AI ACADEMIC COMPANION','UniMate AI Assistant 🤖','Talk to UniMate about your real university schedule, courses and study planning.')

    st.markdown('<div class="ai"><h3>🧠 Schedule-aware AI</h3><p class="muted">UniMate can use your loaded timetable to discuss classes, free periods, back-to-back lectures, course workload, attendance and upcoming assessments. It can also build a study plan around your actual class times.</p><span class="tag">Schedule-aware</span><span class="tag">Course-aware</span><span class="tag">Study planning</span></div>',unsafe_allow_html=True)

    st.markdown('<div class="section-title">Ask about your university schedule</div>',unsafe_allow_html=True)
    prompts=[
        'أرسل لي جدولي الأسبوعي',
        'وش عندي يوم الأحد؟',
        'هل عندي تعارض في جدولي؟',
        'رتب لي مذاكرة CNE 100 حول جدولي'
    ]
    pcols=st.columns(4)
    for col,prompt in zip(pcols,prompts):
        with col:
            if st.button(prompt,key='prompt_'+prompt,use_container_width=True):
                st.session_state.ai_input=prompt

    if 'ai_history' not in st.session_state:
        st.session_state.ai_history=[]
    if 'ai_input' not in st.session_state:
        st.session_state.ai_input=''

    typed=st.text_input('Your question',key='ai_input',placeholder='مثال: كيف أرتب مذاكرتي بين محاضرات الأحد والأربعاء؟')
    ask=st.button('🤖 Ask UniMate',type='primary',use_container_width=True)
    question=typed

    if ask and question.strip():
        question=question.strip()
        st.session_state.ai_input=''
        st.session_state.ai_history.append(('user',question))
        with st.spinner('UniMate is checking your schedule...'):
            try:
                answer=ask_unimate_ai(question)
            except Exception:
                answer=None
            if not answer:
                answer=prototype_answer(question)
        st.session_state.ai_history.append(('assistant',answer))

    if st.session_state.ai_history:
        st.markdown('<div class="ai-chat">',unsafe_allow_html=True)
        for role,message in st.session_state.ai_history[-12:]:
            if role=='user':
                st.markdown(f'<div class="ai-user"><b>You</b><br>{message}</div>',unsafe_allow_html=True)
            else:
                safe_message=message.replace('\n','<br>')
                st.markdown(f'<div class="ai-assistant"><div class="ai-title">🤖 UniMate</div>{safe_message}</div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)
    else:
        st.markdown('<div class="ai-hint"><b>Try this:</b> “رتب لي مذاكرة CNE 100 حول جدولي” — UniMate will look at your class times and suggest study blocks without inventing missing deadlines.</div>',unsafe_allow_html=True)

    st.markdown('<div class="section-title">What UniMate can help you decide</div>',unsafe_allow_html=True)
    a,b,c=st.columns(3)
    with a:
        st.markdown('<div class="card"><h3>📅 Schedule</h3><p class="muted">Find classes by day, identify free periods and explain your weekly routine.</p></div>',unsafe_allow_html=True)
    with b:
        st.markdown('<div class="card"><h3>📚 Courses</h3><p class="muted">Compare your courses, instructors, rooms, assessment weights and current records.</p></div>',unsafe_allow_html=True)
    with c:
        st.markdown('<div class="card"><h3>🧠 Study Planning</h3><p class="muted">Build study blocks around your lectures and focus on CNE 100 when your supplied record shows the most useful review area.</p></div>',unsafe_allow_html=True)

# -------------------- PRACTICE --------------------
elif page=='Practice Prep':
    hero('AI PRACTICE EXAM PREP','Practice Prep','Original practice prompts mapped to your current courses.')
    questions={
    'CIS 202':('Java Linked Lists','Describe an algorithm that recursively reverses a singly linked list. Then state the time complexity of searching a balanced binary search tree.'),
    'CNE 100':('Networking','Identify the protocol data unit associated with the TCP/IP network layer and compare guided with unguided transmission media.'),
    'MTH 104':('Chain Rule','Find the derivative of f(x) = ln(sin(3x²)) using the chain rule.'),
    'AIE 101':('AI Foundations','Explain supervised vs unsupervised machine learning and what makes a heuristic admissible for A*.'),
    'SLM 101':('Islamic Culture','Give a conceptual analysis of Shumuliyyah (شمولية) in Islamic culture.')}
    code=st.selectbox('Choose a course',list(questions)); topic,q=questions[code]
    st.markdown(f'<div class="card"><span class="code">{code}</span><h2 style="margin:5px 0">{topic}</h2><p>{q}</p><span class="tag">Practice Question</span><span class="tag">AI demo</span></div>',unsafe_allow_html=True)

# -------------------- CLUBS --------------------
elif page=='Clubs':
    hero('CAMPUS CONNECTIONS','Clubs & Recommendations','Recommendations connected to your courses and Network Engineering pathway.')
    st.markdown('<div class="card"><h3>✓ Current Membership</h3><p><b>Data Science Club</b> · Active Member</p><span class="tag">Current</span><span class="tag">Data & AI</span></div>',unsafe_allow_html=True)
    st.markdown('<div class="section-title">Recommended for You</div>',unsafe_allow_html=True)
    recs=[('Cybersecurity & Networking Club','Aligns with CNE 100 and upcoming security modules CNE 307/CNE 200.','CNE 100','Networking'),('Google Developer Student Club (GDSC)','Reinforces CIS 202 data structures and hands-on full-stack project building.','CIS 202','Development'),('Toastmasters / Debate Society','Builds technical communication for presentations and project defense.','Communication','Presentation')]
    cols=st.columns(3)
    for col,(name,desc,t1,t2) in zip(cols,recs):
        with col: st.markdown(f'<div class="card"><h3>🎯 {name}</h3><p class="muted">{desc}</p><span class="tag">{t1}</span><span class="tag">{t2}</span></div>',unsafe_allow_html=True)

st.markdown('<div style="text-align:center;color:#9AA5B8;font-size:10px;margin-top:28px">UniMate · Prototype · Al Yamamah University · Fall 2026/2027</div>',unsafe_allow_html=True)
