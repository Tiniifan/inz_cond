# Inazuma Condition Parser

`inz_cond` is a **Python tool** that interprets the internal condition data used in Level-5 Nintendo 3DS games.  
These conditions determine when characters, talk events, quests, or other in-game elements should appear.

The tool can do:

* Converting **Base64-encoded condition data** into editable code.
* Converting **human-readable code back into Base64** for use in the game.

## Overview

Level-5 condition data is stored as **Base64-encoded binary**.
Once decoded, the data represents a **hexadecimal byte sequence**.

Conversion process:

```
Base64 → Hexadecimal → Human-readable code
```

Base64:

```
AAAAAA8FNZjuS0cAAQAyBfZ9Sng=
```

Hexadecimal:

```
00 00 00 00 0F 05 35 98 EE 4B 47 00 01 00 32 05 F6 7D 4A 78
```

Human-readable code (C code):

```c
bool condition()
{
    bool result = false;

    if (getGameSubPhase() == 100040020) {
        result = true;
    }

    return result;
}
```

## Supported Functions

| Function (C)                 | Function (Squirrel)                | Description                                                                                  |
| ---------------------------- | ---------------------------------- | -------------------------------------------------------------------------------------------- |
| `GetSubPhase()`              | `CMND_GET_SUB_PHASE()`             | Returns the current sub-phase of the game.                                                   |
| `GetPhase()`                 | `CMND_GET_PHASE()`                 | Returns the current main phase of the game.                                                  |
| `GetTRouteFlag(flagID)`      | `CMND_GET_T_ROUTE_FLAG()`          | Returns true or false depending on whether the specified route flag is active.               |
| `GetTempMapByteFlag(flagID)` | `CMND_GET_TEMP_MAP_BYTE_FLAG()`    | Returns the temporary map byte flag value for the given ID.                                  |
| `GetTempByteFlag(flagID)`    | `CMND_GET_TEMP_BYTE_FLAG()`        | Returns the temporary byte flag value for the given ID.                                      |
| `GetGlobalCharaMetFlag(id)`  | `CMND_GET_GLOBAL_CHARA_MET_FLAG()` | Returns true or false depending on whether the specified character has been met globally.    |
| `GetGlobalBitFlag(flagID)`   | `CMND_GET_GLOBAL_BIT_FLAG()`       | Returns true or false depending on whether the specified global bit flag is set.             |
| `GetTempMapBitFlag(flagID)`  | `CMND_GET_TEMP_MAP_BIT_FLAG()`     | Returns true or false depending on whether the specified temporary map bit flag is active.   |
| `GetTempBitFlag(flagID)`     | `CMND_GET_TEMP_BIT_FLAG()`         | Returns true or false depending on whether the specified temporary bit flag is active.       |
| `GetGlobalTBoxFlag(flagID)`  | `CMND_GET_GLOBAL_T_BOX_FLAG()`     | Returns true or false depending on whether the specified global treasure box flag is active. |
| `IsHaveItem(itemID)`         | `CMND_IS_HAVE_ITEM()`              | Returns true or false depending on whether the player owns the specified item.               |
| `CheckShopOpen(shopID)`      | `CMND_CHECK_SHOP_OPEN()`           | Returns true or false depending on whether the specified shop is currently open.             |
| `GetGameVersion()`           | `CMND_GET_GAME_VERSION()`          | Returns the current game version identifier.                                                 |
| `GetFrameChapter()`          | `CMND_GET_FRAME_CHAPTER()`         | Returns the current frame chapter number of the game.                                        |
| `GetChapter()`               | `CMND_GET_CHAPTER()`               | Returns the current chapter number of the game.                                              |

## Game Compatibility
- **Inazuma Eleven Go** ✅

## Supported Languages

* **C** (default)
* **Squirrel**

## Installation

### 1. Clone or Download the Source Code

### 2. Install dependencies

There is no dependency for the CLI.  

The only dependency required for the GUI is **PyQt6**.

```bash
pip install PyQt6
```

or

```bash
pip install -r requirements.txt
```

## Example Usage

### Command Line

#### Generate C code (default)

```bash
python inz_cond_cmd.py -d AAAAAA8FNZjuS0cAAQAyBfZ9Sng=
```

#### Force C generation

```bash
python inz_cond_cmd.py -d AAAAAA8FNZjuS0cAAQAyBfZ9Sng= -c
```

#### Generate Squirrel code

```bash
python inz_cond_cmd.py -d AAAAAA8FNZjuS0cAAQAyBfZ9Sng= -sq
```

#### Generate Base64

You cannot convert code to base64 with the CMD version.

## Graphical User Interface (GUI)

A graphical version of the tool is available to easily decode and visualize the condition code.

Compared to the command-line version, the GUI offers several additional features:

* A simple and intuitive interface to convert Base64 strings into readable code, and perform the reverse operation just as easily.
* Syntax highlighting based on the selected language, making the condition code easier to read and analyze.
* The ability to set and modify parameters to simulate and test code behavior directly within the interface.
* Support for `.inzcond` files from the **template** folder, providing built-in guidance and examples for understanding condition structures.

You can start the GUI using this command

```bash
python level5_condition_gui.py
```

<img width="1593" height="925" alt="image" src="https://github.com/user-attachments/assets/720d9efd-262b-47fa-9c36-7207c3f6c099" />

Please note: you need PyQt6 to use this version

## Special Thanks

* [n123git](https://github.com/n123git) for giving me detailed explanations about the format. I recommend [his version of condition parser optimized for ykw](https://github.com/n123git/yw-cond)

## Notes
* The tool can make mistakes, the logic was written by a human :)
* This tool is intended for research and educational purposes.
* It does not modify or execute any game content.
* The generated code is fictitious, it's just a representation of how the engine works.
