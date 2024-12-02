from setuptools import setup, find_packages

setup(
    name="fun-tools",
    version="1.0.0",
    description="A collection of fun games and utilities",
    author="Hong Ki Bum",
    author_email="your_email@example.com",
    url="https://github.com/HongKiBum/toytoy3",
    packages=find_packages(),
    install_requires=[
        "kivy>=2.0.0",       # Kivy 라이브러리
        "mediapipe",         # Mediapipe 라이브러리
        "ultralytics"        # Ultralytics YOLO 라이브러리
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
