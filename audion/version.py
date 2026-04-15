from importlib import metadata

try:
    __version__ = metadata.version("audion-sdk")
except metadata.PackageNotFoundError:
    __version__ = "0.1.7"
