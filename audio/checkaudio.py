import wave

def check_audio_format(filename):
    try:
        with wave.open(filename, 'rb') as wf:
            channels = wf.getnchannels()
            sample_width = wf.getsampwidth()
            frame_rate = wf.getframerate()
            print("Channels:", channels)
            print("Sample width (bytes):", sample_width)
            print("Frame rate (Hz):", frame_rate)
            if channels == 1 and sample_width == 2 and frame_rate == 44100:
                print("Audio format: PCM WAV")
            else:
                print("The audio format is not a PCM WAV")
    except wave.Error as e:
        print("Failed to open the audio file:", e)


check_audio_format("AUDIO.wav")
