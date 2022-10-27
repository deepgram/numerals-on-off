# numerals-on-off
Sample code for turning numeral formatting on and off during a real-time audio stream.

## Usage

`python numerals_on_off.py -k $DEEPGRAM_API_KEY`

Once the script has started, speak into your microphone and Deepgram will output the transcript into your terminal.

Numeral formatting is disabled at the start of the script. 

To enable it, say "numerals on" or "turn on numerals". 

To disable it, say "numerals off" or "turn off numerals".

To close the connection and end the script, say "goodbye".

<img width="423" alt="image" src="https://user-images.githubusercontent.com/3937986/198396295-7c0a2b0b-381e-434c-95ef-a0d128f43766.png">

_Protip: store your Deepgram API key in an environment variable so it doesn't appear in your bash history._
