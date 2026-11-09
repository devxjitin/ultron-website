"""What the phone shows for every example in the docs. The page script (dist/page.js) knows these screen kinds:

  voice    the real voice screen; Ultron only answers aloud (needs `reply`)
  search   an app's search box: the cursor taps it, types, presses Enter, results appear (app, text, results)
  chat     a messaging app: the cursor taps the box, types a reply and presses Send (name, incoming, reply)
  scan     Ultron reads the screen and numbers what it can press (rows)
  scroll   a long list scrolls (rows)
  shot     a screenshot is taken (rows)
  back     Back is pressed and the page slides away (app, page)
  ytdl     a YouTube download with progress, then the file lands in Downloads/Ultron (title, quality, file, size)
  alarm    a new alarm appears in the clock app (time, label, optional old)
  timer    a countdown timer starts (start)
  calendar a day view; an event is added or a free slot is shown (slots, events, new or free)
  tiles    quick settings, one tile switches on (tile)
  slider   a level moves (label, to, start)
  call     a call is placed, or Ultron asks which contact (name, optional ask)
  route    directions start in maps (dest)
  launch   an app is opened from the grid (app, index)
  list     a list screen with one row picked (title, rows, pick, optional note)
  weather  a weather card (city, temp, cond, days)
  photo    a saved picture is shown (caption)
  wait     Ultron waits for text to appear (text, busy)
  notif    a reminder notification lands on the lock screen (title, text)

Values shown on screen are examples, not real data."""


def v(reply):
    return {"kind": "voice", "reply": reply}


CONNECTORS = {
    "device_info": [
        v("Battery is at 82 percent and charging. You have 41 GB of storage free."),
        v("You are on HomeNet Wi-Fi and the signal is strong."),
        v("This phone runs Android 15 and the language is set to English."),
    ],
    "device_controls": [
        {"kind": "tiles", "tile": "Flashlight"},
        {"kind": "tiles", "tile": "Do Not Disturb"},
        {"kind": "slider", "label": "Brightness", "start": 35, "to": 100},
    ],
    "alarms": [
        {"kind": "alarm", "time": "6:30 AM", "label": "Tomorrow"},
        {"kind": "timer", "start": 600},
        {"kind": "alarm", "time": "6:00 AM", "label": "Tomorrow", "old": "5:30 AM"},
    ],
    "reminders": [
        {"kind": "notif", "title": "Reminder", "text": "Take medicine", "time": "9:00"},
        {"kind": "notif", "title": "Reminder", "text": "Call Mummy", "time": "4:30"},
        {"kind": "notif", "title": "Reminder", "text": "Call Mummy, now at 4 PM", "time": "4:00"},
    ],
    "apps_settings": [
        {"kind": "launch", "app": "Calculator", "index": 4},
        {"kind": "list", "title": "Share with", "rows": ["WhatsApp", "Messages", "Gmail"], "pick": 0},
        {"kind": "list", "title": "Instagram, App info", "rows": ["Permissions", "Storage", "Uninstall"], "pick": 0},
    ],
    "weather": [
        {"kind": "weather", "city": "Your location", "temp": "31", "cond": "Light rain later", "days": ["Tue 32", "Wed 30", "Thu 29"]},
        {"kind": "weather", "city": "Manali", "temp": "14", "cond": "Clear", "days": ["Sat 15", "Sun 13", "Mon 12"]},
        {"kind": "weather", "city": "Your location", "temp": "34", "cond": "Hot and sunny", "days": ["Tue 35", "Wed 34", "Thu 33"]},
    ],
    "duckduckgo": [
        v("I searched the web for it. The latest result says the match ended last night, and I will read out the score."),
        v("I found a few recent reviews. Most of them pick the same two pairs under 2000 rupees."),
        v("Here is today's rate from the latest result I found."),
    ],
    "web_reader": [
        v("I opened the link. In short, here are the main points of the article."),
        v("From the page, the ingredients are listed: I will read them out one by one."),
        v("The page says refunds are explained in its refund section. I will read that part."),
    ],
    "youtube": [
        {"kind": "list", "title": "YouTube, React hooks", "rows": ["React Hooks in 30 minutes", "useEffect explained", "Custom hooks, step by step"], "pick": 0},
        v("I read the captions. In short, the video explains the main idea first and then shows an example."),
        {"kind": "list", "title": "Latest videos", "rows": ["Newest upload", "Last week's upload", "Two weeks ago"], "pick": 0},
    ],
    "youtube_downloads": [
        {"kind": "ytdl", "title": "Lo-fi beats to study to", "quality": "720p", "file": "Lo-fi beats to study to.mp4", "size": "84 MB"},
        {"kind": "ytdl", "title": "Lo-fi beats to study to", "quality": "Audio only", "file": "Lo-fi beats to study to.m4a", "size": "58 MB"},
        {"kind": "list", "title": "Download options", "rows": ["360p video", "720p video", "1080p video", "Audio only"], "pick": 1},
    ],
    "calendar": [
        {"kind": "calendar", "events": {"10 AM": "Standup", "2 PM": "Design review"}},
        {"kind": "calendar", "events": {"10 AM": "Standup", "2 PM": "Design review"}, "free": "4 PM"},
        {"kind": "calendar", "events": {"10 AM": "Standup", "2 PM": "Design review"}, "new": {"6 PM": "Dentist"}},
    ],
    "contacts": [
        {"kind": "list", "title": "Contacts", "rows": ["Rahul Sharma", "Rahul Verma", "Rahul K."], "pick": 0, "note": "98xxxx xx21"},
        v("I found Priya in your contacts. Her birthday is saved on her contact card."),
        {"kind": "list", "title": "New contact", "rows": ["Name: Aman", "Phone", "Save"], "pick": 2, "note": "You press Save"},
    ],
    "calls": [
        {"kind": "call", "name": "Papa"},
        {"kind": "call", "name": "Amit", "ask": ["Amit Sharma", "Amit Gupta"]},
        {"kind": "call", "name": "98xxxx xx21"},
    ],
    "location": [
        v("You are near the main road, close to the market."),
        {"kind": "route", "dest": "Nearest petrol pump"},
        v("Your location is on the map now. You can share it from there."),
    ],
    "files": [
        {"kind": "list", "title": "Files, last week", "rows": ["bill_nov.pdf", "bill_oct.pdf", "scan_0042.pdf"], "pick": 0},
        {"kind": "list", "title": "Share with", "rows": ["WhatsApp", "Messages", "Gmail"], "pick": 0},
        {"kind": "list", "title": "Download", "rows": ["bill_nov.pdf", "ticket.pdf", "notes.txt", "Photos"], "pick": 0},
    ],
    "images": [
        {"kind": "photo", "caption": "My car"},
        {"kind": "photo", "caption": "ID card"},
        v("The picture is closed."),
    ],
    "app_usage": [
        {"kind": "list", "title": "Most used this week", "rows": ["Instagram", "YouTube", "WhatsApp"], "pick": 0},
        {"kind": "list", "title": "Instagram, today", "rows": ["Today", "Yesterday", "This week"], "pick": 0},
        {"kind": "list", "title": "Top apps", "rows": ["Instagram", "YouTube", "WhatsApp", "Chrome", "Snapchat"], "pick": 0},
    ],
    "notifications": [
        {"kind": "list", "title": "Notifications", "rows": ["Rohan: kab tak aa rahe ho?", "Bank: payment received", "Mummy: call me"], "pick": 0},
        {"kind": "chat", "name": "Rohan", "incoming": "Kab tak aa rahe ho?", "reply": "10 minute mein pahunch raha hu"},
        v("That is playing in your music app right now. I will read out the title."),
    ],
    "navigation": [
        {"kind": "scroll", "rows": ["Headline one", "Headline two", "Headline three", "Headline four", "Headline five", "Headline six", "Headline seven", "Headline eight"]},
        {"kind": "shot", "rows": ["Home", "Messages", "Gallery"]},
        {"kind": "back", "app": "Settings", "page": "Wi-Fi"},
    ],
    "screen": [
        {"kind": "search", "app": "Swiggy", "text": "pizza", "results": ["Margherita pizza", "Farmhouse pizza", "Pizza combo"]},
        {"kind": "scan", "rows": ["Log in", "Search", "Settings"]},
        {"kind": "wait", "text": "Payment successful", "busy": "Processing payment"},
    ],
}

