"""
Music controls T-rex!

Play the notes (changeable) to control the T-Rex from the link: http://www.trex-game.skipser.com/  (or any T-Rex
that has same controls).

documentation:

    Aubio and Pyaudio setup: https://gist.github.com/notalentgeek/48aeab398b6b74e3a9134a61b6b79a36
    Simulate Key Presses: https://www.youtube.com/watch?v=DTnz8wA6wpw&feature=emb_logo
    Return Key by knowing Vlaue of an item in dictionary
https://stackoverflow.com/questions/3545331/how-can-i-get-dictionary-key-as-variable-directly-in-python-not-by-searching-fr
    Closest number from a list with a given number
https://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value

"""
import aubio
import numpy as num
import pyaudio
import sys
import time
from selenium import webdriver
from pynput.keyboard import Key, Controller
from win32gui import GetWindowText, GetForegroundWindow # importing this to make sure that the user is in the game
# import pyautogui #Tried to clear the screen so i get better visuals with pyautogui.hotkey(cls). Variable worked better
# import winsound # for beep reference


kb = Controller()
# kb.press/release('key')  #Object that allows me to use keyboard

# HERTZ TO MUSICAL NOTES CONVERTER!
my_dict = {
    "C0": 16,
    "C#0/Db0": 17,
    "D0": 18,
    "D#0/Eb0": 19,
    "E0": 20,
    "F0": 21,
    "F#0/Gb0": 23,
    "G0": 24,
    "G#0/Ab0": 25,
    "A0": 27,
    "A#0/Bb0": 29,
    "B0": 30,
    "C1": 32,
    "C#1/Db1": 34,
    "D1": 36,
    "D#1/Eb1": 38,
    "E1": 41,
    "F1": 43,
    "F#1/Gb1": 46,
    "G1": 49,
    "G#1/Ab1": 51,
    "A1": 55,
    "A#1/Bb1": 58,
    "B1": 61,
    "C2": 65,
    "C#2/Db2": 69,
    "D2": 73,
    "D#2/Eb2": 77,
    "E2": 82,
    "F2": 87,
    "F#2/Gb2": 92,
    "G2": 98,
    "G#2/Ab2": 103,
    "A2": 110,
    "A#2/Bb2": 116,
    "B2": 123,
    "C3": 130,
    "C#3/Db3": 138,
    "D3": 146,
    "D#3/Eb3": 155,
    "E3": 164,
    "F3": 174,
    "F#3/Gb3": 185,
    "G3": 196,
    "G#3/Ab3": 207,
    "A3": 220,
    "A#3/Bb3": 233,
    "B3": 246,
    "C4": 261,
    "C#4/Db4": 277,
    "D4": 293,
    "D#4/Eb4": 311,
    "E4": 329,
    "F4": 349,
    "F#4/Gb4": 369,
    "G4": 392,
    "G#4/Ab4": 415,
    "A4": 440,
    "A#4/Bb4": 466,
    "B4": 493,
    "C5": 523,
    "C#5/Db5": 554,
    "D5": 587,
    "D#5/Eb5": 622,
    "E5": 659,
    "F5": 698,
    "F#5/Gb5": 739,
    "G5": 783,
    "G#5/Ab5": 830,
    "A5": 880,
    "A#5/Bb5": 932,
    "B5": 987,
    "C6": 1046,
    "C#6/Db6": 1108,
    "D6": 1174,
    "D#6/Eb6": 1244,
    "E6": 1318,
    "F6": 1396,
    "F#6/Gb6": 1479,
    "G6": 1567,
    "G#6/Ab6": 1661,
    "A6": 1760,
    "A#6/Bb6": 1864,
    "B6": 1975,
    "C7": 2093,
    "C#7/Db7": 2217,
    "D7": 2349,
    "D#7/Eb7": 2489,
    "E7": 2637,
    "F7": 2793,
    "F#7/Gb7": 2959,
    "G7": 3135,
    "G#7/Ab7": 3322,
    "A7": 3520,
    "A#7/Bb7": 3729,
    "B7": 3951,
    "C8": 4186,
    "C#8/Db8": 4434,
    "D8": 4698,
    "D#8/Eb8": 4978,
    "E8": 5274,
    "F8": 5587,
    "F#8/Gb8": 5919,
    "G8": 6271,
    "G#8/Ab8": 6644,
    "A8": 7040,
    "A#8/Bb8": 7458,
    "B8": 7902,
}

# Being able to access the key knowing the value (Did because i didn't want to edit every single item)
key_list = list(my_dict.keys())
val_list = list(my_dict.values())


