from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "skewheap - a fast, mergeable priority queue"

setup(
        name="skewheap",
        version=VERSION,
        author="Jeff Ober",
        author_email="<sysread@fastmail.fm>",
        description=DESCRIPTION,
        long_description=DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        keywords=[
            "heap",
            "skewheap",
            "priority",
            "queue",
        ],
        classifiers= [
            "Development Status :: 4 - Beta",
            "License :: OSI Approved :: MIT License",
            "Topic :: Utilities",
        ],
)
