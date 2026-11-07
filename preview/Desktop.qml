import QtQuick
import ".." as Plugin

Item {
  id: scene
  width: 1600
  height: 900
  property alias lockView: lockView
  Rectangle { anchors.fill: parent; color: "#0b1118" }
  Rectangle {
    width: parent.width; height: 38; color: "#151d28"
    Text { x: 24; anchors.verticalCenter: parent.verticalCenter; text: "OMARCHY     1   [2]   3   4"; textFormat: Text.PlainText; color: "#cbd5e1"; font.family: "monospace"; font.pixelSize: 13 }
    Text { anchors.centerIn: parent; text: "STAY AWAKE  /  WATCH LOCK"; textFormat: Text.PlainText; color: "#9ae6b4"; font.family: "monospace"; font.pixelSize: 12 }
    Text { anchors.right: parent.right; anchors.rightMargin: 24; anchors.verticalCenter: parent.verticalCenter; text: "DEMO     14:30"; textFormat: Text.PlainText; color: "#94a3b8"; font.family: "monospace"; font.pixelSize: 13 }
  }
  Text { x: 40; y: 60; text: "WATCH LOCK  /  KEEP AN EYE ON THE WORK"; textFormat: Text.PlainText; color: "#94a3b8"; font.family: "monospace"; font.pixelSize: 12; font.letterSpacing: 1.5 }
  Rectangle {
    x: 40; y: 100; width: 970; height: 500; color: "#111925"; radius: 10; border.color: "#29384c"
    Rectangle { width: parent.width; height: 40; color: "#1a2535"; radius: 10 }
    Text { x: 20; y: 12; text: "●  ●  ●     build / sample-workspace"; textFormat: Text.PlainText; color: "#8ba4bd"; font.family: "monospace"; font.pixelSize: 13 }
    Text {
      x: 28; y: 72; width: parent.width - 56
      textFormat: Text.PlainText
      text: "$ make verify\n\n[09/12] Compiling the demo application...\n[10/12] Running the sample test suite...\n\n  ✓ configuration loads\n  ✓ background tasks continue\n  ✓ preview fixtures contain sample data\n  ✓ no account details in output\n\n[11/12] Building release artifacts...\n        ████████████████████░░░░░░░░  72%\n\nWatching the work while app input is locked."
      font.family: "monospace"; font.pixelSize: 19; lineHeight: 1.4; color: "#b8d8c5"
    }
  }
  Rectangle {
    x: 1034; y: 100; width: 526; height: 500; color: "#111925"; radius: 10; border.color: "#29384c"
    Rectangle { width: parent.width; height: 40; color: "#1a2535"; radius: 10 }
    Text { x: 20; y: 12; text: "●  ●  ●     player / sample playlist"; textFormat: Text.PlainText; color: "#8ba4bd"; font.family: "monospace"; font.pixelSize: 13 }
    Rectangle {
      x: 32; y: 76; width: 462; height: 214; radius: 7
      gradient: Gradient { orientation: Gradient.Horizontal; GradientStop { position: 0; color: "#214d54" } GradientStop { position: 1; color: "#273050" } }
      Row {
        anchors.centerIn: parent; spacing: 12; height: 100
        Repeater {
          model: [28,52,85,61,100,73,40,86,59,33,68,45]
          Rectangle { required property int modelData; width: 16; height: modelData; anchors.bottom: parent.bottom; radius: 3; color: "#7dd3c4" }
        }
      }
    }
    Text { x: 34; y: 322; text: "Evening Signals"; textFormat: Text.PlainText; color: "#e2e8f0"; font.family: "monospace"; font.pixelSize: 24 }
    Text { x: 34; y: 360; text: "Sample Artist · Demo playlist"; textFormat: Text.PlainText; color: "#93a4b8"; font.family: "monospace"; font.pixelSize: 15 }
    Rectangle { x: 34; y: 410; width: 458; height: 4; color: "#2a3b4f"; Rectangle { width: parent.width * 0.62; height: parent.height; color: "#7dd3c4" } }
    Text { x: 34; y: 435; text: "02:18     ◀     ▌▌     ▶     03:42"; textFormat: Text.PlainText; color: "#bdcbdc"; font.family: "monospace"; font.pixelSize: 18 }
  }
  Rectangle {
    x: 40; y: 624; width: 970; height: 216; color: "#111925"; radius: 10; border.color: "#29384c"
    Text { x: 28; y: 26; text: "BACKGROUND WORK"; textFormat: Text.PlainText; color: "#7dd3c4"; font.family: "monospace"; font.pixelSize: 12; font.letterSpacing: 2 }
    Text { x: 28; y: 64; text: "build      running    •    output keeps updating\nplayer     playing    •    audio continues\napp input  locked     •    password required"; textFormat: Text.PlainText; color: "#afbed0"; font.family: "monospace"; font.pixelSize: 17; lineHeight: 1.7 }
  }
  Plugin.LockView {
    id: lockView
    anchors.fill: parent
    inputEnabled: false
    loadBackground: false
    liveBackground: true
    watchMode: true
  }
  Text {
    x: 40; y: 866
    text: "PREVIEW ONLY · SYNTHETIC APP CONTENT · NO REAL DESKTOP CAPTURED"
    textFormat: Text.PlainText; color: "#72869d"; font.family: "monospace"; font.pixelSize: 10
  }
}
