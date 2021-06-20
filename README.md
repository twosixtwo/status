# status [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
Status page without any javascript, because who needs javascript!
Code might be a bit messy, wrote this at 3am.

## How it works
It uses server-side insertion, to avoid any usage of javascript.

## How to setup
- Rename `config.x.json` to `config.json` and change the values in it
- IMPORTANT: Time is in seconds and the only available methods are: `http` and `ping`. When using http don't forget to add `https://`!
- Install dependencies `pip install -r requirements.txt`
- Run