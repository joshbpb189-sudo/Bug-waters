from datetime import datetime
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
import platform
import sys

KV = r"""
<RootUI>:
    orientation: "vertical"
    padding: "18dp"
    spacing: "12dp"
    canvas.before:
        Color:
            rgba: 0.055, 0.07, 0.10, 1
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        text: "WATERS BUG"
        font_size: "26sp"
        bold: True
        size_hint_y: None
        height: "48dp"
        color: 0.35, 0.78, 0.95, 1
    Label:
        text: "SYSTEM CHECKER"
        font_size: "13sp"
        size_hint_y: None
        height: "24dp"
        color: 0.78, 0.84, 0.90, 1
    Label:
        text: root.status
        size_hint_y: None
        height: "42dp"
        color: 0.45, 0.9, 0.62, 1
    BoxLayout:
        size_hint_y: None
        height: "48dp"
        spacing: "10dp"
        Button:
            text: "MULAI"
            on_release: root.start_check()
        Button:
            text: "BERHENTI"
            on_release: root.stop_check()
    Label:
        text: "LOG AKTIVITAS"
        size_hint_y: None
        height: "28dp"
        bold: True
        color: 0.8, 0.86, 0.92, 1
    TextInput:
        id: log
        text: "Aplikasi siap. Tekan MULAI untuk pemeriksaan lokal.\\n"
        readonly: True
        multiline: True
        background_color: 0.10, 0.13, 0.18, 1
        foreground_color: 0.88, 0.92, 0.96, 1
    Label:
        text: "Pemeriksaan hanya membaca informasi dasar perangkat dan tidak berinteraksi dengan aplikasi lain."
        font_size: "11sp"
        size_hint_y: None
        height: "42dp"
        color: 0.65, 0.72, 0.80, 1
"""

class RootUI(BoxLayout):
    running = BooleanProperty(False)
    status = StringProperty("Status: SIAP")
    event = None

    def add_log(self, message):
        self.ids.log.text += f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n"

    def start_check(self):
        if self.running:
            self.add_log("Pemeriksaan sedang berjalan.")
            return
        self.running = True
        self.status = "Status: MEMERIKSA"
        self.add_log("Pemeriksaan lokal dimulai.")
        self.event = Clock.schedule_once(self.run_check, 0.5)

    def run_check(self, _dt):
        if not self.running:
            return
        self.add_log(f"Platform: {platform.system() or 'Android'}")
        self.add_log(f"Versi Python: {sys.version.split()[0]}")
        self.add_log("Aplikasi berjalan dan antarmuka merespons.")
        self.running = False
        self.status = "Status: SELESAI"
        self.add_log("Pemeriksaan selesai.")

    def stop_check(self):
        if self.event is not None:
            self.event.cancel()
            self.event = None
        self.running = False
        self.status = "Status: DIHENTIKAN"
        self.add_log("Pemeriksaan dihentikan.")

class WatersBugApp(App):
    title = "WATERS BUG"

    def build(self):
        Builder.load_string(KV)
        return RootUI()

if __name__ == "__main__":
    WatersBugApp().run()
