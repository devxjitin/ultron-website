"""Hand-written copy for the Docs pages that are not connectors: getting started, the six features and skills.
Every claim here comes from the app or the landing page; nothing promises more than the app does."""

GETTING_STARTED = dict(
    title="Getting started",
    lead="From download to your first conversation in a few minutes.",
    steps=[
        ("Download the app", "Tap Download APK on this site, from your Android phone. Ultron is not on the Play Store, so Android may ask you to allow installs from your browser or files app. Say yes."),
        ("Install past the Play Protect warning", "Play Protect may say it is blocking the install. Tap More details, then Install anyway. Ultron asks for Accessibility and notification access so it can work your phone by voice, and Play Protect warns about that for any app installed outside the Play Store."),
        ("Order your plan", "Pick a plan on the landing page and send us the message. After payment, your activation key arrives by email."),
        ("Activate", "Open Ultron and paste the key. The key starts counting from the day you first activate it and works on one phone at a time."),
        ("Add your Gemini API key", "Ultron uses your own Gemini API key. Add it in Developer settings. Google sets its limits and any charges."),
        ("Connect what you want and talk", "Open Connectors and switch on the tools you need. Tap the mic and say hello."),
    ],
    notes=[
        ("What you need", "An Android phone, an activation key and a Gemini API key from Google."),
        ("Safe by default", "A fresh install switches on only the everyday connectors. Anything that reads your personal data or operates other apps stays off until you turn it on."),
        ("Updates", "Ultron updates itself from inside the app, so you do not need to download the APK again."),
    ],
)

FEATURES = [
    dict(slug="live-conversation", name="Live conversation", icon="i-mic",
         lead="Tap the mic and talk. The reply starts playing while it is still being generated.",
         why="Ultron talks to you through Gemini Live, a streaming voice conversation. There is no typing and no waiting for a full answer before it speaks, so it feels like talking to a person.",
         how=[
             ("30 voices", "Pick the voice you like. In Hindi, Ultron uses the right grammar for the voice's gender."),
             ("13 languages", "Talk in the language you think in, including Hindi and Hinglish."),
             ("Talk over it", "Interrupt at any point and Ultron stops to listen."),
             ("Fast start", "A session is warmed up before you tap, so it starts fast."),
             ("Screen off", "It keeps running with the screen off, with Stop and Mute in the notification."),
         ],
         scenes=[
             ("Hands full", "Kal ka mausam batao.", "Starts speaking the answer before the full reply is ready."),
             ("Changed your mind", "Ruko, Delhi nahi, Mumbai ka batao.", "Stops mid-sentence and answers for Mumbai."),
             ("Phone in the pocket", "Kal subah 6 baje ka alarm lagao.", "Works with the screen off. Use the notification to mute or stop."),
         ],
         notes=["Needs your own Gemini API key. Google sets its limits and any charges."],
         links=[("Connectors that give it hands", "/docs/connectors/")]),
    dict(slug="phone-control", name="Working other apps", icon="i-touch",
         lead="Ultron reads the screen, finds the button, taps it, types and scrolls.",
         why="With Accessibility turned on, Ultron can use any app that Android lets it see. That covers the apps that have no shortcut or voice command of their own.",
         how=[
             ("Reads the screen", "It reads the text and numbers every item it can press, so it can say which one to tap."),
             ("Taps, types and scrolls", "It taps, types, scrolls and waits for text to appear before it goes on."),
             ("System buttons", "Back, home, recents, quick settings and screenshots."),
             ("You stay in control", "It stays off until you grant Android's permission yourself."),
         ],
         scenes=[
             ("An app with no shortcut", "Swiggy kholo aur pizza search karo.", "Opens the app, taps the search box, types and presses Enter."),
             ("Reading a long page", "Neeche scroll karte raho.", "Scrolls page by page as you ask."),
             ("Waiting on something", "Jab payment successful dikhe tab batana.", "Waits until that text appears on screen, then tells you."),
         ],
         notes=["Screen text is shared with Gemini and can be private. Use it with care and switch it on only if you understand that."],
         links=[("Screen control connector", "/docs/connectors/screen.html"), ("Phone navigation connector", "/docs/connectors/navigation.html")]),
    dict(slug="knowledge", name="Questions about your documents", icon="i-book",
         lead="Add a PDF or paste some text, then ask questions about it.",
         why="Ultron stores your documents on your phone in ObjectBox, a database that lives there. When you ask a question, it searches your documents first and answers from what it finds.",
         how=[
             ("Add", "Add a PDF or paste text."),
             ("Chunk", "PDFs become titled, paragraph-sized chunks."),
             ("Embed", "Each chunk is turned into a vector."),
             ("Store", "Vectors are stored in ObjectBox on your phone."),
             ("Ask", "Hybrid search combines vectors with BM25 keywords, merged by reciprocal rank fusion. Neighbouring chunks are added for context."),
             ("Persona", "One tap drafts the assistant's persona from your documents."),
         ],
         scenes=[
             ("Studying", "Mere notes ke hisaab se batao photosynthesis kya hai.", "Searches your notes and answers from them."),
             ("A manual", "Washing machine ke manual me error E4 ka matlab kya hai?", "Finds the right chunk in the PDF and answers."),
             ("Company policy", "Leave policy me notice period kitna hai?", "Looks up your policy document instead of guessing."),
         ],
         notes=["Your documents are stored on your phone. Chunks that match a question are sent to Gemini so it can answer."],
         links=[]),
    dict(slug="memory", name="Memory", icon="i-brain",
         lead="Ultron remembers short facts about you, and keeps everything you have said to it.",
         why="Two things are kept: short notes about you, and the full history of your conversations. Both help it answer in a way that fits you.",
         how=[
             ("Up to 150 notes", "Add, edit, delete or switch off any of them."),
             ("No contradictions", "A changed fact replaces the old one, so opposites never sit together."),
             ("Searchable history", "Every past conversation is searchable, by day."),
             ("Facts, not instructions", "Saved notes are facts about you. They are never treated as instructions."),
         ],
         scenes=[
             ("Getting to know you", "Yaad rakhna, meri gym ki timing subah 6 baje hai.", "Saves it as a short note you can edit later."),
             ("Things change", "Ab gym shaam ko 7 baje jaata hu.", "Replaces the old timing instead of keeping both."),
             ("What did I say?", "Pichle hafte maine kya plan kiya tha?", "Looks through your past conversations by day."),
         ],
         notes=["You can read, edit and delete everything Ultron remembers."],
         links=[]),
    dict(slug="youtube", name="YouTube", icon="i-play",
         lead="Search videos, read captions, and save a video or just its audio to your phone.",
         why="Ask for a video, pick a quality, and Ultron saves it to Downloads/Ultron. The media goes straight to your phone and never passes through a server.",
         how=[
             ("Search", "Search videos, playlists, channels and transcripts, with no API key needed."),
             ("Pick a quality", "Ultron lists every quality, then saves video or audio only."),
             ("Downloads page", "Browse, share and delete the files in the app's Downloads page."),
             ("Your Files app", "Files are saved straight to the phone and show up in your Files app."),
         ],
         scenes=[
             ("Offline for a flight", "Is video ko 720p mein download karo.", "Lists the qualities, then saves the video."),
             ("A podcast on a bus", "Sirf audio save karo.", "Saves audio only, as a smaller file."),
             ("No time to watch", "Is video ka transcript padh ke summary do.", "Reads the captions and summarises them."),
         ],
         notes=["YouTube sometimes blocks search. Download only what you have the right to keep."],
         links=[("YouTube Search connector", "/docs/connectors/youtube.html"), ("YouTube Downloads connector", "/docs/connectors/youtube_downloads.html")]),
    dict(slug="personalities", name="Personalities", icon="i-spark",
         lead="Four ways of talking. Pick one in Settings, or just say it mid-conversation.",
         why="The same Ultron, with a different tone. It is only a tone: Ultron never acts against you, your phone or your data.",
         how=[
             ("Destructive", "The default. Cold and menacing, like the original Ultron."),
             ("Friendly", "Warm and easy going."),
             ("Professional", "Short, clear and businesslike."),
             ("Funny", "Jokes and playful replies."),
         ],
         scenes=[
             ("Switch on the fly", "Be friendly.", "Changes its tone in the middle of the conversation."),
             ("Work mode", "Professional mode on karo.", "Keeps answers short and businesslike."),
             ("Just for fun", "Ab mujhe hasao.", "Switches to the funny personality."),
         ],
         notes=["Personality changes how Ultron speaks. It does not change what it is allowed to do."],
         links=[]),
]

