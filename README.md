# UrsinaAchievements
A simple WIP library allowing you to create achievements for the Ursina game engine !

*Note : the library is currently pretty barebones, but it is still usable, as seen in the game [Rally](https://mandaw2014.itch.io/rally) by [Mandaw2014](https://github.com/mandaw2014/). The library usage is shown in [the game's fourth devlog.](https://www.youtube.com/watch?v=Akqf1_ethQ8)*

## Library usage
To use the library, first download this repo, and add the UrsinaAchievements folder to your game's main folder.

Then, in your main file, import the `create_achievement` function.
```python
from UrsinaAchievements import create_achievement
```

You can now create achievements by calling the function, with the following parameters :
- `name` (str) : The name of the achievement.
- `unlock_condition` : A callback function representing whether the achievement should be unlocked.
  - Unlocks the achievement if the return value is True, passes if it is either False or None.
- `icon` (str, None by default) : The path to the image file being represented with the text, optional.
- `ringtone` (str, "clicking" by default) : The name of the ringtone to be used to signal the achievement get.
  - Can be "clicking", "subtle", "uplifting" or the path to a wav/ogg file. 
  - It can also be None, and thus won't produce a sound.
- `importance` (int/float, default is 1) : The higher the number is, the longer the achievement will stay on screen.

For example :
```python
from ursina import *
from UrsinaAchievements import create_achievement

app = Ursina()

Sky()
do = False

def cond():
  global do
  return do
  
create_achievement("Bubbles.", cond, "bubbles.png", "subtle")

def setdo():
  global do
  do = True
  
invoke(setdo, delay=2)

app.run()
```

## Achievement look tweaking
You can also customize the look of the achievement by importing the `Achievement` class and tweaking the following attributes :
- `Achievement.achievement_color`
- `Achievement.text_color`
- `Achievement.icon_color`

All of those correspond to a 3-value tuple of integers.

## Features & Todos
- [x] Popups at the bottom-right corner of the screen
  - Contains an achievement name
  - An icon
- [x] Every frame, each function given for the argument check is tested ; achievement is given if the function tests true
- [x] All gotten achievements are stored in a JSON file
- [ ] An HTML file is generated with every achievement you got
- [ ] The function used for creating the achievements can be used as a decorator
