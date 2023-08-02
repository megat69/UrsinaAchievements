# More information
A simple library for creating achievements for the Ursina game engine.

*Note : the library is currently pretty barebones, but it is still usable, as seen in the game [Rally](https://mandaw2014.itch.io/rally) by [Mandaw2014](https://github.com/mandaw2014/). The library usage is shown in [the game's fourth devlog.](https://www.youtube.com/watch?v=Akqf1_ethQ8)*

## How to use the library
To use this library, first download this repository, and add the UrsinaAchievements folder to your game's main folder.

Then, in your main file, import the `create_achievement` function.
```python
from UrsinaAchievements import create_achievement
```

This function takes several parameters into account.
- `name` (str) : Name of the achievement.
- `condition` : Callback function representing the condition under which the achievement must be unlocked.
  - Unlocks the achievement if the returned value is True and passes if the returned value is either False or None.
- `icon` (str, None by default) : The path to the image of your choice that will represent your achievement. (optional)
- `sound` (str, "sudden" by default) : Name of the sound used to signal the achievement get.
  - This could be "ringing", "rising", "sudden" or the path to a WAV format file.
- `duration` (float, 1 by default) : Time during which the achievement will be displayed on screen.

For example :
```python
from ursina import *
from UrsinaAchievements import create_achievement

app = Ursina(borderless = False, fullscreen = True, development_mode = False)

do = False

def cond():
    global do
    return do

create_achievement(name = 'Welcome!', condition = cond, icon = 'confetti', sound = 'sudden', duration = 1.5)

def setdo():
    global do
    do = True
invoke(setdo, delay = 3)

Sky()

app.run()
```

## Customisation
You can customise the appearance of the achievement by importing the Achievement class and modifying the following variables associated with it:
- `Achievement.achievement_color`
- `Achievement.text_color`
- `Achievement.icon_color`

They correspond to a tuple of three integer values.

## Features & Todos
- [x] Popups at the bottom-right corner of the screen
  - Contains an achievement name
  - An icon
- [x] Every frame, each function given for the argument check is tested ; achievement is given if the function tests true
- [x] All gotten achievements are stored in a JSON file
- [ ] An HTML file is generated with every achievement you got
- [ ] The function used for creating the achievements can be used as a decorator
