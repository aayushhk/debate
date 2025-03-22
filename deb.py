import openai
import streamlit as st
import time

# OpenAI Client


sanatan = {
    "rel": "Hindu",
    "language": "Hindi",
    "books": {
        "Mahabharata", "Bhagavad Gita", "Ramayana", "Upanishads", "Vedas",
        "Narada Bhakti Sutras", "Rigveda", "Sutra", "Dharmasastras",
        "Hindu eschatology", "Brahmana", "Aranyakas", "Purana"
    },
    "quotations": {
        "Shlok", "Doha", "Chhand", "Padya", "Chaupai",
        "Kabita", "Gatha", "Shair", "Shabda"
    },
   
}
christianity = {
    "rel": "Christian",
    "language": "English",
    "books": {
        "Bible", "Old Testament", "New Testament", "Gospels",
        "Psalms", "Proverbs", "Genesis", "Exodus", "Revelation",
        "Epistles", "Acts", "Deuteronomy", "Job", "Isaiah"
    },
    "quotations": {
        "Verses", "Parables", "Psalms", "Proverbs", "Hymns",
        "Sermons", "Beatitudes", "Scripture"
    },
}
islam = {
    "rel": "Islam",
    "language": "Urdu",
    "books": {
        "Quran", "Hadith", "Sunnah", "Tafsir", "Fiqh", "Seerah",
        "Sahih al-Bukhari", "Sahih Muslim", "Riyad as-Salihin",
        "Al-Adab Al-Mufrad", "Tirmidhi", "An-Nawawi’s 40 Hadith",
        "Usul al-Fiqh", "Tafsir al-Jalalayn"
    },
    "quotations": {
        "Ayah", "Hadith", "Dua", "Surah", "Tafsir",
        "Sunnah", "Qasas", "Fatwa", "Quranic Verse"
    },
}

st.set_page_config(page_title="Sage vs. Sage - Wisdom Duel", layout="wide")

religion = sanatan
with st.sidebar:
    api_keys=st.text_input("Enter OPENAI API Key")
    client = openai.OpenAI(api_key=api_keys)
    rel=st.radio("Select Religion",["Hindu","Christian","Islam"])
    if rel=="Hindu":
        religion = sanatan  # Assign religion
    elif rel=="Islam":
        religion = islam
    else:
        religion = christianity

    iter=st.slider("Select Iterations",1,10,1)
    st.info(f"Current religion :  {religion['rel']}")
    st.info(f"Language :  {religion['language']}")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []  # Stores conversation history

# Function to generate a response
def generate_sage_response(speaker, context):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=context,
        temperature=0.5,
        
    )
    sage_text = response.choices[0].message.content

    voice = "onyx" if speaker == "🧙 Sage 1" else "fable"
    sage_voice = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=sage_text,
       
    )
    col3 =st.container(border=True)
    with col3:
    # Display response in an expander
        col1, col2 = st.columns([1, 2])
    
            # Adjust layout
        with col1:
                with st.expander(f"{speaker} says:", expanded=False):
                    st.markdown(f"<p style='font-size:16px; line-height:1.6;'>{sage_text}</p>", unsafe_allow_html=True)
        with col2:
            st.audio(sage_voice.content)

        return sage_text

# Function to process user input and start discussion
def start_sage_discussion(topic):
    # Initialize conversation
    st.session_state.messages.append({"role": "user", "content": topic})

    context = [
        {"role": "system", "content": f"You are a wise saint speaking in {religion['language']}. Engage in a philosophical debate using examples from {religion['books']}. Keep it warm and respectful and within 200 words. Point out mistakes, provide insights"},
        {"role": "user", "content": topic}
    ]

    # Sage 1's Opening Statement
    sage1_text = generate_sage_response("🧙 Sage 1", context)
    context.append({"role": "assistant", "content": sage1_text})
    time.sleep(2)

    # Continuous back-and-forth discussion
    for _ in range(iter):  # Number of rounds
        context.append({"role": "system", "content": "Now, you are another saint. Either correct, expand, or challenge the previous statement with deeper insights."})
        sage2_text = generate_sage_response("🧙‍♂️ Sage 2", context)
        context.append({"role": "assistant", "content": sage2_text})
        time.sleep(2)

        context.append({"role": "system", "content": "Now, return as the first sage and counter the argument, provide new insights, or refine your explanation."})
        sage1_text = generate_sage_response("🧙 Sage 1", context)
        context.append({"role": "assistant", "content": sage1_text})
        time.sleep(2)

# Streamlit UI


st.markdown(
    "<h1>🧙 Sage vs. Sage - Wisdom Duel ⚔️</h1>",
    unsafe_allow_html=True,
)



topic = st.text_input("Enter a topic for discussion:", placeholder="e.g. The nature of Dharma")


st.markdown(
    """<style>
    div.stButton > button {
        background-color: #6A0DAD;
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 10px;
    }
    div.stButton > button:hover {
        background-color: #4B0082;
    }
    </style>""",
    unsafe_allow_html=True,
)
if st.button("⚔️ Start Debate"):
    if topic:
        st.markdown("<hr style='border: 1px solid #5A189A;'>", unsafe_allow_html=True)
        start_sage_discussion(topic)
    else:
        st.error("⚠️ Please enter a topic first!")

# Display conversation history
with st.sidebar:
    if st.session_state.messages:
        st.subheader("📜 Conversation History:")
        for msg in st.session_state.messages:
            role = "👤 **You:**" if msg["role"] == "user" else msg["role"]
            st.markdown(f"{role} {msg['content']}")
