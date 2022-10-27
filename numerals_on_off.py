""" 
An example demonstrating how to turn numerals on and off during a real-time audio stream.

This script transcribes audio from your microphone. 
It starts the stream with numerals turned off, so if you say "one two three",
it will be transcribed as "one two three".

If you say "turn numerals on", numerals will be turned on and "one two three"
will be transcribed as "1 2 3".

You can then say "turn numerals off" to turn them off again.
"""

import string
import pyaudio
import asyncio
import sys
import websockets
import os
import json
import shutil
import argparse

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 8000

terminal_size = shutil.get_terminal_size()

audio_queue = asyncio.Queue()

def callback(input_data, frame_count, time_info, status_flag):
    audio_queue.put_nowait(input_data)
    return (input_data, pyaudio.paContinue)

async def run(key):
    extra_headers = {
        'Authorization': f'token {key}'
    }
    async with websockets.connect('wss://api.deepgram.com/v1/listen?encoding=linear16&sample_rate=16000&channels=1', extra_headers = extra_headers) as ws:
        async def microphone():
            audio = pyaudio.PyAudio()
            stream = audio.open(
                format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = CHUNK,
                stream_callback = callback
            )

            stream.start_stream()

            while stream.is_active():
                await asyncio.sleep(0.1)

            stream.stop_stream()
            stream.close()

        async def sender(ws):
            print("🟢 DG connection opened")
            try:
                while True:
                    data = await audio_queue.get()
                    await ws.send(data)
            except Exception as e:
                print('Error while sending: ', + string(e))
                raise

        async def receiver(ws):
            try:
                async for msg in ws:
                    msg = json.loads(msg)

                    if msg.get('type') == 'Error':
                        print(f'ERROR: {msg.get("description")}')
                    
                    else:
                        latest_transcript = msg.get('channel', {}).get('alternatives', [{}])[0].get('transcript')
                    
                    if msg['is_final'] and len(latest_transcript) > 0:
                        print(latest_transcript)
                        
                    if "turn on numerals" in latest_transcript or "turn numerals on" in latest_transcript:
                        print("ℹ️ Turning on numerals")
                        await ws.send(json.dumps({
                            "type": "Configure",
                            "processors": {
                                "numerals": True
                            }
                        }))

                    elif "turn off numerals" in latest_transcript or "turn numerals off" in latest_transcript:
                        print("ℹ️ Turning off numerals")
                        await ws.send(json.dumps({
                                "type": "Configure",
                                "processors": {
                                    "numerals": False
                                }
                            }))


            except Exception as e:
                print(e)

        await asyncio.wait([
            asyncio.ensure_future(microphone()),
            asyncio.ensure_future(sender(ws)),
            asyncio.ensure_future(receiver(ws))
        ])

def parse_args():
    """ Parses the command-line arguments.
    """
    parser = argparse.ArgumentParser(description='Submits data to the real-time streaming endpoint.')
    parser.add_argument('-k', '--key', required=True, help='YOUR_DEEPGRAM_API_KEY (authorization)')
    return parser.parse_args()

def main():
    args = parse_args()
    asyncio.run(run(args.key))

if __name__ == '__main__':
    sys.exit(main() or 0)
