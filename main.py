"""Command line interface for Sine Pulse Synth."""

import argparse
import sys
from engine import SynthesizerEngine

def parse_harmonics(val: str) -> list:
    try:
        return [float(x) for x in val.split(",")]
    except ValueError as err:
        raise argparse.ArgumentTypeError("Harmonics must be comma-separated floats (e.g., 1,0.5,0.25)") from err

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Additive synthesizer and sequencer generating raw PCM audio."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    gen_parser = subparsers.add_parser("generate", help="Generate an audio file from a pattern")
    gen_parser.add_argument("--output", required=True, help="Path to output WAV file")
    gen_parser.add_argument("--tempo", type=int, default=120, help="Tempo in BPM (default: 120)")
    gen_parser.add_argument("--pattern", default="C4,E4,G4,B4", help="Comma-separated notes (e.g. C4,E4,REST,G4)")
    gen_parser.add_argument("--harmonics", type=parse_harmonics, default=[1.0, 0.5, 0.25], help="Harmonic weights")

    args = parser.parse_args()

    if args.command == "generate":
        print(f"[INFO] Initialized synthesizer engine at 44100 Hz")
        notes = [n.strip() for n in args.pattern.split(",")]
        print(f"[INFO] Compiling pattern: {notes} at {args.tempo} BPM")
        
        engine = SynthesizerEngine()
        try:
            buffer = engine.render_sequence(notes, args.tempo, args.harmonics)
            engine.write_wav(args.output, buffer)
            print(f"[SUCCESS] Render complete. File written to {args.output}")
        except Exception as e:
            print(f"[ERROR] Render failed: {e}", file=sys.stderr)
            return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
