# Installation
## environment installation
- install poetry if it's not in your environment (see [python-poerty/poerty](https://github.com/python-poetry/poetry))
- use [pyenv](https://github.com/pyenv/pyenv) or [conda](https://github.com/conda/conda) to create a virtual environment of python version=3.8 (env name=pr-decision-bot, we will use this environment name in the following text)

```
git clone https://github.com/PR-bots/PR-decision-bot.git
cd PR-decision-bot
conda activate pr-decision-bot
poetry install
poetry shell
```