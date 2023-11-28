import tkinter as tk
from tkinter import Label, Entry, Button, messagebox
import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage
from fractions import Fraction

# Dictionary to map rhythm descriptions to their corresponding durations
RHYTHM_DURATIONS = {
    'q': 1,
    'e': 0.5,
    'aq': 1,
    'ae': 0.5,
}

class MidiGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MIDI Rhythm Generator")

        self.label1 = Label(root, text="Enter Time Signature (e.g., '4/4'):")
        self.label1.pack()

        self.time_signature_entry = Entry(root, width=10)
        self.time_signature_entry.pack()

        self.label2 = Label(root, text="Enter Rhythm Description:")
        self.label2.pack()

        self.rhythm_entry = Entry(root, width=50)
        self.rhythm_entry.pack()

        self.label3 = Label(root, text="Enter Tempo (default is 120 BPM):")
        self.label3.pack()

        self.tempo_entry = Entry(root, width=10)
        self.tempo_entry.insert(0, "120")
        self.tempo_entry.pack()

        self.generate_button = Button(root, text="Generate MIDI", command=self.generate_midi)
        self.generate_button.pack()

    def generate_midi(self):
        time_signature_str = self.time_signature_entry.get()
        rhythm_description = self.rhythm_entry.get()
        tempo_str = self.tempo_entry.get()

        try:
            time_signature = self.parse_time_signature(time_signature_str)
            tempo = self.parse_tempo(tempo_str)
            midi_file = self.create_midi(rhythm_description, time_signature, tempo)
            messagebox.showinfo("MIDI Generated", "MIDI file generated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error generating MIDI: {e}")

    def parse_time_signature(self, time_signature_str):
        # Parsing time signature
        try:
            numerator, denominator = map(int, time_signature_str.split('/'))
            return Fraction(numerator, denominator)
        except ValueError:
            raise ValueError("Invalid time signature format. Please use the format 'numerator/denominator'.")

    def parse_tempo(self, tempo_str):
        # Parsing tempo
        try:
            return int(tempo_str)
        except ValueError:
            raise ValueError("Invalid tempo. Please enter a valid integer.")

    def create_midi(self, rhythm_description, time_signature, tempo):
        # Parsing rhythm description
        rhythm_tokens = rhythm_description.split()
        midi_file = MidiFile(ticks_per_beat=480)
        track = MidiTrack()
        midi_file.tracks.append(track)

        # Setting time signature
        ticks_per_beat = midi_file.ticks_per_beat
        time_signature_message = MetaMessage('time_signature', numerator=time_signature.numerator,
                                             denominator=time_signature.denominator,
                                             clocks_per_click=24, notated_32nd_notes_per_beat=8)
        track.append(time_signature_message)

        # Setting tempo
        tempo_message = MetaMessage('set_tempo', tempo=mido.bpm2tempo(tempo))
        track.append(tempo_message)

        # Adding notes and rests based on rhythm description
        tick_duration = int(mido.second2tick(1, ticks_per_beat=ticks_per_beat, tempo=500000))
        tick_offset = 0

        for i, token in enumerate(rhythm_tokens):
            if token[0] == 'r':
                rest_duration = int(token[1]) if len(token) > 1 else 1
                tick_offset += int(tick_duration * (rest_duration / 16))  # Duration of rest in 16th notes
            elif token in RHYTHM_DURATIONS:
                if token[0] == 'a':
                    velocity = 90  # Default velocity for accented notes
                else:
                    velocity = 45  # Default velocity for non-accented notes

                track.append(Message('note_on', note=60, velocity=velocity, time=tick_offset))
                track.append(Message('note_off', note=60, velocity=velocity, time=int(tick_duration * RHYTHM_DURATIONS[token])))
                tick_offset = 0  # Reset tick_offset for the next note

        midi_file.save('output.mid')
        return midi_file

if __name__ == "__main__":
    root = tk.Tk()
    app = MidiGeneratorApp(root)
    root.mainloop()
