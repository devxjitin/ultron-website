"""Hand-written copy for the connector pages: what to say to Ultron for every tool, and a few real-life scenes per
connector. Tool keys are the function names in data/connectors.json. Only claim what the tool really does
(see its hint in the app), so nothing here promises more than the app delivers."""

# connector id -> lead (one line), why (a short paragraph), scenes [(situation, you say, Ultron does)]
CONNECTORS = {
    "device_info": dict(
        lead="Ask your phone how it is doing, out loud.",
        why="You are driving, cooking or in bed and the phone is across the room. Instead of unlocking and digging through settings, ask. Ultron reads the real value from the phone each time, so the answer is never a guess.",
        scenes=[
            ("Before a long trip", "Battery kitna hai, aur kitna storage bacha hai?", "Reads the battery level and charging state, then free storage and RAM, in one answer."),
            ("Slow internet at a cafe", "Kaunsa Wi-Fi laga hai aur signal kaisa hai?", "Tells you the network name, the signal strength and whether you are on Wi-Fi or mobile data."),
            ("Selling your old phone", "What phone model and Android version is this?", "Gives the model, Android version, screen size, language and time zone."),
        ]),
    "device_controls": dict(
        lead="Flashlight, volume, brightness and modes, hands free.",
        why="The small switches you reach for fifty times a day. Say it once and it is done, even when your hands are full or the phone is out of reach.",
        scenes=[
            ("Power cut at night", "Torch on kar do.", "Turns the flashlight on. Say off and it goes off."),
            ("Starting a meeting", "Phone ko silent karo aur Do Not Disturb on.", "Sets the ringer to silent and switches Do Not Disturb on."),
            ("Reading in the sun", "Brightness full kar do.", "Raises the screen brightness to the level you asked for."),
        ]),
    "alarms": dict(
        lead="Set, change and cancel alarms and timers by talking.",
        why="Alarms go into your real clock app, so they ring with sound even if Ultron is closed. You can also ask what is already set, so you never stack two alarms by accident.",
        scenes=[
            ("Early morning", "Kal subah 5:30 ka alarm laga do.", "Creates the alarm in your clock app."),
            ("Cooking", "Ten minute ka timer start karo.", "Starts a countdown that rings with sound."),
            ("Plans change", "Meri 5:30 wali alarm 6 baje kar do.", "Moves that alarm to the new time."),
        ]),
    "reminders": dict(
        lead="Reminders that ring, not just notifications you swipe away.",
        why="Tell Ultron what to remember and when. It rings and vibrates at the time, once or every day or week. It all runs on the phone.",
        scenes=[
            ("Medicine", "Roz raat 9 baje dawai ka reminder lagao.", "Schedules a reminder that repeats every day."),
            ("A call to return", "Ek ghante baad mummy ko call karna yaad dilana.", "Sets a one time reminder after an hour."),
            ("Changed your mind", "Wo kal wala reminder 4 baje kar do.", "Changes the time of a waiting reminder."),
        ]),
    "apps_settings": dict(
        lead="Open any app, any setting, and move text around.",
        why="Skip the home screen hunt. Say the app's name, a settings page or a link. Ultron can also copy text for you to paste anywhere, and show a notification.",
        scenes=[
            ("In a hurry", "Calculator kholo.", "Opens the installed app by name."),
            ("Sharing something", "Ye text WhatsApp par share karna hai.", "Opens the Android share sheet with the text ready."),
            ("App is misbehaving", "Instagram ki app settings kholo.", "Opens that app's info page, where you can check permissions, storage or uninstall."),
        ]),
    "weather": dict(
        lead="Weather now and for the next few days. Free, no sign-in.",
        why="Ask for where you are or any city. It uses a free weather service and needs no account or key.",
        scenes=[
            ("Leaving home", "Aaj baarish hogi kya?", "Tells you the weather now and the forecast for where you are."),
            ("Planning a trip", "Manali mein is weekend mausam kaisa rahega?", "Gives the forecast for the city you name."),
            ("Morning routine", "Aaj kitni garmi hai?", "Reads the current conditions and temperature."),
        ]),
    "duckduckgo": dict(
        lead="Ask anything and get an answer from the live web.",
        why="Gemini on its own can be out of date. With web search on, Ultron looks it up, reads the results and answers in one go. No search account needed.",
        scenes=[
            ("Last night's match", "Kal ke match ka score kya tha?", "Searches the web and tells you the result."),
            ("Before buying", "Best budget earbuds under 2000?", "Looks up recent reviews and summarises the picks."),
            ("Quick fact", "Aaj petrol ka rate kya hai?", "Finds the latest price and answers."),
        ]),
    "web_reader": dict(
        lead="Give it a link, get the point.",
        why="Long articles, terms pages, recipes full of ads. Ultron opens the page, pulls out the main text and reads or summarises it. Nothing is stored.",
        scenes=[
            ("A long article", "Is link ka summary suna do.", "Fetches the page and gives you the key points."),
            ("A recipe", "Is recipe ke ingredients batao.", "Reads the page and lists just the ingredients."),
            ("Fine print", "Is policy page me refund ke baare mein kya likha hai?", "Reads the page and answers from it."),
        ]),
    "youtube": dict(
        lead="Search YouTube, read captions, browse a channel.",
        why="Find the right video without scrolling. Ultron can search, show a video's details, read its captions so you can get the gist without watching, and list what a channel or playlist has.",
        scenes=[
            ("Learning something", "YouTube par React hooks ke best tutorials dhundo.", "Searches YouTube and lists the top videos."),
            ("No time to watch", "Is video ka transcript padh ke summary do.", "Reads the captions and summarises them."),
            ("Catching up", "Is channel ke latest videos dikhao.", "Lists the newest videos from that channel or playlist."),
        ]),
    "youtube_downloads": dict(
        lead="Save a video or just its audio straight to your phone.",
        why="Ask for a video, pick a quality, and the file lands in Downloads/Ultron on your phone. The media never passes through a server. Download only what you have the right to keep.",
        scenes=[
            ("Offline for a flight", "Is video ko 720p mein download karo.", "Lists the qualities, then saves the video to Downloads/Ultron."),
            ("A podcast on a bus", "Is video ka sirf audio save karo.", "Saves audio only, as a small file."),
            ("Not sure what to pick", "Is video ke kaun kaun se quality options hain?", "Lists every format and size, then waits for your choice."),
        ]),
    "calendar": dict(
        lead="Your real calendar, on voice.",
        why="Ask what is coming up, check if a slot is free and add or cancel events. Changes happen in your actual calendar, so every other app sees them too.",
        scenes=[
            ("Morning check", "Aaj mere kya kya events hain?", "Reads today's events from your calendar."),
            ("Finding a slot", "Kal shaam 4 baje free hu kya?", "Checks that slot for conflicts."),
            ("Booking", "Shukravar 6 baje dentist ka event add karo.", "Adds the event to your calendar."),
        ]),
    "contacts": dict(
        lead="Find a number or a birthday without opening Contacts.",
        why="Names can be spelled in many ways on a phone. Ultron matches what you say to your contacts and answers or opens a ready form to save a new one.",
        scenes=[
            ("Need a number", "Rahul ka number kya hai?", "Finds the contact and tells you the number."),
            ("Do not forget", "Priya ka birthday kab hai?", "Reads the birthday saved on that contact."),
            ("Just met someone", "Naya contact save karo, naam Aman.", "Opens a new contact form. You press save."),
        ]),
    "calls": dict(
        lead="Call anyone by name, no touching the phone.",
        why="It places the call straight away, even when the name is spelled differently on your phone. If two contacts fit, it asks which one you mean instead of guessing.",
        scenes=[
            ("Driving", "Papa ko call lagao.", "Places the call right away."),
            ("Two people, same name", "Amit ko call karo.", "Asks which Amit, then calls."),
            ("A number you read out", "Is number par call karo.", "Dials the number you say."),
        ]),
    "location": dict(
        lead="Know where you are and start directions.",
        why="Ask where you are right now, or name a place and Ultron starts navigation in your maps app. Your location is shared only when you ask.",
        scenes=[
            ("Lost in a new city", "Main abhi kahan hu?", "Tells you where the phone is right now."),
            ("Heading out", "Sabse paas ke petrol pump ka rasta batao.", "Starts navigation in your maps app."),
            ("Telling a friend", "Meri location kya hai?", "Reads out your current location so you can share it."),
        ]),
    "files": dict(
        lead="Find any file by saying roughly what it is called.",
        why="You never remember the exact name. Ultron searches by partial names, typos, folders and dates like yesterday or last week, then opens the file in your own apps or sends it to WhatsApp.",
        scenes=[
            ("Need a document", "Pichle hafte wali bill ki PDF dikhao.", "Finds the best match and opens it."),
            ("Sharing a photo", "Kal wali photo WhatsApp par bhejo.", "Finds the photo and opens the share sheet to the app."),
            ("Poking around", "Download folder mein kya hai?", "Lists the files and folders inside it."),
        ]),
    "images": dict(
        lead="Show a picture the moment you ask for it.",
        why="Add pictures to Ultron once, with a name or a note about what is in them. Later, say what you want to see and it appears over the screen. Pictures stay on your phone.",
        scenes=[
            ("Showing a friend", "Meri car ki photo dikhao.", "Shows the picture you saved of it."),
            ("A saved document", "Aadhar card ki photo dikhao.", "Shows the picture you added under that name."),
            ("Done looking", "Photo band karo.", "Hides the picture again."),
        ]),
    "app_usage": dict(
        lead="See where your screen time really goes.",
        why="Ask which apps you use most and for how long. App names and times are shared with Gemini only when you ask.",
        scenes=[
            ("A reality check", "Is hafte maine sabse zyada kaunsi app use ki?", "Lists your most used apps."),
            ("One app in doubt", "Instagram par aaj kitna time laga?", "Tells you how long you used that app."),
            ("Cutting down", "Top 5 apps batao jo mera time kha rahi hain.", "Ranks them so you can decide what to limit."),
        ]),
    "notifications": dict(
        lead="Hear what you missed, reply, and clear the noise.",
        why="Ultron reads your current notifications aloud, replies to chat messages such as WhatsApp, and clears them. Notification text can be private and is shared with Gemini when you ask.",
        scenes=[
            ("Hands busy", "Kya kya notifications aaye hain?", "Reads your pending notifications."),
            ("Quick reply", "Rohan ko bol do main 10 minute mein pahunch raha hu.", "Replies to his chat notification."),
            ("Music in the background", "Ye kaunsa gaana chal raha hai?", "Tells you the song and the app playing it."),
        ]),
    "navigation": dict(
        lead="Back, home, scroll, screenshot. The phone's buttons, by voice.",
        why="This one uses Android accessibility, so it is off until you turn it on. It presses the system buttons and scrolls for you. It does not read what is on your screen.",
        scenes=[
            ("Reading in bed", "Thoda neeche scroll karo.", "Scrolls the page down by the amount you ask."),
            ("Capture this", "Screenshot le lo.", "Takes a screenshot and saves it in your gallery."),
            ("Leaving an app", "Back jao, phir home screen.", "Presses Back, then goes to the home screen."),
        ]),
    "screen": dict(
        lead="Ultron can read the screen and use other apps for you.",
        why="The strongest and most sensitive connector. With accessibility on, Ultron reads what is on screen, taps, types and swipes, so it can do things inside apps that have no shortcuts. Screen text goes to Gemini and can be private, so switch it on only if you understand that.",
        scenes=[
            ("An app with no shortcut", "Swiggy kholo aur pizza search karo.", "Opens the app, taps the search box, types and presses Enter."),
            ("What is on my screen?", "Is screen par kya likha hai?", "Reads the text and buttons on screen and tells you."),
            ("Waiting on a page", "Jab payment successful dikhe tab batana.", "Waits until that text appears on the screen."),
        ]),
}

