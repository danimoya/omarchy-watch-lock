import QtQuick
import QtTest
import Quickshell
import "." as Fixture

TestCase {
  id: test
  name: "SafePreview"
  visible: true
  when: false
  width: 1600
  height: 900
  property bool saved: false
  Fixture.Desktop { id: desktop; anchors.fill: parent }

  function save(name) {
    saved = false
    verify(desktop.grabToImage(function(result) {
      verify(result.saveToFile(Quickshell.env("WATCH_LOCK_OUTPUT") + "/" + name))
      saved = true
    }))
    tryCompare(test, "saved", true)
  }

  function test_capture() {
    var panel = findChild(desktop, "passwordPanel")
    verify(panel !== null)
    mouseMove(desktop, 2, 2)
    tryCompare(panel, "opacity", 0.05)
    save("watch-lock-faded.png")
    var center = panel.mapToItem(desktop, panel.width / 2, panel.height / 2)
    mouseMove(desktop, center.x, center.y)
    tryCompare(panel, "opacity", 1)
    save("watch-lock.png")
    console.log("SAFE_PREVIEW_CAPTURED")
  }
}
