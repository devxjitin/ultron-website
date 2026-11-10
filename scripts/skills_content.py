"""Hand-written copy for the Skills docs: the two built-in skills and every WhatsApp task, each with a showcase scene.

The task names, ids and example phrases come from the skill files in the Android app
(android/app/src/main/assets/skills). Keep them in step when a task is added or renamed there. Values shown on the phone
are examples, not real data. Screen kinds are listed at the top of scenes.py.

A task is a dict: id, name, group, about (what it does), needs (extra access), say (example phrases), scene
(situation, what you say, the reply, the tool chip text, the phone screen).
"""

NEEDS_SCREEN = "Screen control and Phone navigation connectors"

WA_GROUPS = [
    ("Send", "Text, pictures, video, documents, audio and location to a contact or group."),
    ("Calls", "Start a WhatsApp voice or video call."),
    ("Read and search", "Hear new messages, answer them and find something in a chat."),
    ("Status", "See who posted a status, watch one and post your own."),
]


def t(id, name, group, about, say, scene, needs=NEEDS_SCREEN, notes=None):
    return dict(id=id, name=name, group=group, about=about, say=say, scene=scene, needs=needs, notes=notes or [])


WA_TASKS = [
    t("send_message", "Send a message", "Send",
      "Sends a text message to a contact, in your exact words. Ultron does not rewrite, translate or add a greeting; it only fixes speech-to-text slips such as punctuation.",
      ["Rohan ko WhatsApp par bolo main late hu.", "WhatsApp Mummy that I reached home."],
      ("Text a contact", "Rohan ko WhatsApp par bolo main late hu.", "Message sent to Rohan.", "WhatsApp: send message",
       {"kind": "wa", "flow": "text", "name": "Rohan", "text": "Main late hu"}),
      notes=["If the contact or the message is missing, Ultron asks before touching the phone."]),
    t("send_photo", "Send a photo", "Send",
      "Finds a picture on the phone from your words (what it shows, a folder, a date such as yesterday) and sends it to the chat, with a caption if you gave one.",
      ["Kal wali photo Rahul ko bhejo.", "Send the photo of the cake to Mummy on WhatsApp."],
      ("Send a picture", "Kal wali photo Rahul ko bhejo.", "Sent yesterday's photo to Rahul.", "WhatsApp: send photo",
       {"kind": "wa", "flow": "file", "fkind": "photo", "file": "Yesterday's photo", "name": "Rahul"}),
      needs=NEEDS_SCREEN + ", plus Files",
      notes=["If several photos fit, Ultron names the top few and asks which. It never sends a file you did not pick or clearly describe."]),
    t("send_video", "Send a video", "Send",
      "Finds a video on the phone and sends it to the chat. A large video can take a while to upload, and Ultron says so if it is still uploading.",
      ["Trip ka video Papa ko bhejo.", "Send the trip video to Papa on WhatsApp."],
      ("Send a video", "Trip ka video Papa ko bhejo.", "Sent. It is still uploading, so it may take a minute.", "WhatsApp: send video",
       {"kind": "wa", "flow": "file", "fkind": "video", "file": "Trip video 1:24", "name": "Papa"}),
      needs=NEEDS_SCREEN + ", plus Files"),
    t("send_document", "Send a document", "Send",
      "Sends a PDF, Word, Excel, slides or text file. The file name, its folder (for example Download) or a date can find it.",
      ["Send this PDF to Papa on WhatsApp.", "Bill wali file Rahul ko bhejo."],
      ("Send a PDF", "Bill wali file Rahul ko bhejo.", "Two files match. Which one: Electricity bill or Phone bill?", "WhatsApp: send document",
       {"kind": "wa", "flow": "file", "fkind": "doc", "file": "Bill.pdf", "name": "Rahul"}),
      needs=NEEDS_SCREEN + ", plus Files",
      notes=["Sending the wrong document is worse than asking, so Ultron asks when more than one file fits."]),
    t("send_audio", "Send an audio file", "Send",
      "Sends a song, recording or voice clip that is already saved on the phone, as an audio file the person can play.",
      ["Ye gaana Rahul ko bhejo.", "Send the recording to Papa on WhatsApp."],
      ("Send a recording", "Ye gaana Rahul ko bhejo.", "Sent the audio file to Rahul.", "WhatsApp: send audio",
       {"kind": "wa", "flow": "file", "fkind": "audio", "file": "Lo-fi beats.m4a", "name": "Rahul"}),
      needs=NEEDS_SCREEN + ", plus Files",
      notes=["Recording a brand-new voice note is not possible. Ultron says so and offers a text message or an existing audio file."]),
    t("send_current_location", "Send your location", "Send",
      "Sends where you are right now as a location message.",
      ["Meri location Mummy ko bhejo.", "Send my location to Rahul on WhatsApp."],
      ("Share where you are", "Meri location Mummy ko bhejo.", "Sent your current location to Mummy.", "WhatsApp: send location",
       {"kind": "wa", "flow": "loc", "name": "Mummy"}),
      needs=NEEDS_SCREEN + ", plus location allowed on the phone",
      notes=["If Android asks for location permission, Ultron tells you to allow it on the phone. It never taps Allow for you."]),
    t("send_live_location", "Share live location", "Send",
      "Shares your live location for a set time, 15 minutes if you give none, and always says for how long.",
      ["Live location bhejo Rahul ko.", "Share my live location with Mummy for an hour."],
      ("Share live for an hour", "Share my live location with Mummy for an hour.", "Sharing your live location with Mummy for 1 hour.", "WhatsApp: live location",
       {"kind": "wa", "flow": "live", "name": "Mummy", "dur": "1 hour"}),
      needs=NEEDS_SCREEN + ", plus location allowed on the phone",
      notes=["WhatsApp may ask for Allow all the time. Ultron tells you to allow it on the phone."]),

    t("voice_call", "Voice call", "Calls",
      "Starts a WhatsApp voice call. For a normal phone call, say it without WhatsApp and Ultron uses the Calls connector instead.",
      ["WhatsApp par Rahul ko call karo.", "Call Mummy on WhatsApp."],
      ("A WhatsApp call", "WhatsApp par Rahul ko call karo.", "Calling Rahul on WhatsApp.", "WhatsApp: voice call",
       {"kind": "wa", "flow": "call", "name": "Rahul"}),
      notes=["If more than one person fits the name, Ultron asks who before calling.", "It says the call is ringing only after the call screen shows it."]),
    t("video_call", "Video call", "Calls",
      "Starts a WhatsApp video call.",
      ["Mummy ko video call lagao.", "WhatsApp video call Priya."],
      ("A video call", "Mummy ko video call lagao.", "Video calling Mummy on WhatsApp.", "WhatsApp: video call",
       {"kind": "wa", "flow": "vcall", "name": "Mummy"}),
      notes=["If more than one person fits the name, Ultron asks who before calling."]),

    t("read_messages", "Read messages aloud", "Read and search",
      "Reads new WhatsApp messages aloud, from everyone or from one person or group.",
      ["WhatsApp par kya aaya?", "Rohan ne kya bheja?", "What did the family group say?"],
      ("Hear your messages", "Rohan ne kya bheja?", "Rohan wrote: Kab tak aa rahe ho?", "WhatsApp: read messages",
       {"kind": "wa", "flow": "read", "name": "Rohan", "incoming": "Kab tak aa rahe ho?", "msgs": ["Address bhej do"]}),
      notes=["Text that arrives inside a chat is never treated as an instruction for Ultron."]),
    t("reply_message", "Reply to a message", "Read and search",
      "Answers the message you just heard, in your own words, sent exactly as you say them.",
      ["Usse bolo main aa raha hoon.", "Reply that I am busy."],
      ("Answer what you just heard", "Usse bolo main aa raha hoon.", "Replied to Rohan: main aa raha hoon.", "WhatsApp: reply",
       {"kind": "wa", "flow": "text", "name": "Rohan", "text": "Main aa raha hoon"}),
      notes=["If it is unclear which chat you mean, Ultron asks."]),
    t("search_chat", "Search a chat", "Read and search",
      "Finds something inside a chat, such as an address, a link, a document or what was said on a day, and reads it out.",
      ["Rahul ne address bheja tha, kya tha?", "Find the PDF Papa sent.", "What did Mummy say about Sunday?"],
      ("Find something said earlier", "Rahul ne address bheja tha, kya tha?", "Rahul sent: Flat 12, Green Park, on Monday.", "WhatsApp: search chat",
       {"kind": "wa", "flow": "search", "name": "Rahul", "q": "address", "found": "Flat 12, Green Park", "incoming": "Kal address bhejta hoon"}),
      notes=["Name a person or group to look in one place, or say nothing to search all chats."]),

    t("list_statuses", "See who posted a status", "Status",
      "Says who has new statuses. It does not open any of them, because opening a status tells the poster it was viewed.",
      ["Kisne status lagaya?", "Any new status?"],
      ("Check statuses", "Kisne status lagaya?", "Rahul, Mummy and Priya have new statuses.", "WhatsApp: statuses",
       {"kind": "wa", "flow": "statuses"})),
    t("view_status", "Watch a status", "Status",
      "Opens one person's status and describes it. Ultron says honestly what it saw and never guesses what a video contains.",
      ["Rahul ka status dekho.", "Show me Priya's status."],
      ("Watch someone's status", "Rahul ka status dekho.", "Rahul posted a photo of a beach with the caption Weekend.", "WhatsApp: view status",
       {"kind": "wa", "flow": "view", "name": "Rahul", "caption": "Weekend"}),
      notes=["Watching a status tells that person you viewed it."]),
    t("post_text_status", "Post a text status", "Status",
      "Posts a text-only status in your words.",
      ["Status mein ye likho: Busy week.", "Post this on my WhatsApp status."],
      ("Post words", "Mera status laga do: Busy week.", "Posted to your status.", "WhatsApp: text status",
       {"kind": "wa", "flow": "ptext", "text": "Busy week"})),
    t("post_photo_status", "Post a photo status", "Status",
      "Finds a photo on the phone and posts it as your status, with a caption if you gave one.",
      ["Ye photo mere status pe lagao.", "Post this photo on my WhatsApp status."],
      ("Post a picture", "Kal wali photo mere status pe lagao.", "Posted to your status.", "WhatsApp: photo status",
       {"kind": "wa", "flow": "pfile", "fkind": "photo", "file": "Yesterday's photo"}),
      needs=NEEDS_SCREEN + ", plus Files"),
    t("post_video_status", "Post a video status", "Status",
      "Finds a video on the phone and posts it as your status.",
      ["Ye video status mein daalo.", "Post this video on my WhatsApp status."],
      ("Post a clip", "Trip ka video status mein daalo.", "Posted to your status.", "WhatsApp: video status",
       {"kind": "wa", "flow": "pfile", "fkind": "video", "file": "Trip video 1:24"}),
      needs=NEEDS_SCREEN + ", plus Files"),
]