# tool function name -> what you might say
TOOLS = {
    # device_info
    "get_current_time": "Abhi kitne baje hain? What is today's date?",
    "get_battery_status": "Battery kitni bachi hai? Is it charging?",
    "get_device_info": "Mera phone kaunsa model hai aur Android version kya hai?",
    "get_storage_and_memory": "Kitna storage aur RAM free hai?",
    "get_network_status": "Main Wi-Fi par hu ya mobile data par?",
    "get_wifi_info": "Kaunsa Wi-Fi laga hai aur signal kaisa hai?",
    "get_bluetooth_status": "Bluetooth on hai? Kaun kaun se devices paired hain?",
    "get_step_count": "Aaj maine kitne steps chale?",
    "get_light_level": "Is kamre mein kitni roshni hai?",
    # device_controls
    "set_flashlight": "Torch on karo. Torch band karo.",
    "set_brightness": "Brightness thodi kam kar do. Brightness 80 percent.",
    "get_brightness": "Abhi brightness kitni hai?",
    "set_volume": "Media volume badha do. Ring volume 50 percent.",
    "get_volume": "Abhi saare volume kitne hain?",
    "get_ringer_mode": "Phone silent hai ya vibrate par?",
    "set_ringer_mode": "Phone ko vibrate mode par kar do.",
    "vibrate_device": "Phone vibrate karo, mujhe dhundhna hai.",
    "set_do_not_disturb": "Do Not Disturb on karo.",
    "media_control": "Gaana pause karo. Next song. Pichla gaana.",
    "set_screen_timeout": "Screen 2 minute tak on rakho.",
    "set_auto_rotate": "Auto rotate band kar do.",
    "open_connectivity_panel": "Wi-Fi ka panel kholo. NFC panel dikhao.",
    # alarms
    "set_alarm": "Kal subah 6 baje ka alarm lagao.",
    "list_alarms": "Meri saari alarms batao.",
    "cancel_alarm": "6 baje wali alarm cancel karo.",
    "modify_alarm": "Wo alarm 6:30 par shift kar do.",
    "set_timer": "Paanch minute ka timer lagao.",
    "list_timers": "Kaun kaun se timer chal rahe hain?",
    "cancel_timer": "Timer band kar do.",
    # reminders
    "schedule_reminder": "Shaam 7 baje doodh lene ka reminder do.",
    "list_reminders": "Mere pending reminders kya hain?",
    "cancel_reminder": "Doodh wala reminder hata do.",
    "modify_reminder": "Wo reminder 8 baje kar do.",
    # apps_settings
    "open_app": "YouTube kholo. Open Calculator.",
    "open_camera": "Camera kholo. Video record karna hai.",
    "open_app_settings": "WhatsApp ki settings kholo.",
    "open_settings": "Display settings kholo. Bluetooth settings dikhao.",
    "get_clipboard_text": "Maine kya copy kiya tha?",
    "set_clipboard_text": "Ye address copy kar do.",
    "show_notification": "Mujhe ek notification dikhao: chai ka time.",
    "list_installed_apps": "Mere phone mein kaun kaun si apps hain?",
    "open_url": "Is website ko browser mein kholo.",
    "share_text": "Ye message share karo.",
    # weather
    "get_weather": "Aaj mausam kaisa hai? Kal Delhi mein baarish hogi?",
    # search / web
    "web_search": "Latest iPhone ka price kya hai?",
    "fetch_webpage": "Is link ko padh kar summary do.",
    # youtube
    "youtube_search": "YouTube par lo-fi beats dhundo.",
    "youtube_video_info": "Is video ke baare mein batao: kitni lambi hai, kisne banayi.",
    "youtube_transcript": "Is video ke captions padh kar summary do.",
    "youtube_list_videos": "Is channel ke latest video dikhao.",
    "youtube_download_options": "Is video ki kaun kaun si quality milti hai?",
    "download_youtube_video": "Ise 720p mein download karo. Sirf audio save karo.",
    # calendar
    "get_upcoming_events": "Aaj aur kal ke events kya hain?",
    "check_calendar_conflicts": "Kal 4 baje free hu kya?",
    "create_calendar_event": "Shukravar 6 baje meeting add karo.",
    "cancel_calendar_event": "Kal ki meeting cancel karo.",
    # contacts
    "search_contact": "Rahul ka number kya hai?",
    "get_contact_birthday": "Priya ka birthday kab hai?",
    "create_contact": "Naya contact banao, naam Aman.",
    # calls
    "make_call": "Mummy ko call karo.",
    # location
    "get_current_location": "Main abhi kahan hu?",
    "get_directions": "Railway station ka rasta shuru karo.",
    # files
    "search_files": "Pichle hafte wali bill ki PDF dhundo.",
    "open_file": "Pehli wali file kholo.",
    "list_folder": "Download folder mein kya hai?",
    "share_file": "Ye photo WhatsApp par bhejo.",
    # images
    "show_image": "Meri car ki photo dikhao. Photo band karo.",
    # app usage
    "get_most_used_apps": "Sabse zyada kaunsi apps use karta hu?",
    "get_app_usage_time": "Instagram par aaj kitna time gaya?",
    # notifications
    "read_notifications": "Kya kya notifications aaye hain?",
    "reply_to_notification": "Rohan ko reply karo ki main aa raha hu.",
    "dismiss_notification": "Saari notifications hata do.",
    "get_now_playing": "Ye kaunsa gaana chal raha hai?",
    # navigation
    "press_back": "Peeche jao.",
    "open_recent_apps": "Recent apps dikhao.",
    "switch_to_previous_app": "Pichli app par wapas jao.",
    "open_notification_shade": "Notification panel neeche kheencho.",
    "open_quick_settings": "Quick settings kholo.",
    "scroll_screen": "Thoda neeche scroll karo. Page ke end tak scroll karo.",
    "lock_screen": "Phone lock kar do.",
    "take_screenshot": "Screenshot le lo.",
    "go_to_home_screen": "Home screen par chalo.",
    "open_power_menu": "Power menu kholo.",
    "toggle_split_screen": "Split screen on karo.",
    # screen
    "read_screen": "Screen par kya hai, padh kar batao.",
    "look_at_screen": "Is screen ko dekh kar batao, isme text nahi aa raha.",
    "get_current_app": "Abhi kaunsi app khuli hai?",
    "click_on_text": "Login button dabao.",
    "click_screen_item": "Teen number wala option dabao.",
    "tap_screen_position": "Screen ke beech mein tap karo.",
    "type_text": "Search box mein biryani likho.",
    "press_enter": "Enter dabao.",
    "wait_for_screen_text": "Jab Done dikhe tab batana.",
    "swipe_screen": "Screen ko left se right swipe karo.",
    "long_press_position": "Is jagah par long press karo.",
}

ACCESS_TEXT = {
    "NONE": None,
    "ALL_FILES": "All files access. A settings screen opens when you add it.",
    "USAGE_ACCESS": "Usage access.",
    "NOTIFICATION_ACCESS": "Notification access.",
    "ACCESSIBILITY": "Accessibility access. A settings screen opens when you add it.",
}
