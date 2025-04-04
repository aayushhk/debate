import openai
import streamlit as st
import time
import speech_recognition as sr
import random

# Define available voices
available_voices = ["ash", "echo", "fable", "onyx", "shimmer"]

# Define Religions
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
st.session_state.transcription_text = ""

# Sidebar Configuration
religion = sanatan
with st.sidebar:
    api_keys = "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"
    if api_keys:
        client = openai.OpenAI(api_key=api_keys)
    else:
        st.error("Please enter a valid OpenAI API Key")
        st.stop()
    
    rel = st.radio("Select Religion", ["Hindu", "Christian", "Islam"])
    if rel == "Hindu":
        religion = sanatan
    elif rel == "Islam":
        religion = islam
    else:
        religion = christianity

    num_chars = st.slider("Number of Characters (Sages)", 2, 5, 2)
    
    iter = st.slider("Debate Iterations", 1, 10, 1)

    st.info(f"Current Religion: {religion['rel']}")
    st.info(f"Language: {religion['language']}")

# Assign unique voices to sages
def assign_sage_voices(num_sages):
    return random.sample(available_voices, num_sages)

# Generate Response
def generate_sage_response(speaker, context, voice):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=context,
        temperature=0.4,
    )
    sage_text = response.choices[0].message.content

    sage_voice = client.audio.speech.create(
        model="tts-1-hd",
        voice=voice,
        input=sage_text,
    
        )

    col3 = st.container()
    with col3:
        col1, col2 = st.columns([1, 2])
        with col1:
            with st.expander(f"{speaker} says:", expanded=False):
                st.markdown(
                    f"<p style='font-size:16px; line-height:1.6;'>{sage_text}</p>",
                    unsafe_allow_html=True,
                )
        with col2:
            st.audio(sage_voice.content)

    return sage_text

# Start Debate
def start_sage_discussion(topic):
    context = [
        {"role": "system", "content": f'''You are a {religion["rel"]} experienced Sage. You are a wise saint speaking in pure {religion['language']} language. Use examples from {religion['books']}. You belong to {religion['rel']} Community. Provide refrences and specific events. Keep it warm, philosophical, within 60 seconds, and respectful. Point out mistakes, provide insights. '''},
        {"role": "user", "content": topic}
    ]

    sage_voices = assign_sage_voices(num_chars)
    
    # Opening by Sage 1
    sage1_text = generate_sage_response("🧙 Sage 1", context, sage_voices[0])
    context.append({"role": "assistant", "content": sage1_text})
    

    for round_num in range(iter):
        for i in range(2, num_chars + 1):
            context.append({"role": "system", "content": f"Now, you are Sage {i}. Respond, challenge, or expand respectfully."})
            sage_text = generate_sage_response(f"🧙‍♂️ Sage {i}", context, sage_voices[i-1])
            context.append({"role": "assistant", "content": sage_text})
            

        context.append({"role": "system", "content": "Return to Sage 1 to counter the arguments."})
        sage1_text = generate_sage_response("🧙 Sage 1", context, sage_voices[0])
        context.append({"role": "assistant", "content": sage1_text})
        

# UI
st.header("🦚Samwaad")
st.markdown("***A Philosophical Debate between Sages***")
st.session_state.transcription_text =""
col1=st.container(border=True)
with col1:
    topic = st.text_input("Enter a topic for discussion:", placeholder="e.g. The nature of Dharma")
    audio_value = st.audio_input("Record a voice message")
    if audio_value:
        transcription = client.audio.translations.create(
            model="whisper-1",
            file=audio_value
        )
        st.session_state.transcription_text = transcription.text.strip()
        st.success(f"**Topic:** {st.session_state.transcription_text}")
    startt=st.button("⚔️ Start Debate")
  

if startt:
    if topic or transcription:
        start_sage_discussion(topic+" " + st.session_state.transcription_text)
        st.session_state.transcription_text = ""
    else:
        st.error("⚠️ Please enter a topic first!")
