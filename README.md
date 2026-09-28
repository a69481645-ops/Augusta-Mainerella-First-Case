# Augusta Mainerella: First Case

A standalone cyber-noir visual novel built with Python and Pygame CE. The repository already contains the visual asset library under secret/; the runtime discovers those files at launch instead of requiring expression-label naming.

## Run locally

1. Install Python 3.10 or newer.
2. Install dependencies: python -m pip install -r requirements.txt
3. Launch: python main.py

The window renders on a 1920x1080 logical canvas and scales with letterboxing to preserve a crisp 16:9 layout. The name field defaults to Coptcat when left blank.

## Controls

- Enter / Space / Right Arrow / click: advance dialogue
- F5: save to slot 1
- F9: load slot 1
- Escape: return to menu
- Click the player name field: customize the register

Optional ambient audio is picked up from audio/ambient.ogg or secret/ambient.ogg when present. Without that file, the game remains fully playable. Save data is local to the saves/ directory and is ignored by Git.

## Story systems

The script contains exactly twelve sequential chapters and a complete epilogue. Character frames are selected from the loaded image pixels using brightness, alpha coverage, and color-bias signals derived at startup; staging automatically offsets overlapping sprites and keeps Loppunie facing screen-right. Coptcat's dialogue is telepathic and keeps the mouth closed, with the pest scene reserved for the dark-comedy exception.
