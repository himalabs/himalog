import importlib_metadata

try:
    VERSION = importlib_metadata.version("himalog")
except importlib_metadata.PackageNotFoundError:
    VERSION = "unknown"
    print("Package 'himalog' is not installed. __version__ set to 'unknown'.")

__version__ = VERSION
