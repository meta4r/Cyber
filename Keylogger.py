import pynput.keyboard
import datetime
import matplotlib.pyplot as plt

key_count = {}
current_date = str(datetime.datetime.now().date())
log_file = current_date + "_key_log.txt"

def on_press(key):
    current_time = str(datetime.datetime.now())
    try:
        key_str = str(key.char)
    except AttributeError:
        key_str = str(key)

    key_count[key_str] = key_count.get(key_str, 0) + 1

    with open(log_file, "a") as f:
        f.write(current_time + " Key pressed: " + key_str + "\n")

def on_release(key):
    current_time = str(datetime.datetime.now())
    key_str = str(key)
    with open(log_file, "a") as f:
        f.write(current_time + " Key released: " + key_str + "\n")

def plot_key_count():
    keys = list(key_count.keys())
    counts = list(key_count.values())
    plt.bar(keys, counts)
    plt.xlabel("Key")
    plt.ylabel("Count")
    plt.title("Key Count")
    plt.show()

keyboard_listener = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
keyboard_listener.start()
keyboard_listener.join()

plot_key_count()
