from setuptools import setup, find_packages

setup(
    name="fun-tools",
    version="1.0.0",
    description="A collection of fun games and utilities",
    author="HongKiBum",
    author_email="hgb9720@hanyang.ac.kr",
    url="https://github.com/HongKiBum/toytoy3",
    packages=find_packages(),
    install_requires=[
        "kivy",            # 필요한 패키지
        "mediapipe",       # 필요한 패키지
        "ultralytics",     # 필요한 패키지
    ],
    python_requires=">=3.7",
)
