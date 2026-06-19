import os
import wave
import math
import struct

def save_wav(filename, samples, sample_rate=22050):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2) # 16-bit
        f.setframerate(sample_rate)
        # Convert samples to 16-bit binary PCM
        data = bytearray()
        for s in samples:
            val = int(max(-32768, min(32767, s * 32767)))
            data.extend(struct.pack('<h', val))
        f.writeframes(data)
    print(f"Generated: {filename} ({len(samples)} samples)")

def generate_tone(freq, duration, type='sine', sample_rate=22050, volume=0.5):
    num_samples = int(duration * sample_rate)
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        # Envelope: linear decay
        envelope = 1.0 - (i / num_samples)
        
        if type == 'sine':
            val = math.sin(2 * math.pi * freq * t)
        elif type == 'square':
            val = 1.0 if math.sin(2 * math.pi * freq * t) >= 0 else -1.0
        elif type == 'triangle':
            val = 2.0 * abs(2.0 * (t * freq - math.floor(t * freq + 0.5))) - 1.0
        else:
            val = math.sin(2 * math.pi * freq * t)
            
        samples.append(val * envelope * volume)
    return samples

def generate_slide(freq_start, freq_end, duration, type='sine', sample_rate=22050, volume=0.5):
    num_samples = int(duration * sample_rate)
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        envelope = 1.0 - (i / num_samples)
        # Linear interpolation of frequency
        freq = freq_start + (freq_end - freq_start) * (i / num_samples)
        phase = 2 * math.pi * freq * t
        
        if type == 'sine':
            val = math.sin(phase)
        elif type == 'square':
            val = 1.0 if math.sin(phase) >= 0 else -1.0
        elif type == 'triangle':
            val = 2.0 * abs(2.0 * (t * freq - math.floor(t * freq + 0.5))) - 1.0
        else:
            val = math.sin(phase)
            
        samples.append(val * envelope * volume)
    return samples

def generate_melody(notes, note_duration, type='sine', sample_rate=22050, volume=0.5):
    samples = []
    for note in notes:
        if note == 0: # rest
            samples.extend([0.0] * int(note_duration * sample_rate))
        else:
            samples.extend(generate_tone(note, note_duration, type, sample_rate, volume))
    return samples

# Frequencies of notes
C4 = 261.63
D4 = 293.66
E4 = 329.63
F4 = 349.23
G4 = 392.00
A4 = 440.00
B4 = 493.88
C5 = 523.25
E5 = 659.25
G5 = 783.99
C6 = 1046.50

def main():
    dest_dir = os.path.join("recursos", "sonidos")
    
    # 1. Correcta.wav: Pleasant high-pitched arpeggio chime (C5 -> E5 -> G5)
    correct_samples = []
    correct_samples.extend(generate_tone(C5, 0.08, 'sine', volume=0.4))
    correct_samples.extend(generate_tone(E5, 0.08, 'sine', volume=0.4))
    correct_samples.extend(generate_tone(G5, 0.15, 'sine', volume=0.4))
    save_wav(os.path.join(dest_dir, "Correcta.wav"), correct_samples)
    
    # 2. equivocado.wav: Buzzy descending crash/error slide
    wrong_samples = generate_slide(300, 100, 0.35, 'square', volume=0.25)
    save_wav(os.path.join(dest_dir, "equivocado.wav"), wrong_samples)
    
    # 3. Title.wav: Short cheerful title screen melody (C4 -> E4 -> G4 -> C5 -> G4 -> C5)
    title_notes = [C4, E4, G4, C5, G4, C5]
    title_samples = generate_melody(title_notes, 0.2, 'triangle', volume=0.35)
    save_wav(os.path.join(dest_dir, "Title.wav"), title_samples)
    
    # 4. ganador.wav: Triumphant ascending fanfare
    victory_notes = [C5, E5, G5, C6]
    victory_samples = []
    victory_samples.extend(generate_tone(C5, 0.15, 'sine', volume=0.4))
    victory_samples.extend(generate_tone(E5, 0.15, 'sine', volume=0.4))
    victory_samples.extend(generate_tone(G5, 0.15, 'sine', volume=0.4))
    victory_samples.extend(generate_tone(C6, 0.40, 'triangle', volume=0.35))
    save_wav(os.path.join(dest_dir, "ganador.wav"), victory_samples)
    
    # 5. GameOver.wav: Sad descending melody (G4 -> E4 -> C4)
    defeat_notes = [G4, E4, C4]
    defeat_samples = []
    defeat_samples.extend(generate_tone(G4, 0.3, 'sine', volume=0.4))
    defeat_samples.extend(generate_tone(E4, 0.3, 'sine', volume=0.4))
    defeat_samples.extend(generate_slide(C4, C4 / 2, 0.6, 'sine', volume=0.4))
    save_wav(os.path.join(dest_dir, "GameOver.wav"), defeat_samples)

if __name__ == "__main__":
    main()
