import streamlit as st
from PIL import Image
from queueOps import Queue  # <-- your queue.py file (must be in same folder)

# --- Page setup ---
st.set_page_config(page_title="Web Music Player", layout="centered")
st.title("🎧 Web Music Player")

# --- Initialize session variables ---
if "musicname" not in st.session_state:
    st.session_state.musicname = None
if "q" not in st.session_state:
    st.session_state.q = Queue()  # your custom queue
if "history" not in st.session_state:
    st.session_state.history = []  # for previous songs
if "is_playing" not in st.session_state:
    st.session_state.is_playing = False
# --- Helper Functions ---
def get_image():
    """Return album cover path or placeholder."""
    song = st.session_state.musicname
    if not song:
        return "musicArt/empty.jpg"
    path = f"musicArt/{song}.jpg"
    try:
        Image.open(path)  # test if it exists
        return path
    except FileNotFoundError:
        return "musicArt/empty.jpg"

def play_music(song_name):
    audio_path = f"music/{song_name}.mp3"
    try:
        with open(audio_path, "rb") as f:
            st.audio(f.read(), format="audio/mp3",autoplay=True)
    except FileNotFoundError:
        st.warning(f"Audio file not found: {audio_path}")
    


# --- Sidebar: Add to Queue ---
# we use form so the the page dosn't reload causing the current song to stop playing
with st.sidebar.form("add_song_form"):
    new_song = st.selectbox("Add Songs to Queue", ["Hold-On,-We're-Going-Home", "i'm-the-one", "greece",
                                                    "No-Brainer","Every-Breath-You-Take","Hotel-California"])
    submit = st.form_submit_button("Add to Queue")

if submit:
    st.session_state.q.enqueue(new_song)



# --- Sidebar: Queue Display ---
st.sidebar.markdown("### Song Queue")
if st.session_state.q.is_empty():
    st.sidebar.write("No songs in queue.")
else:
    # Display all valid songs from queue
    current = st.session_state.q.front
    songs_list = st.session_state.q.getAllqueue()
    while True:
        if current == st.session_state.q.rear:
            break
        current = (current + 1) % st.session_state.q.MAX
    for i, song in enumerate(songs_list, start=1):
        st.sidebar.write(f"{i}. {song}")



# Set first song if none playing
if st.session_state.musicname is None and not st.session_state.q.is_empty():
    st.session_state.musicname = st.session_state.q.dequeue()

# Display album cover
try:
    img = Image.open(get_image())
    st.image(img, width=250, caption=st.session_state.musicname or "No Song Playing")
except FileNotFoundError:
    st.image("musicArt/empty.jpg", width=250, caption="No Song Playing")


# --- Audio Control Section ---
if st.session_state.musicname:
    if st.session_state.is_playing:
        play_music(st.session_state.musicname)
    else:
        st.info(f"⏸️ '{st.session_state.musicname}' is paused.")

        
# --- Song Controls ---
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("⏮️ Previous"):
        if st.session_state.history:
            prev_song = st.session_state.history.pop()
            st.session_state.musicname = prev_song
            st.session_state.is_playing = True
            st.rerun()
        else:
            st.warning("No previous song!")
with col3:
    if st.button("⏭️ Next"): 
        if not st.session_state.q.is_empty():
            st.session_state.history.append(st.session_state.musicname)
            st.session_state.musicname = st.session_state.q.dequeue()
            st.session_state.is_playing = True
            st.rerun()
        else:
            st.warning("No next song in queue!")