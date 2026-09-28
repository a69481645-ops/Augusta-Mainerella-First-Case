const DEFAULT_PLAYER_NAME = "Coptcat";
const chapters = [
  {
    chapter: 1,
    title: "Chapter 1",
    background: "linear-gradient(180deg, rgba(10,9,17,0.5), rgba(18,11,23,0.82)), url('assets/chapters/city-night.svg') center center / cover no-repeat",
    characters: {
      left: { name: "Augusta Mainerella", image: "assets/characters/augusta.svg", position: { x: 8, y: 0 }, visible: true },
      center: { name: "Coptcat", image: "assets/characters/coptcat.svg", position: { x: 46, y: 0 }, visible: true },
      right: { name: "Sabrina Shadowcoat", image: "assets/characters/sabrina.svg", position: { x: 76, y: 0 }, visible: true }
    },
    dialogue: [
      { speaker: "Augusta Mainerella", text: "Loppunie wasn't replying. The studio loft was too quiet, and the city lights were bleeding into the rain like a bad memory." },
      { speaker: "Coptcat", text: "The ancestral thread woke me. Your grandma calls through breath and ash, child. The clan is in danger." },
      { speaker: "Augusta Mainerella", text: "I called her. No answer. I checked the tracking desk, and Cideon Minx was already pulling dirty logs." }
    ]
  },
  {
    chapter: 2,
    title: "Chapter 2",
    background: "linear-gradient(180deg, rgba(12,10,14,0.5), rgba(15,10,26,0.82)), url('assets/chapters/city-night.svg') center center / cover no-repeat",
    characters: {
      left: { name: "Augusta Mainerella", image: "assets/characters/augusta.svg", position: { x: 12, y: 0 }, visible: true },
      center: { name: "Cideon Minx", image: "assets/characters/cideon.svg", position: { x: 48, y: 0 }, visible: true },
      right: { name: "Officer Shepherd", image: "assets/characters/shepherd.svg", position: { x: 74, y: 0 }, visible: true }
    },
    dialogue: [
      { speaker: "Cideon Minx", text: "Firewall bleed. Deep-web storefront. An OnlyFans-style slave-shipping platform with disguised payment channels and buyer lists." },
      { speaker: "Augusta Mainerella", text: "This isn't a prank. The city does not run on clean money. It runs on coercion and silence." },
      { speaker: "Officer Shepherd", text: "I can't touch it without a warrant and a body count. Call me when you have actual evidence." },
      { speaker: "Augusta Mainerella", text: "You just hung up on me, Shepherd. Real professional." }
    ]
  },
  {
    chapter: 3,
    title: "Chapter 3",
    background: "linear-gradient(180deg, rgba(6,9,17,0.52), rgba(12,16,28,0.84)), url('assets/chapters/loft-interior.svg') center center / cover no-repeat",
    characters: {
      left: { name: "Augusta Mainerella", image: "assets/characters/augusta.svg", position: { x: 10, y: 0 }, visible: true },
      center: { name: "Coptcat", image: "assets/characters/coptcat.svg", position: { x: 50, y: 0 }, visible: true },
      right: { name: "Agent Rouge", image: "assets/characters/rouge.svg", position: { x: 76, y: 0 }, visible: true }
    },
    dialogue: [
      { speaker: "Augusta Mainerella", text: "The only person who ever made this kind of thing feel like a rule-book was my ancestor. We have a codeword. Spyjewel." },
      { speaker: "Coptcat", text: "When the veil is torn, the hive remembers. The dead do not forget the living. A debt has been called." },
      { speaker: "Agent Rouge", text: "PTO? I took it. I am here. You can be dramatic later. Let's move." }
    ]
  },
  {
    chapter: 4,
    title: "Chapter 4",
    background: "linear-gradient(180deg, rgba(11,8,15,0.58), rgba(15,10,24,0.86)), url('assets/chapters/velvet-onyx.svg') center center / cover no-repeat",
    characters: {
      left: { name: "Sonic", image: "assets/characters/sonic.svg", position: { x: 11, y: 0 }, visible: true },
      center: { name: "Madonna", image: "assets/characters/madonna.svg", position: { x: 48, y: 0 }, visible: true },
      right: { name: "Augusta Mainerella", image: "assets/characters/augusta.svg", position: { x: 74, y: 0 }, visible: true }
    },
    dialogue: [
      { speaker: "Madonna", text: "Sonic, the money trail is all coming back to The Velvet Onyx. The cabaret is laundering nightlife cash into a side venture with blood on it." },
      { speaker: "Sonic", text: "Then we go in together. You sing and I watch the room. We cover each other. That's how it works." },
      { speaker: "Madonna", text: "And if anyone gets too comfortable, I remind them the stage has a trapdoor. We keep our eyes open." }
    ]
  },
  {
    chapter: 5,
    title: "Chapter 5",
    background: "linear-gradient(180deg, rgba(13,10,17,0.52), rgba(18,13,24,0.84)), url('assets/chapters/velvet-onyx.svg') center center / cover no-repeat",
    characters: {
      left: { name: "Augusta Mainerella", image: "assets/characters/augusta.svg", position: { x: 12, y: 0 }, visible: true },
      center: { name: "Cleo Habessha", image: "assets/characters/cleo.svg", position: { x: 50, y: 0 }, visible: true },
      right: { name: "Sonic", image: "assets/characters/sonic.svg", position: { x: 76, y: 0 }, visible: true }
    },
    dialogue: [
      { speaker: "Cleo Habessha", text: "I don't traffic human beings. I sell nights, not flesh. Forced human slavery is a line I will not cross, and Vance made his mistake when he thought my curtain call could be bought." },
      { speaker: "Augusta Mainerella", text: "Then hand over the keycard and stop pretending your vanity isn't as sharp as a blade." },
      { speaker: "Cleo Habessha", text: "Take the mansion keycard. The only thing I am guaranteeing is his collapse. I prefer a cleaner city." }
    ]
  },
  {
    chapter: 6,
    title: "Chapter 6",
    background: "linear-gradient(180deg, rgba(12,14,18,0.52), rgba(15,20,26,0.85)), url('assets/chapters/alley-rain.svg') center center / cover no-repeat",
    characters: {
      left: { name: "Augusta Mainerella", image: "assets/characters/augusta.svg", position: { x: 9, y: 0 }, visible: true },
      center: { name: "Sabrina Shadowcoat", image: "assets/characters/sabrina.svg", position: { x: 49, y: 0 }, visible: true },
      right: { name: "Sonic", image: "assets/characters/sonic.svg", position: { x: 78, y: 0 }, visible: true }
    },
    dialogue: [
      { speaker: "Sabrina Shadowcoat", text: "I sell surveillance, not ideology. I survive. My code is not moral, just profitable. If you want the courtyard floodlights dead, there is a price." },
      { speaker: "Augusta Mainerella", text: "Your price is survival. Mine is a city that doesn't get sold off by a cartel and a smirk. You know what a pack-protector does when the line is crossed." },
      { speaker: "Sabrina Shadowcoat", text: "Then keep your claws to yourself. I am not your sister. I am not your enemy. I am a bargain. Here. The breaker switch is yours." }
    ]
  },
  {
    chapter: 7,
    title: "Chapter 7",
    background: "linear-gradient(180deg, rgba(10,13,18,0.5), rgba(14,19,28,0.76)), url('assets/chapters/vault.svg') center center / cover no-repeat",
    characters: {
      left: { name: "Augusta Mainerella", image: "assets/characters/augusta.svg", position: { x: 14, y: 0 }, visible: true },
      center: { name: "Sonic", image: "assets/characters/sonic.svg", position: { x: 48, y: 0 }, visible: true },
      right: { name: "Silas Flint", image: "assets/characters/silas.svg", position: { x: 75, y: 0 }, visible: true }
    },
    dialogue: [
      { speaker: "Silas Flint", text: "This vault belongs to the family. You are not walking out of it. We have guns and an empty conscience." },
      { speaker: "Sonic", text: "Good. I like a fair fight. You can start by missing." },
      { speaker: "Augusta Mainerella", text: "Heavy boots. Heavy answers. I'm the line. And if you are in my space, you are in my kick zone." },
      { speaker: "Cideon Minx", text: "I am copying the encryption files. Keep the server room breathing for five more seconds." }
    ]
  },
  {
    chapter: 8,
    title: "Chapter 8",
    background: "linear-gradient(180deg, rgba(7,8,12,0.56), rgba(15,12,18,0.8)), url('assets/chapters/dungeon.svg') center center / cover no-repeat",
    characters: {
      left: { name: "Augusta Mainerella", image: "assets/characters/augusta.svg", position: { x: 12, y: 0 }, visible: true },
      center: { name: "Loppunie", image: "assets/characters/loppunie.svg", position: { x: 50, y: 0 }, visible: true },
      right: { name: "Baron Vance", image: "assets/characters/vance.svg", position: { x: 76, y: 0 }, visible: true }
    },
    dialogue: [
      { speaker: "Loppunie", text: "Augusta... I kept thinking they would never make it. I could hear the city through the walls, but not my own heartbeat." },
      { speaker: "Baron Vance", text: "A miracle of poor choices and excellent logistics. Jax, tell them why the smirk is permanent. It's the only expression worth keeping." },
      { speaker: "Augusta Mainerella", text: "The man who thinks a smirk is a personality can never understand the weight of a human being. Not mine. Not hers." }
    ]
  },
  {
    chapter: 9,
    title: "Chapter 9",
    background: "linear-gradient(180deg, rgba(8,8,13,0.52), rgba(14,14,18,0.82)), url('assets/chapters/dungeon.svg') center center / cover no-repeat",
    characters: {
      left: { name: "Augusta Mainerella", image: "assets/characters/augusta.svg", position: { x: 14, y: 0 }, visible: true },
      center: { name: "Coptcat", image: "assets/characters/coptcat.svg", position: { x: 50, y: 0 }, visible: true },
      right: { name: "Sonic", image: "assets/characters/sonic.svg", position: { x: 74, y: 0 }, visible: true }
    },
    dialogue: [
      { speaker: "Coptcat", text: "I have not spoken in years. The law of the line is simple: no one owns a person. Not a cartel, not a cage, not a man with a smirk. Rise." },
      { speaker: "Sonic", text: "On it. Loppunie, stay with me. Augusta, take the camera. Cideon, wipe it all before the light comes back." },
      { speaker: "Augusta Mainerella", text: "The box camera goes down. The monster does not have a final word. I am not here to be polite. I am here to end this." }
    ]
  },
  {
    chapter: 10,
    title: "Chapter 10",
    background: "linear-gradient(180deg, rgba(10,9,15,0.54), rgba(18,10,18,0.8)), url('assets/chapters/mansion.svg') center center / cover no-repeat",
    characters: {
      left: { name: "Augusta Mainerella", image: "assets/characters/augusta.svg", position: { x: 10, y: 0 }, visible: true },
      center: { name: "Agent Rouge", image: "assets/characters/rouge.svg", position: { x: 50, y: 0 }, visible: true },
      right: { name: "Cleo Habessha", image: "assets/characters/cleo.svg", position: { x: 76, y: 0 }, visible: true }
    },
    dialogue: [
      { speaker: "Agent Rouge", text: "Task force is clearing the mansion. The operation is falling apart in real time. We have the evidence, the witness, and the exit window." },
      { speaker: "Cleo Habessha", text: "I am taking legal control of the cabaret. The city is fickle, but tonight I prefer the law and the stage to the dungeon behind it." },
      { speaker: "Augusta Mainerella", text: "Good. The city deserves better than a smirk and a spreadsheet." }
    ]
  },
  {
    chapter: 11,
    title: "Chapter 11",
    background: "linear-gradient(180deg, rgba(8,9,18,0.54), rgba(10,9,17,0.84)), url('assets/chapters/white-backdrop.svg') center center / cover no-repeat",
    characters: {
      left: { name: "Augusta Mainerella", image: "assets/characters/augusta.svg", position: { x: 12, y: 0 }, visible: true },
      center: { name: "Loppunie", image: "assets/characters/loppunie.svg", position: { x: 50, y: 0 }, visible: true },
      right: { name: "Madonna", image: "assets/characters/madonna.svg", position: { x: 76, y: 0 }, visible: true }
    },
    dialogue: [
      { speaker: "Loppunie", text: "I can feel my limbs again. The weight is gone. There is no chain left inside me but the one that tells me where I belong, and I know where that is now." },
      { speaker: "Madonna", text: "You belong in your own story, sweetheart. We just gave you back the room to write it. That's all." },
      { speaker: "Augusta Mainerella", text: "And I will stand with you while the city learns what personal autonomy looks like in the light." }
    ]
  },
  {
    chapter: 12,
    title: "Chapter 12",
    background: "linear-gradient(180deg, rgba(7,9,14,0.58), rgba(15,20,28,0.88)), url('assets/chapters/night-city.svg') center center / cover no-repeat",
    characters: {
      left: { name: "Augusta Mainerella", image: "assets/characters/augusta.svg", position: { x: 12, y: 0 }, visible: true },
      center: { name: "Coptcat", image: "assets/characters/coptcat.svg", position: { x: 50, y: 0 }, visible: true },
      right: { name: "Cideon Minx", image: "assets/characters/cideon.svg", position: { x: 78, y: 0 }, visible: true }
    },
    dialogue: [
      { speaker: "Coptcat", text: "The city will keep its scars. But no one will own the soul of a living body again. The sacred right of personal agency remains law beyond the paper and beyond the cage." },
      { speaker: "Augusta Mainerella", text: "Then we keep the record. We keep the names. And we keep walking away from the grave they wanted us in." },
      { speaker: "Cideon Minx", text: "I have the archive. They won't be able to scrub the ledger to fit their lie." }
    ]
  },
  {
    chapter: 13,
    title: "Epilogue",
    background: "linear-gradient(180deg, rgba(8,9,17,0.56), rgba(16,10,20,0.86)), url('assets/chapters/white-backdrop.svg') center center / cover no-repeat",
    characters: {
      left: { name: "Augusta Mainerella", image: "assets/characters/augusta.svg", position: { x: 12, y: 0 }, visible: true },
      center: { name: "Loppunie", image: "assets/characters/loppunie.svg", position: { x: 50, y: 0 }, visible: true },
      right: { name: "Coptcat", image: "assets/characters/coptcat.svg", position: { x: 76, y: 0 }, visible: true }
    },
    dialogue: [
      { speaker: "Coptcat", text: "The sacred right of personal agency is not a slogan. It is the door. It is the law of the body, the breath, and the future. Walk through it and keep your name." },
      { speaker: "Loppunie", text: "I am smiling because I am home. Not in the tower. In myself." },
      { speaker: "Augusta Mainerella", text: "This is the kind of case that changes a city. And it begins with one answer: never again." }
    ]
  }
];

