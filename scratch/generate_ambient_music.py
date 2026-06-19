import os
import wave
import math
import struct
import random

def save_wav(filename, samples, sample_rate=22050):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2) # 16-bit
        f.setframerate(sample_rate)
        data = bytearray()
        for s in samples:
            val = int(max(-32768, min(32767, s * 32767)))
            data.extend(struct.pack('<h', val))
        f.writeframes(data)
    print(f"Generated: {filename} ({len(samples)} samples)")

# Sound synthesis helpers
def oscillator(phase, type='sine'):
    if type == 'sine':
        return math.sin(phase)
    elif type == 'square':
        return 1.0 if math.sin(phase) >= 0 else -1.0
    elif type == 'triangle':
        # value between -1 and 1
        p = (phase % (2 * math.pi)) / (2 * math.pi)
        if p < 0.25:
            return 4.0 * p
        elif p < 0.75:
            return 2.0 - 4.0 * p
        else:
            return -4.0 + 4.0 * p
    elif type == 'noise':
        return random.uniform(-1.0, 1.0)
    return 0.0

def make_chiptune_loop(seed, tempo=120, num_bars=4, sample_rate=22050):
    random.seed(seed)
    
    # 120 BPM: quarter note = 60/120 = 0.5s.
    # We will use 16th notes as steps. Step duration = 0.5 / 4 = 0.125s.
    step_duration = 60.0 / (tempo * 4.0)
    samples_per_step = int(step_duration * sample_rate)
    total_steps = num_bars * 16
    total_samples = total_steps * samples_per_step
    
    # Pentatonic minor scale frequencies (Key of C/A minor)
    scale = [220.00, 246.94, 261.63, 293.66, 329.63, 392.00, 440.00, 493.88, 523.25, 587.33, 659.25]
    
    # Generate simple patterns
    # Bass pattern (8 steps, repeated)
    bass_pattern = [random.choice(scale[:4]) for _ in range(8)]
    # Melody pattern (16 steps)
    melody_pattern = []
    for i in range(16):
        if random.random() < 0.6:
            melody_pattern.append(random.choice(scale[4:]))
        else:
            melody_pattern.append(0) # rest
            
    # Drum pattern: kick on steps 0, 8; snare on steps 4, 12
    
    samples = [0.0] * total_samples
    
    phase_melody = 0.0
    phase_bass = 0.0
    
    for step in range(total_steps):
        # Bass note for this step
        bass_note = bass_pattern[step % len(bass_pattern)]
        # Melody note for this step
        melody_note = melody_pattern[step % len(melody_pattern)]
        
        # Determine drum sounds
        is_kick = (step % 8 == 0)
        is_snare = (step % 8 == 4)
        is_hat = (step % 2 == 1)
        
        for s_idx in range(samples_per_step):
            global_s_idx = step * samples_per_step + s_idx
            t_step = s_idx / sample_rate
            
            # Envelope (decay) for note onsets
            env_melody = math.exp(-12.0 * t_step)
            env_bass = math.exp(-6.0 * t_step)
            
            # Synthesize melody (square wave)
            val_melody = 0.0
            if melody_note > 0:
                phase_melody += 2.0 * math.pi * melody_note / sample_rate
                val_melody = oscillator(phase_melody, 'square') * env_melody * 0.15
                
            # Synthesize bass (triangle wave)
            val_bass = 0.0
            if bass_note > 0:
                phase_bass += 2.0 * math.pi * bass_note / sample_rate
                val_bass = oscillator(phase_bass, 'triangle') * env_bass * 0.25
                
            # Synthesize drums
            val_drum = 0.0
            if is_kick:
                # Sine pitch sweep down
                kick_freq = 150.0 * math.exp(-30.0 * t_step) + 40.0
                kick_phase = 2.0 * math.pi * kick_freq * t_step
                val_drum += math.sin(kick_phase) * math.exp(-8.0 * t_step) * 0.4
            if is_snare:
                # White noise decay
                val_drum += random.uniform(-1.0, 1.0) * math.exp(-20.0 * t_step) * 0.2
            if is_hat:
                # Very short hi-hat noise
                val_drum += random.uniform(-1.0, 1.0) * math.exp(-80.0 * t_step) * 0.08
                
            # Mix
            samples[global_s_idx] = val_melody + val_bass + val_drum

    # Smooth clipping
    for idx in range(len(samples)):
        s = samples[idx]
        if s > 1.0:
            samples[idx] = 1.0
        elif s < -1.0:
            samples[idx] = -1.0
            
    return samples

def main():
    dest_dir = os.path.join("recursos", "sonidos")
    
    # Generate 8 unique 8-second loops (perfectly loopable chiptunes)
    for i in range(8):
        # Different seed and tempo for each loop
        tempo = 100 + (i * 5)
        seed = 42000 + i * 137
        samples = make_chiptune_loop(seed=seed, tempo=tempo, num_bars=4)
        filename = os.path.join(dest_dir, f"Music_{i+1}.wav")
        save_wav(filename, samples)

if __name__ == "__main__":
    main()
