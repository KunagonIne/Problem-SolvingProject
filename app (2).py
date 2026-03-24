
import streamlit as st

# -----------------------
# DATA MODEL
# -----------------------
class Player:
    def __init__(self, name, kills, deaths):
        self.name = name
        self.kills = kills
        self.deaths = deaths

    def kd(self):
        return self.kills / self.deaths if self.deaths != 0 else self.kills

    def score(self):
        return self.kills * 2 - self.deaths


# -----------------------
# SESSION STATE (important for Streamlit)
# -----------------------
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []


# -----------------------
# FUNCTIONS
# -----------------------
def search_player(name):
    for player in st.session_state.leaderboard:
        if player.name == name:
            return player
    return None


def add_player(name, kills, deaths):
    if search_player(name):
        st.warning("Player already exists!")
        return
    st.session_state.leaderboard.append(Player(name, kills, deaths))


def remove_player(name):
    lb = st.session_state.leaderboard
    for i in range(len(lb)):
        if lb[i].name == name:
            lb.pop(i)
            return True
    return False


def edit_player(name, kills, deaths):
    player = search_player(name)
    if player:
        player.kills = kills
        player.deaths = deaths
        return True
    return False


def get_value(player, category):
    if category == "Kills":
        return player.kills
    elif category == "Deaths":
        return -player.deaths
    elif category == "KD":
        return player.kd()
    elif category == "Score":
        return player.score()
    return 0


def sort_leaderboard(category):
    lb = st.session_state.leaderboard
    for i in range(1, len(lb)):
        key = lb[i]
        j = i - 1

        while j >= 0 and get_value(lb[j], category) < get_value(key, category):
            lb[j + 1] = lb[j]
            j -= 1

        lb[j + 1] = key


# -----------------------
# UI
# -----------------------
st.title("🎮 Leaderboard System")

# ➕ ADD PLAYER
st.subheader("Add Player")
name = st.text_input("Name")
kills = st.number_input("Kills", min_value=0, step=1)
deaths = st.number_input("Deaths", min_value=0, step=1)

if st.button("Add Player"):
    add_player(name, kills, deaths)

# ✏️ EDIT / REMOVE
st.subheader("Edit / Remove Player")
edit_name = st.text_input("Player Name to Edit/Delete")

col1, col2 = st.columns(2)

with col1:
    new_kills = st.number_input("New Kills", min_value=0, step=1, key="edit_k")
    new_deaths = st.number_input("New Deaths", min_value=0, step=1, key="edit_d")

    if st.button("Edit Player"):
        if edit_player(edit_name, new_kills, new_deaths):
            st.success("Updated!")
        else:
            st.error("Player not found")

with col2:
    if st.button("Remove Player"):
        if remove_player(edit_name):
            st.success("Removed!")
        else:
            st.error("Player not found")


# 🔽 SORT OPTION
st.subheader("Leaderboard")
category = st.selectbox("Sort By", ["Kills", "Deaths", "KD", "Score"])

sort_leaderboard(category)

# 🖥️ DISPLAY
for i, p in enumerate(st.session_state.leaderboard):
    st.write(f"{i+1}. {p.name} | K:{p.kills} D:{p.deaths} KD:{p.kd():.2f} Score:{p.score()}")
