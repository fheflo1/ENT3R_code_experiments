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


st.markdown("---")  # skillelinje

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Felles parametre
x = np.linspace(0, 4 * np.pi, 400)
fps = 20
frames = 60

def make_interference_gif(mode, filename):
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.set_ylim(-2.5, 2.5)
    ax.set_xlim(0, 4 * np.pi)
    ax.axis('off')

    line1, = ax.plot([], [], lw=2, color='blue')
    line2, = ax.plot([], [], lw=2, color='red')
    line_sum, = ax.plot([], [], lw=2.5, color='black')

    def init():
        line1.set_data([], [])
        line2.set_data([], [])
        line_sum.set_data([], [])
        return line1, line2, line_sum

    def animate(i):
        t = i / fps
        if mode == "constructive":
            # To forskjellige bølger (forskjellig frekvens)
            y1 = np.sin(1.0 * x - 2 * np.pi * 0.4 * t)
            y2 = np.sin(1.2 * x - 2 * np.pi * 0.4 * t)
        elif mode == "destructive":
            # To identiske bølger i motfase
            y1 = np.sin(x - 2 * np.pi * 0.4 * t)
            y2 = np.sin(x - 2 * np.pi * 0.4 * t + np.pi)
        else:
            raise ValueError("Mode må være 'constructive' eller 'destructive'.")

        y_sum = y1 + y2
        line1.set_data(x, y1)
        line2.set_data(x, y2)
        line_sum.set_data(x, y_sum)
        return line1, line2, line_sum

    ani = FuncAnimation(fig, animate, frames=frames, init_func=init, blit=True)
    ani.save(filename, writer=PillowWriter(fps=fps))
    plt.close(fig)

# Lag GIF-ene
constructive_path = "constructive.gif"
destructive_path = "destructive.gif"

make_interference_gif("constructive", constructive_path)
make_interference_gif("destructive", destructive_path)

# Vis i Streamlit
st.markdown("---")
st.subheader("📈 Konstruktiv interferens (generert)")
st.markdown("To bølger med litt forskjellig frekvens som forsterker hverandre i perioder.")
st.image(constructive_path, use_container_width=True)

st.subheader("⚠️ Destruktiv interferens (generert)")
st.markdown("To identiske bølger i motfase som kansellerer hverandre.")
st.image(destructive_path, use_container_width=True)
