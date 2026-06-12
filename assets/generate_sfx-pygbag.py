import wave
import struct
import math
import random
import os

SAMPLE_RATE = 44100

def save_wav(filename, samples):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        for sample in samples:
            # clamp and pack
            s = max(-32768, min(32767, int(sample * 32767)))
            wav_file.writeframes(struct.pack('<h', s))

def generate_square_wave(freq, duration, volume=0.5):
    samples = []
    num_samples = int(SAMPLE_RATE * duration)
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        val = 1.0 if (t * freq) % 1.0 < 0.5 else -1.0
        samples.append(val * volume)
    return samples

def generate_blip():
    return generate_square_wave(440, 0.05, 0.3)

def generate_select():
    s1 = generate_square_wave(880, 0.05, 0.3)
    s2 = generate_square_wave(1318.51, 0.1, 0.3) # E6
    return s1 + s2

def generate_coin():
    s1 = generate_square_wave(987.77, 0.1, 0.3) # B5
    s2 = generate_square_wave(1318.51, 0.3, 0.3) # E6
    return s1 + s2

def generate_powerup():
    samples = []
    duration = 0.5
    num_samples = int(SAMPLE_RATE * duration)
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        # Rising sweep
        freq = 400 + (t / duration) * 800
        val = 1.0 if (t * freq) % 1.0 < 0.5 else -1.0
        samples.append(val * 0.3)
    return samples

def generate_crash():
    samples = []
    duration = 0.5
    num_samples = int(SAMPLE_RATE * duration)
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        noise = random.uniform(-1.0, 1.0)
        envelope = max(0, 1.0 - (t / duration)) ** 2 # exponential decay
        samples.append(noise * envelope * 0.5)
    return samples

def generate_menu_music():
    # Slow, calm 4-second loop
    samples = []
    duration = 4.0
    num_samples = int(SAMPLE_RATE * duration)
    notes = [261.63, 329.63, 392.00, 523.25] # C, E, G, C
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        note_idx = int((t % 1.0) * 4) # 4 notes per second
        freq = notes[note_idx]
        val = 1.0 if (t * freq) % 1.0 < 0.5 else -1.0
        # low pass filter / soften
        samples.append(val * 0.1)
    return samples

def generate_game_music():
    # Fast, pulsing 2-second loop
    samples = []
    duration = 2.0
    num_samples = int(SAMPLE_RATE * duration)
    notes = [130.81, 130.81, 155.56, 146.83] # C3, C3, Eb3, D3
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        note_idx = int((t % 0.5) * 8) % 4 # 8 notes per second
        freq = notes[note_idx]
        val = 1.0 if (t * freq) % 1.0 < 0.5 else -1.0
        # Envelope pulsing
        envelope = 1.0 - ((t % 0.125) / 0.125)
        samples.append(val * envelope * 0.15)
    return samples

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sounds_dir = os.path.join(base_dir, "sounds")
    os.makedirs(sounds_dir, exist_ok=True)
    
    save_wav(os.path.join(sounds_dir, "blip.ogg"), generate_blip())
    save_wav(os.path.join(sounds_dir, "select.ogg"), generate_select())
    save_wav(os.path.join(sounds_dir, "coin.ogg"), generate_coin())
    save_wav(os.path.join(sounds_dir, "powerup.ogg"), generate_powerup())
    save_wav(os.path.join(sounds_dir, "crash.ogg"), generate_crash())
    save_wav(os.path.join(sounds_dir, "menu_music.ogg"), generate_menu_music())
    save_wav(os.path.join(sounds_dir, "game_music.ogg"), generate_game_music())
    print("Generated all sound effects and music!")
