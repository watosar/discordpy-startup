apk add build-base libffi-dev libsodium-dev ffmpeg
python3 -m pip install -r requirements.txt
apk del build-base libffi-dev libsodium-dev
python discordbot.py
