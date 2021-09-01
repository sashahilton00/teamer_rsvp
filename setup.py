from distutils.core import setup
import py2exe

setup(
    console=[{
        'script': 'main.py',
        'icon_resources': [(0, 'icon/teamer.ico')],
        'dest_base': 'Teamer'
    }],
    options={
        'py2exe': {
            'bundle_files': 3,
            'optimize': 2,
            'dist_dir': 'executable'
        }
    }
)
