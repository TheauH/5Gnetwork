import subprocess

def start_two_terminals(command1, command2):
    # Start tmux session with two windows
    tmux_cmd = "tmux new-session -d -s my_session -n terminal1"
    subprocess.run(tmux_cmd, shell=True, check=True)

    # Create a new window in the tmux session
    tmux_cmd = "tmux new-window -t my_session:1 -n terminal2"
    subprocess.run(tmux_cmd, shell=True, check=True)

    # Send the first command to the first terminal (window 0)
    tmux_cmd = f"tmux send-keys -t my_session:0 '{command1}' Enter"
    subprocess.run(tmux_cmd, shell=True, check=True)

    # Send the second command to the second terminal (window 1)
    tmux_cmd = f"tmux send-keys -t my_session:1 '{command2}' Enter"
    subprocess.run(tmux_cmd, shell=True, check=True)