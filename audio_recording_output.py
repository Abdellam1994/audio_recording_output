import pyaudio
import wave


def get_input_device_index(port_audio, device_name):
    for index in range(port_audio.get_device_count()):
        device = port_audio.get_device_info_by_index(index)
        if device['name'] == device_name:
            print("Found!{} : nb_channels {}".format(device['name'], device.get('maxInputChannels', 0)))
            return index
    raise ValueError("Device : {} not found".format(device_name))


def get_data(sample_format, channels, rate, chunk, duration_seconds, device_name):
    print("Start recording")
    port_audio = pyaudio.PyAudio()
    index_device = get_input_device_index(port_audio, device_name)
    stream = port_audio.open(format=sample_format,
                    channels=channels,
                    rate=rate,
                    frames_per_buffer=chunk,
                    input=True,
                    input_device_index=index_device)

    frames = []  # Initialize array to store frames

    # Store data in chunk
    for i in range(int(rate / chunk * duration_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    port_audio.terminate()

    sample_size = port_audio.get_sample_size(sample_format)
    print('Finished recording')

    return frames, sample_size


def write_frames_to_file_wav(frames, filename, channels, sample_size, rate):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sample_size)
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()


def main(filename, sample_format, channels, rate, chunk, duration_seconds, device_name):
    frames, sample_size = get_data(sample_format, channels, rate, chunk, duration_seconds, device_name)
    write_frames_to_file_wav(frames, filename, channels, sample_size, rate)


if __name__ == '__main__':
    filename = 'output_test.wav'
    device_name = 'Soundflower (2ch)'
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    rate = 44100  # Record at 44100 samples per second
    duration_seconds = 30

    main(filename, sample_format, channels, rate, chunk, duration_seconds, device_name)
