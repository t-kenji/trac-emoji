from distutils.core import setup
from setuptools import find_packages

version='0.6'

setup(
    name='trac-emoji',
    url='https://github.com/pykler/TracEmoji',
    long_description='Emoji plugin for trac implementing https://github.com/WebpageFX/emoji-cheat-sheet.com.git',
    author='Hatem Nassrat',
    author_email='hatem@nassrat.ca',
    version=version,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    entry_points = """
        [trac.plugins]
        trac_emoji = trac_emoji
    """,
)
