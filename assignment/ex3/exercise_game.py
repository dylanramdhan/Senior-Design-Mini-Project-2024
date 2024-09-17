"""
Response time - single-threaded
"""
from machine import Pin
import network
import time
import random
import urequests
import ujson

N: int = 10
sample_ms = 10.0
on_ms = 500

# Fill in network info
ssid = "Beren"
password = "Istanbul2002."

# Setup WiFi connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for the connection to be established
while not wlan.isconnected():
    print("Connecting to network...")
    time.sleep(1)

print("Connected to network:", wlan.ifconfig())

# Send a POST request to Firebase


def random_time_interval(tmin: float, tmax: float) -> float:
    """Return a random time interval between tmin and tmax."""
    return random.uniform(tmin, tmax)


def blinker(N: int, led: Pin) -> None:
    """Blink the LED N times to indicate the start or end of the game."""
    for _ in range(N):
        led.high()
        time.sleep(0.1)
        led.low()
        time.sleep(0.1)


def write_json(json_filename: str, data: dict) -> None:
    """Writes data to a JSON file."""
    with open(json_filename, "w") as f:
        ujson.dump(data, f)


def scorer(t: list[int | None]) -> None:
    """Calculate and print the score and response times."""
    misses = t.count(None)
    print("You missed the light {misses} / {len(t)} times")

    t_good = [x for x in t if x is not None]

    if len(t_good) == 0:
        print("Did not press the button, this means you don't have a score")
        data = {}
    else:
        max_resp = max(t_good)
        min_resp = min(t_good)
        mean_resp = sum(t_good) / len(t_good)
        data = {
            "Maximum Response Time": max_resp, 
            "Minimum Response Time": min_resp, 
            "Mean Response Time": mean_resp
        }
        
        print(data)

    # Make dynamic filename and write JSON
    now = time.localtime()
    now_str = "-".join(map(str, now[:3])) + "T" + "_".join(map(str, now[3:6]))
    filename = f"score-{now_str}.json"
    
    print(f"Writing to {filename}")
    
    write_json(filename, data)
        
    try:
        res = urequests.post('https://ec463-miniproject-9d0c7-default-rtdb.firebaseio.com/test.json', 
                             data=ujson.dumps(data))

        if res.status_code == 200:
            print("Data sent successfully!")
        else:
            print(f"Failed to send data. Status code: {res.status_code}")
    except Exception as e:
        print(f"Error sending data: {e}")


if __name__ == "__main__":
    led = Pin("LED", Pin.OUT)
    button = Pin(15, Pin.IN, Pin.PULL_UP)

    t: list[int | None] = []
 
    blinker(3, led)

    for i in range(N):
        time.sleep(random_time_interval(0.5, 5.0))

        led.high()

        tic = time.ticks_ms()
        t0 = None
        while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
            if button.value() == 0:
                t0 = time.ticks_diff(time.ticks_ms(), tic)
                led.low()
                break
        t.append(t0)

        led.low()

    blinker(5, led)

    scorer(t)
    

