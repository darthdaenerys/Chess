# Chess Application

This is a chess GUI built with the Pygame library. You can use it as a standalone playable. Read the guide below.

![Alt text](ezgif-5-7c2bb73e30.gif)

## Usage

To install, clone this repository to your local machine git clone `https://github.com/darthdaenerys/Chess.git`
Change to cloned directory `cd Chess`

Install necessary requirements `pip install -r requirements.txt`.

If you ever need to remove a module for any reason, use the command `pip uninstall <module-name>`

Run the `main.py` file.

## Gameplay

The game supports Player vs. Player mode(currently). In PvP, player can choose to play as either Black or White. You can modify the settings in the `settings.json` file. More instructions cann be found below.

## Feature List

- You can add your own custom background.
- Change the tile colour for your board.
- Change the sound theme(Feature currently not available as a setting).
- Helper for all valid moves. This can be turned off too in the settings.

## Instructions

- **Custom background** - Move your background image inside the `background` folder. Then while running the application change your background theme using `B`.
- **Creating Custom background(Recommended)** - I have provided a `background.psd` file. Open the file in adobe photoshop and add your background to a new layer and delete the sparkle background. Save it as a `.jpg` file in the `background` folder.
- **Custom Tile Theme** - Open the `config.py` file in your editor and create a new theme object from `Theme` class. You may need to look at the parameters given to it in the `theme.py` file. After that add your theme in the `self.themes` list just below it. Now you can switch to your custom theme using `T` while running the application.
- **Creating Custom background(Recommended)** - I have also provided a `chessboard.psd` file. Open the file in adobe photoshop and add your color for the dark squares and light squares as mentioned in the layers panel. If you like the look copy-paste the RGB value or HEX value inside the theme object as parameters.

### Key Bindings

|Key|Action|
|:-:|:-:|
|`S`|Flips side|
|`T`|Changes Tile Theme|
|`B`|Changes Background cover|
|`R`|Restart|

## Contribution

The project is under active development. Pull requests are welcome. You can submit any request you want, or report any bug you encounter by opening an issue. Feel free to come up with ideas whether it is about coding practices or game mechanics.

Here are some suggestions of contributions:

- Check the opened issues, there are bugs that could be fixed or enhancement waiting for implementation.
- Contributions for sound effects or new soundtracks would be really appreciated.
