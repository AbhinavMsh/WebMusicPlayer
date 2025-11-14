import streamlit as st
from PIL import Image
from queueOps import Queue 

# Title
st.set_page_config(page_title="Web Music Player", layout="centered")
st.title("🎧 Web Music Player")

# session variables 
if "musicname" not in st.session_state:
    st.session_state.musicname = None
if "q" not in st.session_state:
    st.session_state.q = Queue()  # your custom queue
if "history" not in st.session_state:
    st.session_state.history = []  # for previous songs
if "is_playing" not in st.session_state:
    st.session_state.is_playing = False


# Helper Functions 
def getImage():
    """Returns album cover path"""
    song = st.session_state.musicname
    # if no song playing display greyed out image
    if not song:
        return "musicArt/empty.jpg"
    # else music art
    path = f"musicArt/{song}.jpg"
    # test if path exists
    try:
        Image.open(path)  
        return path
    except FileNotFoundError:
        return "musicArt/empty.jpg"

def playMusic(song_name):
    # get audio path
    audio_path = f"music/{song_name}.mp3"

    # opening audio file
    try:
        with open(audio_path, "rb") as f:
            st.audio(f.read(), format="audio/mp3",autoplay=True,width=500)
    except FileNotFoundError:
        st.warning(f"Audio file not found: {audio_path}")
    


# SIDEBAR: Add song to queue
with st.sidebar.form("add_song_form"):
    new_song = st.selectbox("Add Songs to Queue", ["Hold-On,-We're-Going-Home", "i'm-the-one", "greece",
                                                    "No-Brainer","Every-Breath-You-Take","Hotel-California"])
    submit = st.form_submit_button("Add to Queue")
if submit:
    st.session_state.q.enqueue(new_song)

# if user added a song and no song is playing set music name the added song and dequeue
# This part does not play the song, go to line 87-89
if st.session_state.musicname is None and not st.session_state.q.is_empty():
    st.session_state.musicname = st.session_state.q.dequeue()
    st.session_state.is_playing = True


# SIDEBAR: Queue Display 
st.sidebar.markdown("### Song Queue")
# check if queue is empty
if st.session_state.q.is_empty():
    st.sidebar.write("No songs in queue.")
else:
    # Display all valid songs from queue
    current = st.session_state.q.front

    # getting all songs in queue using getAllqueue in queueOps.py
    songs_list = st.session_state.q.getAllqueue()

    # enumerate to get count to 
    for i, song in enumerate(songs_list, start=1):
        st.sidebar.write(f"{i}. {song}")

# Display album cover
try:
    img = Image.open(getImage())
    st.image(img, width=250, caption=st.session_state.musicname or "No Song Playing")
except FileNotFoundError:
    st.image("musicArt/empty.jpg", width=250, caption="No Song Playing")

# play music
if st.session_state.musicname and st.session_state.is_playing:
    playMusic(st.session_state.musicname)

# Song Controls 
col1, col2 = st.columns([3, 2]) # 3, 2 defined width ratio 
# not utilising the col2 (used just for space)

with col1:
    if st.button("⏮️ Previous"):
        if st.session_state.history: # if stack exists
            prev_song = st.session_state.history.pop() # pop into prev_song
            st.session_state.musicname = prev_song # set musicname to prev_song
            st.session_state.is_playing = True # set is_playing to true
            st.rerun()  # rerun page
        else:
            st.warning("No previous song!")
with col2:
    if st.button("⏭️ Next"): 
        if not st.session_state.q.is_empty(): 
            st.session_state.history.append(st.session_state.musicname) # push current song into stack
            st.session_state.musicname = st.session_state.q.dequeue() # get song from queue
            st.session_state.is_playing = True # set is_playing to true
            st.rerun() # rerun page
        else:
            st.warning("No next song in queue!")