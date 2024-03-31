import streamlit as st
import pandas as pd

def main():
    st.title("Football Event Tagger")

    # Sidebar
    st.sidebar.header("Options")
    team1 = st.sidebar.text_input("Team 1", "Team A")
    team2 = st.sidebar.text_input("Team 2", "Team B")

    # Initialize an empty list to store events
    events = []

    # Main content
    st.subheader("Match Events")
    event_type = st.selectbox("Event Type", ["Goal", "Yellow Card", "Red Card", "Substitution"])
    if event_type == "Goal":
        player = st.text_input("Scorer", "")
        minute = st.number_input("Minute", min_value=0, max_value=120, value=0)
        events.append((team1, team2, minute, "Goal", player, ""))
        st.write(f"{team1} vs {team2}: {minute}' - Goal! {player}")
    elif event_type == "Yellow Card":
        player = st.text_input("Player", "")
        minute = st.number_input("Minute", min_value=0, max_value=120, value=0)
        events.append((team1, team2, minute, "Yellow Card", player, ""))
        st.write(f"{team1} vs {team2}: {minute}' - Yellow Card for {player}")
    elif event_type == "Red Card":
        player = st.text_input("Player", "")
        minute = st.number_input("Minute", min_value=0, max_value=120, value=0)
        events.append((team1, team2, minute, "Red Card", player, ""))
        st.write(f"{team1} vs {team2}: {minute}' - Red Card for {player}")
    elif event_type == "Substitution":
        player_in = st.text_input("Player In", "")
        player_out = st.text_input("Player Out", "")
        minute = st.number_input("Minute", min_value=0, max_value=120, value=0)
        events.append((team1, team2, minute, "Substitution", player_out, player_in))
        st.write(f"{team1} vs {team2}: {minute}' - Substitution: {player_out} out, {player_in} in")

    # Display events in table format
    if events:
        st.subheader("Recorded Events")
        df_events = pd.DataFrame(events, columns=["Team 1", "Team 2", "Minute", "Event Type", "Player 1", "Player 2"])
        st.table(df_events)

    # Export to Excel button
    if st.button("Export to Excel"):
        df = pd.DataFrame(events, columns=["Team 1", "Team 2", "Minute", "Event Type", "Player 1", "Player 2"])
        filename = "football_events.xlsx"
        df.to_excel(filename, index=False)
        st.success(f"Events exported to {filename}")

if __name__ == "__main__":
    main()
