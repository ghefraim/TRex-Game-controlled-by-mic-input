from win32gui import GetWindowText, GetForegroundWindow
import time

time.sleep(3)
focusedWindow = GetWindowText(GetForegroundWindow())
focusedWindow10Chars = ''
for chars in range(10):
    focusedWindow10Chars += focusedWindow[chars]
print (focusedWindow10Chars)