const saveSlots = [
  { id: 1, label: "Slot 1", timestamp: "No save" },
  { id: 2, label: "Slot 2", timestamp: "No save" },
  { id: 3, label: "Slot 3", timestamp: "No save" }
];

const state = {
  screen: "mainMenu",
  chapterIndex: 0,
  dialogueIndex: 0,
  playerName: "",
  textSpeed: 35,
  volume: 75,
  ambientOn: true,
  saveData: { 1: null, 2: null, 3: null }
};

const ui = {
  mainMenu: document.getElementById("mainMenu"),
  gameScreen: document.getElementById("gameScreen"),
  loadScreen: document.getElementById("loadScreen"),
  settingsScreen: document.getElementById("settingsScreen"),
  backgroundLayer: document.getElementById("backgroundLayer"),
  characterLeft: document.getElementById("charLeft"),
  characterCenter: document.getElementById("charCenter"),
  characterRight: document.getElementById("charRight"),
  dialogueName: document.getElementById("dialogueName"),
  dialogueText: document.getElementById("dialogueText"),
  chapterBadge: document.getElementById("chapterBadge"),
  saveSlots: document.getElementById("saveSlots"),
  masterVolume: document.getElementById("masterVolume"),
  volumeValue: document.getElementById("volumeValue"),
  textSpeed: document.getElementById("textSpeed"),
  ambientToggle: document.getElementById("ambientToggle"),
  ambientAudio: document.getElementById("ambientAudio"),
  playerNameInput: document.getElementById("playerNameInput")
};

