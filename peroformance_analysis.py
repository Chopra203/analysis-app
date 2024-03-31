import streamlit as st
import pandas as pd

def main_settings():
    st.title("Football Performance Analysis - Settings")

    # Initialize session state to store settings
    session_state = st.session_state
    if "event_types" not in session_state:
        session_state.event_types = ["Goal", "Yellow Card", "Red Card", "Substitution", "Shot"]
    if "player_names" not in session_state:
        session_state.player_names = [
            "Player 1", "Player 2", "Player 3", "Player 4",
            "Player 5", "Player 6", "Player 7", "Player 8",
            "Player 9", "Player 10", "Player 11", "Player 12",
            "Player 13", "Player 14", "Player 15", "Player 16"
        ]

    # Player names section
    st.subheader("Edit Names:")
    for i, player in enumerate(session_state.player_names):
        session_state.player_names[i] = st.text_input(f"Player {i+1}", player)

    # Event types section
    st.subheader("Edit Event Types:")
    for i, event_type in enumerate(session_state.event_types):
        session_state.event_types[i] = st.text_input(f"Event Type {i+1}", event_type)

    # Export to Excel button
    if st.button("Export Settings to Excel"):
        export_settings_to_excel(session_state.player_names, session_state.event_types)
        st.success("Settings exported to excel.")

def export_settings_to_excel(player_names, event_types):
    # Create DataFrame for player names and event types
    settings_df = pd.DataFrame({
        "Player Names": player_names,
        "Event Types": event_types
    })
    # Export DataFrame to Excel
    filename = "football_settings.xlsx"
    settings_df.to_excel(filename, index=False)

def main_tagging():
    st.title("Football Performance Analysis - Event Tagging")

    # Initialize session state to store events and notes
    session_state = st.session_state
    if "events" not in session_state:
        session_state.events = []
    if "notes" not in session_state:
        session_state.notes = {}

    # Event tagging section
    st.subheader("Event Tagging")

    event_types = st.session_state.event_types
    event_type = st.radio("Select Event Type", options=event_types)

    if event_type in event_types:
        time_input = st.number_input("Time (minutes)", min_value=0, max_value=90, value=0)
        player_names = st.session_state.player_names
        player_name = st.selectbox("Player Name", options=player_names)

        note = st.text_input("Note (Optional)", "")
        add_event_button = st.button("Add Event")

        if add_event_button:
            # Save tagged event to session state
            save_event(session_state.events, event_type, time_input, player_name)
            # Save note for the event (if provided)
            if note:
                save_note(session_state.notes, len(session_state.events), note)

            st.success("Event added successfully!")

    # Event visualization section
    st.subheader("Event Visualization")

    # Display events table with rearranged columns and custom index header
    events_df = pd.DataFrame(session_state.events, columns=["Player", "Event Type", "Time"])
    events_df.index += 1  # Shift index by 1 to start from 1 instead of 0
    events_df.index.name = "Event #"
    # Merge notes with events dataframe
    events_df["Note"] = [session_state.notes.get(i, "") for i in range(1, len(session_state.events) + 1)]
    st.write(events_df)

    # Export to Excel button
    if st.button("Export to Excel"):
        export_to_excel(session_state.events, session_state.notes)

def save_event(events, event_type, time, player):
    # Save the tagged event to the events list
    events.append({"Player": player, "Event Type": event_type, "Time": time})

def save_note(notes, event_number, note):
    # Save the note for the corresponding event number
    notes[event_number] = note

def export_to_excel(events, notes):
    # Convert events list to DataFrame
    events_df = pd.DataFrame(events, columns=["Player", "Event Type", "Time"])
    # Merge notes with events dataframe
    events_df["Note"] = [notes.get(i, "") for i in range(1, len(events) + 1)]

    # Export DataFrame to Excel
    filename = "football_events.xlsx"
    events_df.to_excel(filename, index=False)
    st.success(f"Events exported to {filename}")

if __name__ == "__main__":
    page = st.sidebar.radio("Select Page", ["Settings", "Tagging"])
    if page == "Settings":
        main_settings()
    elif page == "Tagging":
        main_tagging()
