# MLPCCG OCTGN

This is the current updated game definition source code for MLPCCG on OCTGN. The Master branch is used for testing builds while the Live branch is used for hosting the game's current build.

If you are looking for patch notes of official updates for the game, please visit http://www.octgngames.com/mlpccg

If you find any bug/issues with the game, please report it in the issue section or in the discord group (https://discord.gg/QkGx4FT)

Contributors are welcomed but any user-submitted code/changes will be reviewed in the Master branch before being merged into the Live branch.

### Development
Want to contribute? Great! I will give a brief description of the files used in the inner workings of the game definition below. For more detailed information, I recommend visiting [OCTGN Documentation wiki.](https://github.com/octgn/OCTGN/wiki)

Alright, these are the few files that is responsible for all the game code for MLPCCG OCTGN:

| File | Description |
| ------ | ------ |
| **definition**.xml | It is responsible for all of the data and properties that OCTGN requires to locate the game on a feed, play the game, or use the deck editor |
| **actions**.py | It contains all the code for every action in the game |
| **events**.py | It contains a unique code that will only triggers if a certain action has been performed |
| **proxydef**.xml | It is responsible for defining all the generation of proxy cards |

Currently all of the py files are using OCTGN Python 3.1.0.2 API. Documentation of that API can be found [here](https://github.com/octgn/OCTGN/wiki/OCTGN-Python-3.1.0.2-API-Reference).

Other than that, I have some tips too that can help make developing on OCTGN easier. Tip one, do you know you can launch OCTGN in dev mode by adding **-x** at the end of the Target field under the exe properties? This allows you to see what functions are triggering and reload your script without restarting the game!

I will expand this more if necessary. Nevertheless, thank you for your contribution and I hope to see what you can do to improve the game!