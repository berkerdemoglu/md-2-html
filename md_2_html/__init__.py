from pathlib import Path
# below solution from: https://github.com/python-poetry/poetry/pull/2366#issuecomment-652418094
try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version(__name__)

assets_path = Path(__file__).parent / 'assets'
resources_path = Path(__file__).parent / 'resources'