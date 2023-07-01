# README

## Prerequisites
You should have the following tools available/installed:
- XCC Utilities (includes the following:)
    - XCC AV Player
    - XCC Editor
    - XCC MIX Editor
    - XCC Mixer
    - XCC TMP Editor
- Text Editor, e.g. Notepad++, VSCode, etc
- Photo editor, e.g. Photoshop

## Installation
- TBD

## Development
### New Tiles
The easiest way to create a new tile is to use an existing tile as a base/template.
This will help you avoid errors when making your new tile.  

##### Create the Tile
1. Select an existing tile to base your new tile on. 
    - It should be similar in terrain type to what you intend to create, e.g. a ground
        tile, a cliff tile, a shore tile.
    - You also need to pick the game and theater.  For example, if you want to create a
        new Desert tile for Yuri's Revenge, select a tile from `Development Files/YR/Desert`.

2. Open `XCC TMP Editor` and open your tile in the editor.  In the **Open** dialog you may
    need to show "All Files" to see the available tile files in the folder.

3. The file you chose may consist of one or more individual tiles.  Select an individual
    tile by choosing a row on the left-side of the screen.  The chosen tile will be 
    highlighted in the preview pane on the right-side. Press `Ctrl + C`.

4. Open your photo editor and create a new file.  The size of the new image should match
    the tile size, 60 pixels width x 30 pixels height.

5. In the new file, paste what is on your clipboard.  You should now be able to edit
    your chosen tile.

6. When you are done editing, select your entire image using the mask tool.  Copy it.

7. Back in `XCC TMP Editor`, select the same row you copied from and hit `Ctrl + V` to
    paste.  Your edits should appear in the right-side preview.

8. Save the file to a new filename.
    - The filename you choose is significant. Any tile used in Final Alert map editor is
        actually part of a tileset which could contain multiple tile files.  The tileset
        is identified by a number and a basename. Format your new tile filename like so:
        `<basename><id>.<extension>`
        - `basename`: This should be a short descriptive name for your new tileset.
        - `id`: This is a two digit number that uniquely identifies this tile in the tileset.
            This is a different number from the tileset ID.  If this is the first tile in your
            set, choose `01`
        - `extension`: The file extension is related to the theater you chose.  Use the same
            file extension as the file you opened.

    - Your filename might be something like `sand01.des`.  Be sure that your chosen
    `basename` does not conflict with an existing tileset! Also use a filename
    (`basename` + `id`) that is no longer than 8 characters!  You should save the file
    in the same folder as the original file you opened.

#### Integrate Tile with Final Alert 2
1. Package all the files in the folder where your new tile file is saved
    ("theater folder") into a `.mix` file.
    1. Open `XCC Mix Editor`.
    2. Click `New...` and give your mix a name depending on your chosen theater:
        - Urban: `expandmd13.mix`
        - Temperate: `expandmd14.mix`
        - Snow: `expandmd15.mix`
        - NewUrban: `expandmd16.mix`
        - Lunar: `expandmd17.mix`
        - Desert: `expandmd18.mix`
    3. Drag all the files in the theater folder to the `XCC Mix Editor` window.
    4. Click `Save`.
2. Move the new `.mix` file into the RA2YR game folder, overwriting one that's there if
    necessary.
3. Edit the ini file in the theater folder to include a new tileset for your new tile.
    Each tileset gets its own ini section.  Here is an example section:

    ```ini
    [TileSet0208]
    SetName = *Sand Fixes Z*
    FileName = sand
    TilesInSet = 1
    LowRadarColor = 60,40,0
    HighRadarColor = 80,50,0
    AllowTiberium = true
    ```
    Note:
    - Surround the `SetName` with asterisks. This is an RA2TX convention to distinguish
        new tiles from those in the base game.
    - The `SetName` and `FileName` must be unique for the ini file.
    - `FileName` should match the `basename` (i.e. not including the `id`/`extension`) of your tile file.
    - The ini header must start with `TileSet` and end with a 4 digit number. The number
      should be the next available number for the ini file.
    - `TilesInSet` should be set to the number of files you made for this set.
4. Copy the updated ini from the theater folder to the RA2YR game folder.
5. Restart FA2 and start using your new tile.
