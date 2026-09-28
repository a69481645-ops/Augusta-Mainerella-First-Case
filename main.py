from __future__ import annotations

import json
import math
import random
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import pygame


LOGICAL_SIZE = (1920, 1080)
FPS = 60
ROOT = Path(__file__).resolve().parent
SAVE_DIR = ROOT / "saves"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

CYAN = (53, 238, 255)
MAGENTA = (255, 63, 179)
LIME = (176, 255, 87)
INK = (8, 12, 20)
CHARCOAL = (16, 22, 32)
MUTED = (136, 156, 174)
WHITE = (238, 247, 255)

CHAPTERS = [
    "THE MISSING FRAME",
    "FIREWALL / FOG",
    "SPYJEWEL",
    "THE JAZZ DETOUR",
    "VELVET ONYX",
    "WHITE VECTOR RAIN",
    "THE CONCRETE VAULT",
    "UNDER THE IRON DOOR",
    "THE SMIRK",
    "TELEPATHIC AUTHORITY",
    "THE WIPE",
    "PERSONAL AGENCY",
    "EPILOGUE",
]

BACKGROUND_NAMES = [
    "studio", "tracking", "firewall", "club", "alley", "mansion", "vault"
]

CHARACTER_ALIASES = {
    "augusta": "Augusta Mainerella",
    "coptcat (the player)": "Coptcat",
    "coptcat": "Coptcat",
    "gideon": "Cideon Minx",
    "loppunie": "Loppunie",
    "madonna": "Madonna",
    "officer shepherd": "Officer Shepherd",
    "rouge": "Agent Rouge",
    "sabrina": "Sabrina Shadowcoat",
    "sonic": "Sonic",
    "cleo": "Cleo Habessha",
    "baron vance": "Baron Vance",
    "silas flint": "Silas Flint",
    "viktor": "Viktor",
    "jax": "Jax",
}

ANCHORS = {
    "left_outer": 180,
    "left": 430,
    "left_inner": 690,
    "center": 960,
    "right_inner": 1230,
    "right": 1490,
    "right_outer": 1760,
}


@dataclass
class Frame:
    path: Path
    surface: pygame.Surface
    brightness: float
    alpha_coverage: float
    cyan_bias: float
    magenta_bias: float


@dataclass
class SceneLine:
    speaker: str
    text: str
    cast: Tuple[str, ...]
    bg: int
    effect: str = ""


