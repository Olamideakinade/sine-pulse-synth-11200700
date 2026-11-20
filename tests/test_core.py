import unittest
from engine import SynthesizerEngine

class TestSynthesizerEngine(unittest.TestCase):
    def setUp(self):
        self.engine = SynthesizerEngine(sample_rate=8000)

    def test_note_to_freq_valid(self):
        freq = self.engine.note_to_freq("A4")
        self.assertEqual(freq, 440.0)

    def test_note_to_freq_invalid(self):
        with self.assertRaises(ValueError):
            self.engine.note_to_freq("H9")

    def test_generate_tone_length(self):
        tone = self.engine.generate_tone(440.0, 0.5, [1.0, 0.5])
        self.assertEqual(len(tone), 4000)

    def test_render_sequence(self):
        pattern = ["C4", "REST", "C4"]
        buffer = self.engine.render_sequence(pattern, tempo=120, harmonics=[1.0])
        self.assertGreater(len(buffer), 0)

if __name__ == "__main__":
    unittest.main()