function setScreen(name) {
  const screens = [ui.mainMenu, ui.gameScreen, ui.loadScreen, ui.settingsScreen];
  screens.forEach((screen) => screen.classList.remove("active"));

  const target = {
    mainMenu: ui.mainMenu,
    game: ui.gameScreen,
    load: ui.loadScreen,
    settings: ui.settingsScreen
  }[name];

  if (target) target.classList.add("active");
}

function setBackground(backgroundCss) {
  ui.backgroundLayer.style.background = backgroundCss;
}

function showCharacter(slot, sprite) {
  const node = slot === "left" ? ui.characterLeft : slot === "center" ? ui.characterCenter : ui.characterRight;
  if (!sprite || !sprite.image) {
    node.src = "";
    node.classList.remove("visible");
    return;
  }

  node.src = sprite.image;
  node.alt = sprite.name || "Character";
  node.classList.add("visible");
  const baseScale = slot === "center" ? 1.1 : 1;
  node.style.transform = `translate(${slot === "center" ? "-50%" : "0px"}, 0) scale(${baseScale})`;
  node.style.left = slot === "center" ? "50%" : slot === "left" ? "4%" : "72%";
}

function renderDialogue() {
  const chapter = chapters[state.chapterIndex];
  const line = chapter.dialogue[state.dialogueIndex];
  const left = chapter.characters.left;
  const center = chapter.characters.center;
  const right = chapter.characters.right;

  ui.dialogueName.textContent = line.speaker;
  ui.dialogueText.textContent = line.text;
  ui.chapterBadge.textContent = chapter.title;

  setBackground(chapter.background);
  showCharacter("left", left);
  showCharacter("center", center);
  showCharacter("right", right);

  const name = state.playerName || DEFAULT_PLAYER_NAME;
  if (line.speaker === "Coptcat") {
    ui.dialogueName.textContent = name;
  }
}

