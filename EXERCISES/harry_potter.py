import machine
import utime

SPEAKER_PIN = 16

speaker = machine.PWM(machine.Pin(SPEAKER_PIN))

NOTE_FREQUENCIES = {
    'B4': 494,
    'E5': 659,
    'G5': 784,
    'F#5': 740,
    'A5': 880,
    'E6': 1319,
    'D#6': 1245,
    'F#6': 1480,
}

DylanAndBerenTheme = [
    ('E5', 0.5), ('G5', 0.5), ('F#5', 0.5), ('E5', 0.5),
    ('B4', 0.5), ('E5', 0.5), ('G5', 0.5), ('A5', 0.5),
    ('F#5', 0.5), ('E5', 0.5), ('B4', 0.5), ('E6', 0.5),
    ('D#6', 0.5), ('B4', 0.5), ('F#6', 0.5)
]

def playtone(frequency: float, duration: float) -> None:
    """Plays a tone at the given frequency for the given duration."""
    speaker.duty_u16(1000)
    speaker.freq(frequency)
    utime.sleep(duration)
    quiet()

def quiet():
    """Stops the sound (duty cycle set to 0)."""
    speaker.duty_u16(0)

print("Playing Harry Potter Hedwig's theme:")

for note, duration in DylanAndBerenTheme:
    print(f"Playing note {note} ({NOTE_FREQUENCIES[note]} Hz) for {duration} seconds")
    playtone(NOTE_FREQUENCIES[note], duration)

quiet()

