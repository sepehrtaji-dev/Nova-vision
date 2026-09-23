import sys

print("Python version:", sys.version)

try:
    from PySide6.QtWidgets import QApplication, QLabel
    print("PySide6 imported successfully")
except Exception as e:
    print("PySide6 import failed:", e)
    sys.exit(1)

app = QApplication(sys.argv)
print("QApplication created")

label = QLabel("If you see this window, PySide6 is working")
label.resize(420, 200)
label.show()

print("Window shown, entering event loop")

code = app.exec()

print("Event loop exited with code:", code)