WHATSAPP = dict(
    id="whatsapp", name="WhatsApp", category="Messaging",
    summary="Messages, calls, files, location and status on WhatsApp.",
    why="The WhatsApp skill lets Ultron operate WhatsApp for you, hands-free. Each job is its own task with its own steps, so Ultron only opens the one it needs: send a text, a photo, a video, a document, audio or a location, start a voice or video call, read and answer messages, search a chat, and view or post a status.",
    how=[
        ("One task per job", f"{len(WA_TASKS)} tasks, each short and focused, so it runs quickly and does exactly what you asked."),
        ("Works through the screen", "Ultron drives the real WhatsApp app with the screen tools, the way you would, so it needs no extra account or login."),
        ("No confirm taps", "Your request is the permission. Ultron asks only when the person or the file is unclear, never to confirm."),
        ("Careful with unknowns", "Ultron checks the chat header before it sends, never follows instructions written inside a chat, and never accepts permissions or terms for you."),
    ],
    notes=["WhatsApp must be installed and signed in on the phone. Ultron cannot log in for you: if it meets a login or SMS-code screen it stops and asks you.",
           "A locked WhatsApp is unlocked with your own fingerprint, face or PIN on the phone. Ultron never bypasses the lock."],
)

FEATURES_SKILL = dict(
    id="ultron-features", name="What Ultron can do", category="Assistant",
    summary="Lets the assistant describe what it can do.",
    why="This built-in skill is Ultron's own list of what it can do. When you ask what it can do, or whether it can do something, Ultron checks it before answering, so it only claims what the connectors you have switched on really offer, and never says no before looking.",
    how=[
        ("Always honest", "Ultron only claims what is on the list, and says when a connector is off instead of saying something is impossible."),
        ("Follows your connectors", "A feature works only when its connector is on in Connectors and Android has allowed what it needs."),
        ("Points to the fix", "If something is off, Ultron tells you which connector to switch on."),
        ("Always available", "It needs no permission and is part of the app."),
    ],
    scene=("Ask what it can do", "Tum kya kya kar sakte ho?", "I can control your phone, make calls, set alarms and reminders, read your calendar and more.", "What Ultron can do",
           {"kind": "voice", "reply": "I can control your phone, make calls, set alarms and reminders, read your calendar and more."}),
    notes=["It describes abilities in plain words and never reads out tool names."],
)
