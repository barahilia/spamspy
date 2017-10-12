from setuptools import setup

setup(
    name='spamspy',
    version='0.1',
    packages=['spamspy'],
    entry_points={
        'console_scripts': [
            'spamsum = spamspy.spamsum:main',
            'edit_dist = spamspy.edit_dist:main',
            'ngram_spy = spamspy.ngram:main',
        ]
    },

    license='MIT License',
    long_description=open('README.rst').read(),

    url='https://github.com/barahilia/spamspy',
    author='Ilia Barahovsky',
    author_email='barahilia@gmail.com'
)
