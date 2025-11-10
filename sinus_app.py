import streamlit as st
import numpy as np
import sounddevice as sd

st.set_page_config(page_title="Sinusfrekvens-generator", page_icon="🎵")
st.title("🎧 Sinusfrekvens-generator")
st.markdown(
    "Bruk slideren for å velge frekvens (Hz). "
    "Trykk **Start** for å spille av tonen og **Stopp** for å avslutte."
)

# Velg frekvens (innenfor menneskelig hørsel)
frequency = st.slider("Frekvens (Hz)", min_value=20, max_value=20000, value=440, step=1)

# Parametre
duration = 1.0  # sekunder per buffer
sample_rate = 44100
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# session_state initialisering
if "playing" not in st.session_state:
    st.session_state.playing = False
if "prev_freq" not in st.session_state:
    st.session_state.prev_freq = None

# Én knapp som toggler mellom start/stopp
button_label = "▶️ Start" if not st.session_state.playing else "⏹️ Stopp"
if st.button(button_label):
    st.session_state.playing = not st.session_state.playing
    if st.session_state.playing:
        wave = np.sin(2 * np.pi * frequency * t)
        sd.play(wave, samplerate=sample_rate, loop=True)
        st.session_state.prev_freq = frequency
    else:
        sd.stop()

# Oppdater tonefrekvens dynamisk hvis brukeren justerer slider mens det spiller
if st.session_state.playing and frequency != st.session_state.prev_freq:
    wave = np.sin(2 * np.pi * frequency * t)
    sd.play(wave, samplerate=sample_rate, loop=True)
    st.session_state.prev_freq = frequency
