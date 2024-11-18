import streamlit as st
import time
from threading import Thread

# Initialize state for the timers
if "timers" not in st.session_state:
    st.session_state.timers = [2 * 3600] * 5  # 2 hours for each slot in seconds
    st.session_state.running = [False] * 5  # Timer running status

# Countdown function
def countdown(slot):
    while st.session_state.timers[slot] > 0 and st.session_state.running[slot]:
        st.session_state.timers[slot] -= 1
        time.sleep(1)

# Display and control timers
st.title("Warming Fixture Timer")

for i in range(5):
    st.header(f"Slot {i + 1}")

    # Display timer
    mins, secs = divmod(st.session_state.timers[i], 60)
    hours, mins = divmod(mins, 60)
    st.write(f"Time Remaining: {hours:02}:{mins:02}:{secs:02}")

    col1, col2, col3 = st.columns(3)

    # Start Button
    if col1.button(f"Start Slot {i + 1}", key=f"start_{i}"):
        if not st.session_state.running[i]:
            st.session_state.running[i] = True
            Thread(target=countdown, args=(i,), daemon=True).start()

    # Reset Button
    if col2.button(f"Reset Slot {i + 1}", key=f"reset_{i}"):
        st.session_state.timers[i] = 2 * 3600
        st.session_state.running[i] = False

    # Stop Button
    if col3.button(f"Stop Slot {i + 1}", key=f"stop_{i}"):
        st.session_state.running[i] = False

st.write("---")
st.info("The timer will alert you when it reaches zero. Refresh the page to restart.")

# Alert when a timer reaches zero
for i, timer in enumerate(st.session_state.timers):
    if timer == 0:
        st.warning(f"Slot {i + 1} timer has finished!")
