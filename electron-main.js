const { app, BrowserWindow } = require("electron");
const path = require("node:path");

function createWindow() {
  const iconPath = path.join(__dirname, "assets", "icon.svg");
  const window = new BrowserWindow({
    width: 1280,
    height: 720,
    minWidth: 960,
    minHeight: 540,
    title: "Augusta Mainerella: First Case",
    icon: iconPath,
    backgroundColor: "#030812",
    autoHideMenuBar: true,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true
    }
  });

  window.loadFile(path.join(__dirname, "index.html"));
}

app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});