# Some constants for setting the PyAudio and the Aubio
BUFFER_SIZE = 2048
FORMAT = pyaudio.paFloat32
CHANNELS = 1
METHOD = "default"
SAMPLE_RATE = 44100
HOP_SIZE = BUFFER_SIZE//2
PERIOD_SIZE_IN_FRAME = HOP_SIZE

def main():

    # Initiating PyAudio object.
    pA = pyaudio.PyAudio()
    # Open the microphone stream.
    mic = pA.open(format=FORMAT, channels=CHANNELS, rate=SAMPLE_RATE, input=True, frames_per_buffer=PERIOD_SIZE_IN_FRAME)
    # Initiating Aubio's pitch detection object.
    pDetection = aubio.pitch(METHOD, BUFFER_SIZE, HOP_SIZE, SAMPLE_RATE)
    # Set unit.
    pDetection.set_unit("Hz")
    # Frequency under -40 dB will considered as a silence.
    pDetection.set_silence(-40)
    # Initializing the variable that allows me to clear screen
    last_one_printed_out = '         '

    # Asking for user input
    print('''
    
-------------------- Music controls T-rex --------------------------------

Play the notes (changeable) D,G,A to control the T-Rex from the link: 
http://www.trex-game.skipser.com/  (or any T-Rex that has same controls)

You might want to TURN OFF your AUDIO, because this program might get 
sound from the T-Rex Game (beeps), and that will make you 

We would like to know what notes will you use to control the T-Rex!
Example of input: G
*do not use # or b

Your input:
    ''')
    jumpNote = input("What note will you use to JUMP?: ")
    getDownNote = input("What note will you use to CROUCH?: ")
    getUpNote = input("What note will you use to GET BACK up from crouching?: ")
    time.sleep(.5)
    print("We are opening the game... The game will start in 3 seconds. To EXIT click X")
    # Opening the game with selenium.
    # if web == chrome:, but safari????????????????????????????????????????????????????????????????????????????????????
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--mute-audio")
    DRIVER_PATH = 'chromedriver.exe'
    driver = webdriver.Chrome(DRIVER_PATH, options=chrome_options)
    driver.get('http://www.trex-game.skipser.com/')

    counter = 3
    while counter>0:
        time.sleep(1)
        print(counter)
        counter -= 1
    time.sleep(1)
    print('MUSIC CONTROLLER IS ON! Click X to EXIT')

    # Infinite loop, could make some breaks here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    try:
        while True:
            # Always listening to the microphone.
            data = mic.read(PERIOD_SIZE_IN_FRAME)
            # Convert into number that Aubio understand.
            samples = num.frombuffer(data, dtype=aubio.float_type)

            # Finally get the pitch.
            pitch = pDetection(samples)[0]

            # If it detects any pitch, it prints it to console, then different notes press different keys on kb
            if pitch == 0:
                pass
            else:
                # Algorithm that approximates the closest note (e.g.: pitch=310hz, but we have no note with 310, so we get 311hz=D
                approx_val = min(val_list, key=lambda x: abs(x - int(pitch)))
                # We have to make sure we're in the correct window, so we don't mess up with user's PC
                focusedWindow5Chars = ''
                try:
                    focusedWindow = GetWindowText(GetForegroundWindow())
                    for chars in range(5):
                        focusedWindow5Chars += focusedWindow[chars]
                # if we arent able to get the window name, that means we re not in the god one
                except:
                    pass
                # So we have a note = 'D#3/Eb3', note[0]=='D', note[1]=='#; n
                # key_list[val_list.index(approx_val)] returns the note from the dictionary using those arrays
                note = key_list[val_list.index(approx_val)]
                if focusedWindow5Chars == "T-Rex":
                    if note[0] == getUpNote:
                        kb.release(Key.down)
                        kb.release(Key.up)
                    elif note[0] == jumpNote:
                        kb.press(Key.up)
                    elif note[0] == getDownNote:
                        kb.press(Key.down)

                    # The printing
                    if last_one_printed_out[0] == note[0] and last_one_printed_out[1] == note[1]:
                        pass
                    else:
                        if note[1] == '#':
                            print(note[0], note[1])
                        else:
                            print(note[0])
                    last_one_printed_out = note
                else:
                    if last_one_printed_out[0] != 'Y':
                        wrongWindowmMsg = 'You are in the wrong window, please return to the T-Rex Game window!'
                        print(wrongWindowmMsg)
                    last_one_printed_out = wrongWindowmMsg
    except KeyboardInterrupt:
        pass


main()
