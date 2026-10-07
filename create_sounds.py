import wave
import math
import os
import struct

ASSETS_FOLDER = "assets"

os.makedirs(ASSETS_FOLDER, exist_ok=True)


def create_sound(filename, duration, start_freq, end_freq, volume):
    sample_rate = 44100
    total_samples = int(sample_rate * duration)

    path = os.path.join(ASSETS_FOLDER, filename)

    with wave.open(path, "w") as sound:
        sound.setnchannels(1)
        sound.setsampwidth(2)
        sound.setframerate(sample_rate)

        for i in range(total_samples):
            progress = i / total_samples

            frequency = start_freq + (end_freq - start_freq) * progress

            envelope = 1.0
            fade_time = 0.05

            if progress < fade_time / duration:
                envelope = progress / (fade_time / duration)

            elif progress > 1 - fade_time / duration:
                envelope = (1 - progress) / (fade_time / duration)

            value = math.sin(
                2 * math.pi * frequency * i / sample_rate
            )

            value *= volume * envelope

            sample = int(value * 32767)

            sound.writeframes(
                struct.pack("<h", sample)
            )

    print("Created:", path)


create_sound(
    "engine.wav",
    2.0,
    100,
    180,
    0.20
)

create_sound(
    "collision.wav",
    0.25,
    180,
    60,
    0.45
)

create_sound(
    "mission_complete.wav",
    1.0,
    400,
    900,
    0.35
)

create_sound(
    "game_over.wav",
    1.2,
    400,
    80,
    0.35
)

create_sound(
    "background.wav",
    4.0,
    120,
    140,
    0.08
)

print()
print("================================")
print("ALL SOUND FILES CREATED!")
print("================================")