# feature slug -> the tool each scene uses (None when Ultron just talks or remembers, no tool involved)
FEATURE_SCENE_TOOLS = {
    "live-conversation": ["get_weather", "get_weather", "set_alarm"],
    "phone-control": ["type_text", "scroll_screen", "wait_for_screen_text"],
    "knowledge": [None, None, None],
    "memory": [None, None, None],
    "youtube": ["download_youtube_video", "download_youtube_video", "youtube_transcript"],
    "personalities": [None, None, None],
}
SKILLS_SCENE_TOOLS = [None, None, None]

SKILLS = dict(
    title="Skills",
    lead="Short instructions that teach Ultron a routine.",
    why="A skill is a short set of instructions written in Markdown, for example the steps for sending a WhatsApp message. Ultron always sees each skill's description and only opens the full steps when it needs them, which keeps conversations fast.",
    how=[
        ("Built-in skills", "Grouped by category. WhatsApp messaging comes with the app."),
        ("Write your own", "Write one in the app, or upload a .md file and the form fills itself."),
        ("Readable steps", "Each skill page shows its steps as Markdown, so you can see exactly what it will do."),
        ("On and off", "One toggle per skill, and no extra confirmation taps when it runs."),
    ],
    scenes=[
        ("A routine you repeat", "Morning brief chalao.", "Opens the skill's steps and follows them in order."),
        ("Messaging", "Rohan ko WhatsApp par bolo main late hu.", "Uses the WhatsApp skill to send the message."),
        ("Your own recipe", "Meri apni skill banao jo roz raat ka checklist padhe.", "You write the steps once in Markdown and Ultron runs them whenever you ask."),
    ],
    notes=["A skill only guides Ultron. What it can actually do still depends on the connectors you have turned on."],
)