function advanceDialogue() {
  const chapter = chapters[state.chapterIndex];
  if (state.dialogueIndex < chapter.dialogue.length - 1) {
    state.dialogueIndex += 1;
    renderDialogue();
    return;
  }

  if (state.chapterIndex < chapters.length - 1) {
    state.chapterIndex += 1;
    state.dialogueIndex = 0;
    renderDialogue();
    return;
  }

  endGame();
}

function endGame() {
  setScreen("mainMenu");
  ui.playerNameInput.value = state.playerName;
}

function triggerAmbientAudio() {
  if (!state.ambientOn) {
    ui.ambientAudio.pause();
    return;
  }

  ui.ambientAudio.volume = state.volume / 100;
  ui.ambientAudio.play().catch(() => {});
}

function initializeSaveSlots() {
  ui.saveSlots.innerHTML = saveSlots
    .map(
      (slot) => `
        <div class="save-slot" data-slot="${slot.id}">
          <div>
            <strong>${slot.label}</strong>
            <span>${slot.timestamp}</span>
          </div>
          <span>Load</span>
        </div>
      `
    )
    .join("");

  ui.saveSlots.querySelectorAll(".save-slot").forEach((slot) => {
    slot.addEventListener("click", () => {
      const id = Number(slot.dataset.slot);
      const data = state.saveData[id];
      if (data) {
        state.chapterIndex = data.chapterIndex;
        state.dialogueIndex = data.dialogueIndex;
        state.playerName = data.playerName || DEFAULT_PLAYER_NAME;
        renderDialogue();
        setScreen("game");
      }
    });
  });
}

