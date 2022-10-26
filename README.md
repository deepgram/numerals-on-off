# numerals-on-off
Sample code for turning numeral formatting on and off during a real-time audio stream.

## Usage

`python numerals_on_off.py -k $DEEPGRAM_API_KEY`

You can store your Deepgram API key in an environment variable (recommended so it doesn't appear in your bash history) or pass it in as a string.

Once the script has started, speak into your microphone and Deepgram will output the transcript into your terminal.

Numeral formatting is disabled at the start of the script. To enable it, say "turn numerals on". To disable it, say "turn numerals off".

<img width="421" alt="image" src="https://user-images.githubusercontent.com/3937986/197908175-6972dccc-0a77-41b0-95d6-e413d82f95c9.png">

