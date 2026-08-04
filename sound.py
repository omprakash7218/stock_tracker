import time
import simpleaudio as sa

# Load a short silent WAV file
wave_obj = sa.WaveObject.from_wave_file("silent.wav")

while True:
    play_obj = wave_obj.play()
    play_obj.wait_done()
    time.sleep(1)  # small pause before replay
