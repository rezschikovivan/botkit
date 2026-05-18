from setuptools import setup, find_packages
from abot import __version__

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='abot',
  version = __version__,
  author='rezschikovivan',
  author_email='rezschikovivan@gmail.com',
  description='Framework for creating bots',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/rezschikovivan/abot',
  packages=find_packages(),
  install_requires=[
    'vkbottle==4.8.0', 
    'aiogram==3.27.0'
    ],
  classifiers=[
    'Programming Language :: Python :: 3.14',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='abot bot bots asynchronous',
  project_urls= {},
  python_requires='>=3.12.0'
)