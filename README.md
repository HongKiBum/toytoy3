Fun Tools

A collection of fun games and utilities for Python enthusiasts!

Features
- Guess the Person: Identify people based on images.
- Group Photo Analyzer: Analyze group photos using AI.
- Pronunciation Game: Evaluate your pronunciation accuracy.
- Roulette Game: Spin the wheel for a random choice.
- Receipt Splitter: Split bills among a group.

Installation
Install Fun Tools via pip:
pip install fun-tools

Usage Examples

Guess the Person
from fun_tools.games import GuessGameApp

custom_images = [
    {"image": "person1.jpg", "answer": "Person1"},
    {"image": "person2.jpg", "answer": "Person2"},
]

app = GuessGameApp(images=custom_images)
app.run()

Group Photo Analyzer
from tkinter import Tk
from fun_tools.games import GroupPhotoAnalyzer

root = Tk()
app = GroupPhotoAnalyzer(root)
root.mainloop()

Pronunciation Game
from tkinter import Tk
from fun_tools.games import PronunciationApp

root = Tk()
app = PronunciationApp(root, logo_path="path/to/logo.png")
app.run()

Roulette Game
from fun_tools.games import Roulette

values = ["Option 1", "Option 2", "Option 3"]
roulette = Roulette(values)
roulette.run()

Receipt Splitter
from fun_tools.utils import ReceiptSplitter

app = ReceiptSplitter()
app.run()

Documentation
Full documentation is available at [Read the Docs](https://fun-tools.readthedocs.io/).

License
This project is licensed under the MIT License.
