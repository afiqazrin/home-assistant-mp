import subprocess
subprocess.run(["pactl", "set-sink-mute", "0", "0"])

# Set the volume to a specific level (adjust '70%' as needed)
subprocess.run(["pactl", "set-sink-volume", "0", "1%"])