FEATURES = {
    "live-conversation": [
        v("It will be warm in the afternoon with a light breeze. I started speaking before the full reply was ready."),
        v("Sure, Mumbai then. Here is the weather there."),
        v("Alarm set for 6 AM. The screen can stay off."),
    ],
    "phone-control": [
        {"kind": "search", "app": "Swiggy", "text": "pizza", "results": ["Margherita pizza", "Farmhouse pizza", "Pizza combo"]},
        {"kind": "scroll", "rows": ["Section one", "Section two", "Section three", "Section four", "Section five", "Section six", "Section seven", "Section eight"]},
        {"kind": "wait", "text": "Payment successful", "busy": "Processing payment"},
    ],
    "knowledge": [
        v("From your notes: photosynthesis is how plants turn light, water and carbon dioxide into food."),
        v("In the manual, error E4 means the door is not locked properly."),
        v("Your policy document says the notice period is stated in the leave section."),
    ],
    "memory": [
        v("Noted. Your gym time is 6 AM."),
        v("Updated. Your gym time is now 7 PM, and the old one is gone."),
        v("Last week you planned a trip and a team meeting. I looked through that day."),
    ],
    "youtube": [
        {"kind": "ytdl", "title": "Lo-fi beats to study to", "quality": "720p", "file": "Lo-fi beats to study to.mp4", "size": "84 MB"},
        {"kind": "ytdl", "title": "Lo-fi beats to study to", "quality": "Audio only", "file": "Lo-fi beats to study to.m4a", "size": "58 MB"},
        v("I read the captions. In short, the video explains the main idea and then shows an example."),
    ],
    "personalities": [
        v("Switched to Friendly. Happy to help."),
        v("Professional mode is on. Answers will be short and clear."),
        v("Funny mode on. Ask me anything, I will try to keep it light."),
    ],
}

SKILLS = [
    v("Running your morning brief: weather, calendar and reminders."),
    v("I used the WhatsApp skill to send the message."),
    v("Done. I followed the steps of your skill in order."),
]
