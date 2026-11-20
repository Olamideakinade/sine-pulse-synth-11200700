"""Core DSP engine for additive synthesis and step sequencing."""

import math
import struct
import wave
from typing import List, Dict

NOTE_FREQUENCIES: Dict[str, float] = {
    "C3": 130.81,
    "C#3": 138.59,
    "D3": 146.83,
    "D#3": 155.56,
    "E3": 164.81,
    "F3": 174.61,
    "F#3": 185.00,
    "G3": 196.00,
    "G#3": 207.65,
    "A3": 220.00,
    "A#3": 233.08,
    "B3": 246.94,
    "C4": 261.63,
    "C#4": 277.18,
    "D4": 293.66,
    "D#4": 311.13,
    "E4": 329.63,
    "F4": 349.23,
    "F#4": 369.99,
    "G4": 392.00,
    "G#4": 415.30,
    "A4": 440.00,
    "A#4": 466.16,
    "B4": 493.88,
    "C5": 523.25,
}

class SynthesizerEngine:
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate

    def note_to_freq(self, note: str) -> float:
        cleaned = note.strip().upper()
        if cleaned in NOTE_FREQUENCIES:
            return NOTE_FREQUENCIES[cleaned]
        raise ValueError(f"Unknown note identifier: {note}")

    def generate_tone(self, freq: float, duration: float, harmonics: List[float], volume: float = 0.5) -> List[float]:
        num_samples = int(self.sample_rate * duration)
        buffer = [0.0] * num_samples
        
        norm_harmonics = [h / sum(harmonics) for h in harmonics] if sum(harmonics) > 0 else harmonics

        for i in range(num_samples):
            t = i / self.sample_rate
            sample = 0.0
            for harmonic_index, weight in enumerate(norm_harmonics, start=1):
                if weight == 0:
                    continue
                harmonic_freq = freq * harmonic_index
                envelope = min(1.0, (num_samples - i) / (self.sample_rate * 0.05)) * min(1.0, i / (self.sample_rate * 0.01))
                sample += math.sin(2.0 * math.pi * harmonic_freq * t) * weight * envelope
            
            buffer[i] = sample * volume

        return buffer

    def render_sequence(self, pattern: List[str], tempo: int, harmonics: List[float]) -> List[float]:
        beat_duration = 60.0 / tempo
        master_buffer: List[float] = []

        for note in pattern:
            if note.upper() == "REST" or note == "":
                master_buffer.extend([0.0] * int(self.sample_rate * beat_duration))
            else:
                freq = self.note_to_freq(note)
                tone = self.generate_tone(freq, beat_duration, harmonics)
                master_buffer.extend(tone)

        return master_buffer

    def write_wav(self, filepath: str, buffer: List[float]) -> None:
        max_val = max(abs(x) for x in buffer) if buffer else 1.0
        if max_val == 0:
            max_val = 1.0

        scaled_buffer = [int((x / max_val) * 32767) for x in buffer]
        
        with wave.open(filepath, "w") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.sample_rate)
            
            data = struct.pack(f"<{len(scaled_buffer)}h", *scaled_buffer)
            wav_file.writeframes(data)