class AssetManager:
    """Discovers visual assets and selects frames from their pixels, not labels."""

    def __init__(self, root: Path):
        self.root = root
        self.frames: Dict[str, List[Frame]] = {}
        self.backgrounds: List[pygame.Surface] = []
        self.logo: Optional[pygame.Surface] = None
        self.scan()

    def _canonical_character(self, folder: str) -> Optional[str]:
        key = folder.strip().lower()
        return CHARACTER_ALIASES.get(key)

    def _visual_signature(self, surface: pygame.Surface) -> Tuple[float, float, float, float]:
        width, height = surface.get_size()
        step_x = max(1, width // 24)
        step_y = max(1, height // 24)
        total = bright = coverage = cyan = magenta = 0.0
        for y in range(0, height, step_y):
            for x in range(0, width, step_x):
                r, g, b, a = surface.get_at((x, y))
                if a < 16:
                    continue
                total += 1
                coverage += min(1.0, a / 255.0)
                value = (r + g + b) / (3 * 255.0)
                bright += value
                cyan += max(0.0, (g + b) / 510.0 - r / 255.0)
                magenta += max(0.0, (r + b) / 510.0 - g / 255.0)
        if total == 0:
            return 0.5, 0.0, 0.0, 0.0
        return bright / total, coverage / total, cyan / total, magenta / total

    def scan(self) -> None:
        all_images: List[Path] = []
        for folder in (self.root / "images", self.root / "secret", self.root):
            if folder.exists():
                all_images.extend(p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS)
        seen = set()
        for path in all_images:
            if path in seen:
                continue
            seen.add(path)
            try:
                surface = pygame.image.load(str(path)).convert_alpha()
            except pygame.error:
                continue
            if path.name.lower() == "logo.png":
                self.logo = surface
            parts = list(path.parts)
            try:
                sprite_index = parts.index("Sprites")
            except ValueError:
                sprite_index = -1
            if sprite_index >= 0:
                tail = parts[sprite_index + 1 : -1]
                if tail:
                    character = self._canonical_character(tail[-1])
                    if character:
                        bright, cover, cyan, magenta = self._visual_signature(surface)
                        self.frames.setdefault(character, []).append(
                            Frame(path, surface, bright, cover, cyan, magenta)
                        )
            if "Backgrounds" in parts:
                self.backgrounds.append(surface)
        self.backgrounds.sort(key=lambda surface: surface.get_width() * surface.get_height())
        for values in self.frames.values():
            values.sort(key=lambda frame: str(frame.path).lower())

    def choose_frame(self, character: str, line: str) -> Optional[Frame]:
        options = self.frames.get(character, [])
        if not options:
            return None
        text = line.lower()
        urgency = sum(word in text for word in ("now", "run", "fire", "kick", "help", "break", "stop"))
        warmth = sum(word in text for word in ("love", "partner", "safe", "thank", "grandma", "smile"))
        threat = sum(word in text for word in ("blood", "slave", "weapon", "trap", "smirk", "vault", "wipe"))
        target_brightness = 0.45 + 0.08 * urgency + 0.05 * warmth - 0.04 * threat
        target_cyan = 0.18 + 0.05 * urgency
        target_magenta = 0.18 + 0.05 * warmth + 0.04 * threat
        return min(
            options,
            key=lambda frame: abs(frame.brightness - target_brightness)
            + abs(frame.cyan_bias - target_cyan)
            + abs(frame.magenta_bias - target_magenta)
            + abs(frame.alpha_coverage - 0.55) * 0.2,
        )

    def background(self, index: int) -> Optional[pygame.Surface]:
        if not self.backgrounds:
            return None
        return self.backgrounds[index % len(self.backgrounds)]


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Augusta Mainerella: First Case")
        self.window = pygame.display.set_mode(LOGICAL_SIZE, pygame.RESIZABLE)
        self.canvas = pygame.Surface(LOGICAL_SIZE, pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("dejavusans", 28)
        self.small_font = pygame.font.SysFont("dejavusans", 21)
        self.title_font = pygame.font.SysFont("dejavusans", 70, bold=True)
        self.chapter_font = pygame.font.SysFont("dejavusans", 24, bold=True)
        self.assets = AssetManager(ROOT)
        self.rng = random.Random(2712)
        self.rain = [(self.rng.randrange(0, 1920), self.rng.randrange(0, 1080), self.rng.randrange(22, 52)) for _ in range(150)]
        self.state = "menu"
        self.name_input = "Coptcat"
        self.player_name = "Coptcat"
        self.name_active = False
        self.chapter = 0
        self.line_index = 0
        self.reveal_started = time.monotonic()
        self.save_notice = ""
        self.notice_until = 0.0
        self.running = True
        self.audio_ready = False
        self._bind_ambient_audio()
        self.script = self._build_script()

    def _bind_ambient_audio(self) -> None:
        """Optional audio hook: the game remains playable when no audio files are present."""
        try:
            pygame.mixer.init()
            for candidate in (ROOT / "audio" / "ambient.ogg", ROOT / "secret" / "ambient.ogg"):
                if candidate.exists():
                    pygame.mixer.music.load(str(candidate))
                    pygame.mixer.music.set_volume(0.28)
                    pygame.mixer.music.play(-1)
                    self.audio_ready = True
                    break
        except (pygame.error, FileNotFoundError):
            self.audio_ready = False

    def _build_script(self) -> List[List[SceneLine]]:
        def L(speaker: str, text: str, cast: Iterable[str], bg: int, effect: str = "") -> SceneLine:
            return SceneLine(speaker, text, tuple(cast), bg, effect)

        return [
            [
                L("Augusta Mainerella", "Los Angeles was supposed to be a photography vacation. One white backdrop, one client, zero disasters.", ("Augusta Mainerella",), 0),
                L("Augusta Mainerella", "Loppunie should have answered three calls ago. I am texting again. I am not panicking. I am a professional.", ("Augusta Mainerella",), 0),
                L("Coptcat", "The message vanished into the dark. I saw it. I remember it. I have been waiting beside your lens.", ("Augusta Mainerella", "Coptcat"), 0),
                L("Augusta Mainerella", "You are not a god. You are my ultimate great x6 grandmother. Grandma. And I am an atheist, so please skip the worship portion.", ("Augusta Mainerella", "Coptcat"), 0),
                L("Cideon Minx", "Bring the phone to my tracking desk. If Loppunie left a signal, I can find the frame it disappeared from.", ("Augusta Mainerella", "Cideon Minx"), 1),
            ],
            [
                L("Cideon Minx", "There. The firewall is wearing a nightclub mask over a shipping manifest. That is not a metaphor I enjoy.", ("Cideon Minx", "Augusta Mainerella"), 1),
                L("Augusta Mainerella", "Captive women catalogued like merchandise. I am calling the LAPD precinct. Someone official has to see this.", ("Augusta Mainerella", "Cideon Minx"), 2),
                L("Officer Shepherd", "This is not a police matter without a local complainant and a clean chain of evidence. Do not call back.", ("Officer Shepherd", "Augusta Mainerella"), 2),
                L("Augusta Mainerella", "He hung up. I crossed an ocean for a holiday and found a crime scene that refuses to be convenient.", ("Augusta Mainerella",), 2),
            ],
            [
                L("Augusta Mainerella", "The codeword is Spyjewel. If anyone is listening, I am done waiting for permission.", ("Augusta Mainerella",), 1),
                L("Agent Rouge", "PTO is a flexible concept when a photographer says the word Spyjewel. I brought wings, lock picks, and bad timing.", ("Agent Rouge", "Augusta Mainerella"), 1),
                L("Augusta Mainerella", "You dropped through my studio window.", ("Augusta Mainerella", "Agent Rouge"), 0),
                L("Agent Rouge", "Tactical support should enter from the least expected angle. Also, the window was open.", ("Agent Rouge", "Augusta Mainerella"), 0),
            ],
            [
                L("Sonic", "You found a syndicate. We found a route in. Madonna traced the money to a cabaret called The Velvet Onyx.", ("Sonic", "Augusta Mainerella", "Agent Rouge"), 3),
                L("Madonna", "I sing jazz, not pop, and I know every room where rich people mistake a velvet curtain for a conscience.", ("Madonna", "Sonic", "Augusta Mainerella"), 3),
                L("Sonic", "We go together. Girlfriend, partner, and the fastest exit in the building.", ("Sonic", "Madonna", "Augusta Mainerella"), 3),
                L("Madonna", "Boyfriend, partner, and the person I will personally drag out if he improvises without me.", ("Madonna", "Sonic", "Augusta Mainerella"), 3),
            ],
            [
                L("Cleo Habessha", "The Velvet Onyx sells music and spectacle. Forced human slavery is where my hospitality ends.", ("Cleo Habessha", "Augusta Mainerella", "Sonic"), 3),
                L("Augusta Mainerella", "Then help us dismantle the room behind the room.", ("Augusta Mainerella", "Cleo Habessha", "Sonic"), 3),
                L("Cleo Habessha", "Vance hides behind a suburban mansion and a keycard no honest guest should possess. Take it.", ("Cleo Habessha", "Augusta Mainerella", "Sonic"), 3),
                L("Sonic", "A clean line is still a line. Thank you for drawing it.", ("Sonic", "Cleo Habessha"), 3),
            ],
            [
                L("Augusta Mainerella", "The alley is freezing. White vector rain cuts the floodlights into hard little arrows.", ("Augusta Mainerella", "Sonic"), 4, "rain"),
                L("Sabrina Shadowcoat", "You want me to risk everything so you can feel brave. I want to live past tonight.", ("Sabrina Shadowcoat", "Augusta Mainerella", "Sonic"), 4, "rain"),
                L("Augusta Mainerella", "I am a tourist from Augusta, Maine. I came here for pictures. I am staying because somebody has to protect the people this city keeps framing out.", ("Augusta Mainerella", "Sabrina Shadowcoat", "Sonic"), 4, "rain"),
                L("Sabrina Shadowcoat", "Then watch the lights. When they go, move.", ("Sabrina Shadowcoat", "Augusta Mainerella"), 4, "rain"),
                L("Augusta Mainerella", "Sabrina throws the heavy breaker. The courtyard disappears.", ("Augusta Mainerella", "Sabrina Shadowcoat", "Sonic"), 4, "blackout"),
            ],
            [
                L("Silas Flint", "Intruders in the concrete vault. Viktor, make the photographer regret the shortcut.", ("Silas Flint", "Viktor", "Augusta Mainerella", "Sonic"), 6),
                L("Sonic", "Eyes on me. I am faster than your aim and considerably harder to intimidate.", ("Sonic", "Silas Flint", "Viktor"), 6),
                L("Augusta Mainerella", "My combat boots are not a prop. They are how a pack-protector stands her ground.", ("Augusta Mainerella", "Silas Flint", "Viktor"), 6),
                L("Augusta Mainerella", "One kick. One server rack. One very expensive lesson in underestimating a tourist.", ("Augusta Mainerella", "Silas Flint", "Cideon Minx"), 6, "impact"),
                L("Cideon Minx", "Encryption copied. The vault is no longer private.", ("Cideon Minx", "Augusta Mainerella"), 6),
            ],
            [
                L("Augusta Mainerella", "The keycard opens a heavy iron door beneath the mansion. The air tastes like dust and old fear.", ("Augusta Mainerella", "Sonic"), 5),
                L("Augusta Mainerella", "Loppunie. Tape. Chair. Camera box. My hands are shaking, but the door is open.", ("Augusta Mainerella", "Loppunie", "Sonic"), 5),
                L("Baron Vance", "You made it all the way down. I admire the commitment to a story with a very obvious ending.", ("Baron Vance", "Jax", "Augusta Mainerella", "Sonic"), 5),
                L("Jax", "Boss says nobody leaves with the footage.", ("Jax", "Baron Vance", "Sonic"), 5),
            ],
            [
                L("Baron Vance", "Paying users want possession. I provide an unregistered deep-web service. The market decides what people are worth.", ("Baron Vance", "Jax", "Augusta Mainerella"), 5),
                L("Augusta Mainerella", "No market decides a person. Your smirk is not a shield; it is evidence of what you chose.", ("Augusta Mainerella", "Baron Vance"), 5),
                L("Baron Vance", "Evidence is only frightening when someone has the power to make it matter.", ("Baron Vance", "Augusta Mainerella", "Sonic"), 5),
                L("Sonic", "Then let us change the power balance.", ("Sonic", "Baron Vance"), 5),
            ],
            [
                L("Coptcat", "Enough. I have watched the living mistake silence for consent. Your thoughts are loud, Baron Vance.", ("Coptcat", "Baron Vance", "Jax"), 5),
                L("Coptcat", "Freeze. Not because I am divine. Because the truth has finally entered the room.", ("Coptcat", "Baron Vance", "Jax", "Augusta Mainerella"), 5),
                L("Sonic", "Loppunie, I have the cuffs. Madonna is outside with Rouge. You are not alone.", ("Sonic", "Loppunie", "Augusta Mainerella"), 5),
                L("Augusta Mainerella", "I roundhouse the box camera. Cideon, wipe every copy that should never have existed.", ("Augusta Mainerella", "Cideon Minx", "Loppunie"), 5, "impact"),
                L("Cideon Minx", "Full server wipe running. Their archive is becoming unusable noise.", ("Cideon Minx", "Augusta Mainerella"), 6),
            ],
            [
                L("Agent Rouge", "Task force is in the mansion. Doors are open, victims are moving toward advocates, and Vance is out of rooms to hide in.", ("Agent Rouge", "Augusta Mainerella", "Sonic"), 5),
                L("Madonna", "Cleo is taking over the legal nightlife. The Velvet Onyx will be a venue, not a pipeline.", ("Madonna", "Cleo Habessha", "Sonic"), 3),
                L("Cleo Habessha", "The stage stays bright. The back rooms stay accountable.", ("Cleo Habessha", "Madonna"), 3),
                L("Loppunie", "My name is mine again. That is the whole miracle.", ("Loppunie", "Augusta Mainerella"), 0),
            ],
            [
                L("Augusta Mainerella", "At the white backdrop, Loppunie stands smiling on her own terms. The photograph is hers to keep.", ("Augusta Mainerella", "Loppunie"), 0),
                L("Sonic", "You came here for a vacation and built a rescue operation instead.", ("Sonic", "Augusta Mainerella", "Madonna"), 0),
                L("Madonna", "That is what a good partner does: notices the wrong note and refuses to sing over it.", ("Madonna", "Sonic", "Augusta Mainerella"), 0),
                L("Coptcat", "Personal agency is sacred because it belongs to the person. Keep your name. Keep your body. Keep your yes and your no.", ("Coptcat", "Augusta Mainerella", "Loppunie"), 0),
            ],
            [
                L("Coptcat", "Case closed. The frame is yours now, player.", ("Coptcat",), 0),
            ],
        ]

    @property
    def line(self) -> SceneLine:
        return self.script[self.chapter][self.line_index]

    def reset_case(self) -> None:
        self.player_name = self.name_input.strip() or "Coptcat"
        self.chapter = 0
        self.line_index = 0
        self.state = "game"
        self.reveal_started = time.monotonic()
        self.save_notice = ""

    def save_case(self, slot: int = 1) -> None:
        SAVE_DIR.mkdir(exist_ok=True)
        payload = {
            "player_name": self.player_name,
            "chapter": self.chapter,
            "line_index": self.line_index,
            "saved_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        (SAVE_DIR / f"slot{slot}.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
        self.save_notice = f"CASE SAVED TO SLOT {slot}"
        self.notice_until = time.monotonic() + 2.4

    def load_case(self, slot: int = 1) -> None:
        path = SAVE_DIR / f"slot{slot}.json"
        if not path.exists():
            self.save_notice = "NO CASE FILE IN SLOT 1"
            self.notice_until = time.monotonic() + 2.4
            return
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.player_name = str(payload.get("player_name") or "Coptcat")
            self.name_input = self.player_name
            self.chapter = max(0, min(12, int(payload.get("chapter", 0))))
            self.line_index = max(0, min(len(self.script[self.chapter]) - 1, int(payload.get("line_index", 0))))
            self.state = "game"
            self.reveal_started = time.monotonic()
        except (ValueError, OSError, json.JSONDecodeError):
            self.save_notice = "CASE FILE CORRUPTED"
            self.notice_until = time.monotonic() + 2.4

    def advance(self) -> None:
        if self.visible_characters() < len(self.line.text):
            self.reveal_started = time.monotonic() - 20
            return
        if self.line_index + 1 < len(self.script[self.chapter]):
            self.line_index += 1
        elif self.chapter < 12:
            self.chapter += 1
            self.line_index = 0
        else:
            self.state = "menu"
        self.reveal_started = time.monotonic()

    def visible_characters(self) -> int:
        return min(len(self.line.text), int((time.monotonic() - self.reveal_started) * 68))

    def wrap(self, text: str, font: pygame.font.Font, width: int) -> List[str]:
        words = text.split()
        lines: List[str] = []
        current = ""
        for word in words:
            candidate = word if not current else current + " " + word
            if font.size(candidate)[0] <= width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def draw_text(self, surface: pygame.Surface, text: str, pos: Tuple[int, int], font: pygame.font.Font, color: Tuple[int, int, int], max_width: Optional[int] = None, line_gap: int = 8) -> int:
        lines = self.wrap(text, font, max_width) if max_width else [text]
        x, y = pos
        for line in lines:
            surface.blit(font.render(line, True, color), (x, y))
            y += font.get_height() + line_gap
        return y

    def fit_background(self, source: pygame.Surface) -> pygame.Surface:
        sw, sh = source.get_size()
        scale = max(LOGICAL_SIZE[0] / sw, LOGICAL_SIZE[1] / sh)
        resized = pygame.transform.smoothscale(source, (int(sw * scale), int(sh * scale)))
        result = pygame.Surface(LOGICAL_SIZE)
        result.blit(resized, ((LOGICAL_SIZE[0] - resized.get_width()) // 2, (LOGICAL_SIZE[1] - resized.get_height()) // 2))
        return result

    def draw_background(self, index: int, blackout: bool = False) -> None:
        background = self.assets.background(index)
        if background:
            self.canvas.blit(self.fit_background(background), (0, 0))
        else:
            for y in range(LOGICAL_SIZE[1]):
                t = y / LOGICAL_SIZE[1]
                pygame.draw.line(self.canvas, (8 + int(15 * t), 13 + int(13 * t), 25 + int(25 * t)), (0, y), (1920, y))
        shade = pygame.Surface(LOGICAL_SIZE, pygame.SRCALPHA)
        shade.fill((3, 7, 15, 92 if not blackout else 205))
        self.canvas.blit(shade, (0, 0))
        for y in range(0, LOGICAL_SIZE[1], 6):
            pygame.draw.line(self.canvas, (30, 225, 244, 14), (0, y), (1920, y), 1)
        vignette = pygame.Surface(LOGICAL_SIZE, pygame.SRCALPHA)
        for edge in range(140, 0, -8):
            alpha = int(1.5 * (140 - edge))
            pygame.draw.rect(vignette, (0, 0, 10, alpha), (140 - edge, 90 - edge, 1920 - 280 + edge * 2, 1080 - 180 + edge * 2), 8)
        self.canvas.blit(vignette, (0, 0))

    def staged_positions(self, cast: Tuple[str, ...]) -> List[Tuple[str, int]]:
        positions: List[Tuple[str, int]] = []
        used: List[int] = []
        preference = ["left_outer", "right_outer", "left", "right", "left_inner", "right_inner", "center"]
        for index, character in enumerate(cast):
            anchor_name = preference[index % len(preference)]
            x = ANCHORS[anchor_name]
            while any(abs(x - old) < 230 for old in used):
                x += 190
                if x > 1780:
                    x = 160 + (index * 130) % 1580
            used.append(x)
            positions.append((character, x))
        return positions

    def draw_characters(self, cast: Tuple[str, ...], text: str) -> None:
        for character, anchor_x in self.staged_positions(cast):
            frame = self.assets.choose_frame(character, text)
            if not frame:
                self.draw_fallback_character(character, anchor_x)
                continue
            sprite = frame.surface.copy()
            target_height = 820 if len(cast) <= 2 else 650
            scale = min(1.0, target_height / max(1, sprite.get_height()))
            sprite = pygame.transform.smoothscale(sprite, (max(1, int(sprite.get_width() * scale)), max(1, int(sprite.get_height() * scale))))
            if character == "Loppunie":
                sprite = pygame.transform.flip(sprite, True, False)
            sprite.set_alpha(232 if character == self.line.speaker else 168)
            rect = sprite.get_rect(midbottom=(anchor_x, 835))
            self.canvas.blit(sprite, rect)

    def draw_fallback_character(self, character: str, anchor_x: int) -> None:
        color = MAGENTA if character == self.line.speaker else CYAN
        rect = pygame.Rect(anchor_x - 115, 250, 230, 585)
        pygame.draw.rect(self.canvas, (12, 22, 35), rect, border_radius=22)
        pygame.draw.rect(self.canvas, color, rect, width=3, border_radius=22)
        pygame.draw.circle(self.canvas, color, (anchor_x, 355), 70, 3)
        self.draw_text(self.canvas, character.upper(), (rect.x + 18, 745), self.small_font, WHITE, 190, 3)

    def draw_rain(self, blackout: bool = False) -> None:
        alpha = 130 if not blackout else 65
        overlay = pygame.Surface(LOGICAL_SIZE, pygame.SRCALPHA)
        for x, y, length in self.rain:
            pygame.draw.line(overlay, (255, 255, 255, alpha), (x, y), (x - 36, y + length), 3)
        self.canvas.blit(overlay, (0, 0))

    def draw_dialogue(self) -> None:
        panel = pygame.Rect(120, 820, 1680, 206)
        pygame.draw.rect(self.canvas, (7, 12, 22, 235), panel, border_radius=10)
        pygame.draw.rect(self.canvas, CYAN, panel, width=2, border_radius=10)
        pygame.draw.line(self.canvas, MAGENTA, (panel.x, panel.y), (panel.x + 390, panel.y), 6)
        name_box = pygame.Rect(panel.x + 34, panel.y - 32, max(260, self.font.size(self.line.speaker.upper())[0] + 58), 52)
        pygame.draw.rect(self.canvas, (11, 24, 35), name_box, border_radius=6)
        pygame.draw.rect(self.canvas, MAGENTA, name_box, width=2, border_radius=6)
        self.canvas.blit(self.chapter_font.render(self.line.speaker.upper(), True, WHITE), (name_box.x + 28, name_box.y + 12))
        visible = self.line.text[: self.visible_characters()]
        self.draw_text(self.canvas, visible, (panel.x + 40, panel.y + 34), self.font, WHITE, panel.width - 80, 12)
        if self.visible_characters() >= len(self.line.text):
            hint = "CLICK / SPACE  ›"
            self.canvas.blit(self.small_font.render(hint, True, LIME), (panel.right - 230, panel.bottom - 42))
        if self.line.speaker == "Coptcat":
            tag = "TELEPATHIC / MOUTH CLOSED"
            if "pest" in self.line.text.lower() and self.visible_characters() >= len(self.line.text):
                tag = "TELEPATHIC / IMMORTAL TREAT"
                pygame.draw.circle(self.canvas, MAGENTA, (1660, 100), 22, 3)
            self.canvas.blit(self.small_font.render(tag, True, CYAN), (panel.right - 460, panel.y + 16))

    def draw_hud(self) -> None:
        chapter_label = "EPILOGUE" if self.chapter == 12 else f"CHAPTER {self.chapter + 1:02d}"
        self.canvas.blit(self.chapter_font.render(chapter_label, True, CYAN), (120, 48))
        self.canvas.blit(self.small_font.render(CHAPTERS[self.chapter], True, WHITE), (120, 82))
        progress = (self.chapter + self.line_index / max(1, len(self.script[self.chapter]))) / 13
        pygame.draw.rect(self.canvas, (40, 54, 70), (120, 120, 440, 8), border_radius=4)
        pygame.draw.rect(self.canvas, MAGENTA, (120, 120, int(440 * progress), 8), border_radius=4)
        self.canvas.blit(self.small_font.render("F5 SAVE   F9 LOAD   ESC MENU", True, MUTED), (1470, 58))

    def draw_game(self) -> None:
        blackout = self.line.effect == "blackout"
        self.draw_background(self.line.bg, blackout)
        self.draw_characters(self.line.cast, self.line.text)
        if self.line.effect == "rain":
            self.draw_rain()
        if self.line.effect == "blackout":
            self.draw_rain(True)
        if self.line.effect == "impact":
            pygame.draw.circle(self.canvas, LIME, (1460, 500), 88, 5)
            pygame.draw.circle(self.canvas, WHITE, (1460, 500), 24, 3)
        self.draw_hud()
        self.draw_dialogue()
        if time.monotonic() < self.notice_until:
            banner = self.small_font.render(self.save_notice, True, LIME)
            self.canvas.blit(banner, (120, 150))

    def draw_menu(self) -> None:
        self.draw_background(0)
        shade = pygame.Surface(LOGICAL_SIZE, pygame.SRCALPHA)
        shade.fill((5, 10, 20, 130))
        self.canvas.blit(shade, (0, 0))
        if self.assets.logo:
            logo = self.assets.logo.copy()
            scale = min(1.0, 760 / max(1, logo.get_width()))
            logo = pygame.transform.smoothscale(logo, (int(logo.get_width() * scale), int(logo.get_height() * scale)))
            self.canvas.blit(logo, logo.get_rect(center=(960, 250)))
        else:
            self.canvas.blit(self.title_font.render("AUGUSTA MAINERELLA", True, WHITE), (500, 180))
            self.canvas.blit(self.title_font.render("FIRST CASE", True, MAGENTA), (690, 270))
        self.draw_text(self.canvas, "A CYBER-NOIR VISUAL NOVEL", (760, 400), self.chapter_font, CYAN, 500, 4)
        input_rect = pygame.Rect(650, 515, 620, 70)
        pygame.draw.rect(self.canvas, (8, 18, 30, 225), input_rect, border_radius=8)
        pygame.draw.rect(self.canvas, MAGENTA if self.name_active else CYAN, input_rect, width=2, border_radius=8)
        self.canvas.blit(self.small_font.render("PLAYER NAME", True, MUTED), (input_rect.x, input_rect.y - 34))
        self.canvas.blit(self.font.render(self.name_input or "Coptcat", True, WHITE), (input_rect.x + 22, input_rect.y + 18))
        buttons = [("BEGIN FIRST CASE", 620, 640, 680), ("LOAD CASE / SLOT 1", 620, 730, 680)]
        for label, x, y, width in buttons:
            rect = pygame.Rect(x, y, width, 66)
            pygame.draw.rect(self.canvas, (12, 27, 40, 230), rect, border_radius=8)
            pygame.draw.rect(self.canvas, LIME if label.startswith("BEGIN") else CYAN, rect, width=2, border_radius=8)
            text = self.chapter_font.render(label, True, WHITE)
            self.canvas.blit(text, text.get_rect(center=rect.center))
        self.draw_text(self.canvas, "ENTER starts  •  click the field to customize  •  assets are discovered from /secret or /images", (570, 900), self.small_font, MUTED, 800, 4)
        if time.monotonic() < self.notice_until:
            self.canvas.blit(self.small_font.render(self.save_notice, True, LIME), (780, 975))

    def logical_mouse(self, position: Tuple[int, int]) -> Tuple[int, int]:
        width, height = self.window.get_size()
        scale = min(width / LOGICAL_SIZE[0], height / LOGICAL_SIZE[1])
        offset_x = (width - LOGICAL_SIZE[0] * scale) / 2
        offset_y = (height - LOGICAL_SIZE[1] * scale) / 2
        return (int((position[0] - offset_x) / scale), int((position[1] - offset_y) / scale))

    def handle_menu_click(self, position: Tuple[int, int]) -> None:
        x, y = position
        if pygame.Rect(650, 515, 620, 70).collidepoint(x, y):
            self.name_active = True
        elif pygame.Rect(620, 640, 680, 66).collidepoint(x, y):
            self.reset_case()
        elif pygame.Rect(620, 730, 680, 66).collidepoint(x, y):
            self.load_case()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.VIDEORESIZE:
            self.window = pygame.display.set_mode(event.size, pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            position = self.logical_mouse(event.pos)
            if self.state == "menu":
                self.handle_menu_click(position)
            else:
                self.advance()
        elif event.type == pygame.KEYDOWN:
            if self.state == "menu":
                if event.key == pygame.K_RETURN:
                    self.reset_case()
                elif event.key == pygame.K_BACKSPACE and self.name_active:
                    self.name_input = self.name_input[:-1]
                elif event.key == pygame.K_ESCAPE:
                    self.name_active = False
                elif self.name_active and event.unicode.isprintable() and len(self.name_input) < 22:
                    self.name_input += event.unicode
            else:
                if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_RIGHT):
                    self.advance()
                elif event.key == pygame.K_ESCAPE:
                    self.state = "menu"
                elif event.key == pygame.K_F5:
                    self.save_case()
                elif event.key == pygame.K_F9:
                    self.load_case()

    def present(self) -> None:
        width, height = self.window.get_size()
        scale = min(width / LOGICAL_SIZE[0], height / LOGICAL_SIZE[1])
        scaled_size = (int(LOGICAL_SIZE[0] * scale), int(LOGICAL_SIZE[1] * scale))
        scaled = pygame.transform.smoothscale(self.canvas, scaled_size)
        self.window.fill((2, 4, 10))
        self.window.blit(scaled, ((width - scaled_size[0]) // 2, (height - scaled_size[1]) // 2))
        pygame.display.flip()

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.canvas.fill(INK)
            if self.state == "menu":
                self.draw_menu()
            else:
                self.draw_game()
            self.present()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    Game().run()