function saveGame(slotId) {
  state.saveData[slotId] = {
    chapterIndex: state.chapterIndex,
    dialogueIndex: state.dialogueIndex,
    playerName: state.playerName || DEFAULT_PLAYER_NAME
  };

  saveSlots[slotId - 1].timestamp = new Date().toLocaleString();
  initializeSaveSlots();
}

function startGame() {
  const input = ui.playerNameInput.value.trim();
  state.playerName = input || DEFAULT_PLAYER_NAME;
  state.chapterIndex = 0;
  state.dialogueIndex = 0;
  renderDialogue();
  setScreen("game");
  triggerAmbientAudio();
}

function bindMenuActions() {
  document.getElementById("newGameBtn").addEventListener("click", startGame);
  document.getElementById("loadGameBtn").addEventListener("click", () => {
    initializeSaveSlots();
    setScreen("load");
  });
  document.getElementById("settingsBtn").addEventListener("click", () => setScreen("settings"));
  document.getElementById("backFromLoadBtn").addEventListener("click", () => setScreen("mainMenu"));
  document.getElementById("backFromSettingsBtn").addEventListener("click", () => setScreen("mainMenu"));

  ui.gameScreen.addEventListener("click", () => {
    advanceDialogue();
  });

  document.addEventListener("keydown", (event) => {
    if (event.code === "Space" || event.code === "Enter" || event.code === "ArrowRight") {
      if (ui.gameScreen.classList.contains("active")) {
        event.preventDefault();
        advanceDialogue();
      }
    }

    if (event.code === "KeyS" && (ui.gameScreen.classList.contains("active") || ui.mainMenu.classList.contains("active"))) {
      saveGame(1);
    }
  });

  ui.masterVolume.addEventListener("input", (event) => {
    state.volume = Number(event.target.value);
    ui.volumeValue.textContent = `${state.volume}%`;
    ui.ambientAudio.volume = state.volume / 100;
  });

  ui.textSpeed.addEventListener("change", (event) => {
    const value = event.target.value;
    const timing = {
      slow: 90,
      normal: 35,
      fast: 18,
      instant: 1
    };
    state.textSpeed = timing[value] ?? 35;
  });

  ui.ambientToggle.addEventListener("change", (event) => {
    state.ambientOn = event.target.checked;
    triggerAmbientAudio();
  });
}

function init() {
  setScreen("mainMenu");
  initializeSaveSlots();
  bindMenuActions();
  ui.ambientAudio.volume = state.volume / 100;
  ui.masterVolume.value = String(state.volume);
  ui.volumeValue.textContent = `${state.volume}%`;
}

window.addEventListener("DOMContentLoaded", init);
