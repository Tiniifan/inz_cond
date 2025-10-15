# Inazuma Condition Parser

`inz_cond` is a **Python tool** that converts the internal condition data used in Level-5 Nintendo 3DS games into **human-readable code**.  
These conditions are used by the game engine to determine when characters, talk events, quests, or other in-game elements should appear.

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

## Supported Condition Types

Currently supported condition types:

* `SubPhase`
* `BitFlag`
* `TeamFlag`
* `HaveItem`

The following functions are referenced in the generated code:

| Function                     | Game Command (CMND)          | Description                                                                                                                                                         |
| ---------------------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `getGameSubPhase()`          | `CMND_GET_SUB_PHASE()`       | Returns the current game sub-phase.                                                                                                                                 |
| `getGlobalBitFlag(flag)`     | `CMND_GET_GLOBAL_BIT_FLAG()` | Returns true or false depending on whether the given bit flag is active.                                                                                            |
| `getTeamBitFlag(flag)`       | `Doesn't exist`              | Returns true or false depending on whether the team bit flag is active.                                                                                             |
| `isHaveItem(itemID)`         | `CMND_IS_HAVE_ITEM()`        | Returns true or false depending on whether the item is owned.                                                                                                       |

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

## Graphical User Interface (GUI)

A graphical version of the tool is available to easily decode and visualize the condition code.

You can start the GUI using this command

```bash
python level5_condition_gui.py
```

<img width="1390" height="823" alt="image" src="https://github.com/user-attachments/assets/0df56417-f4a3-430d-8251-5e09825cbf1d" />

Please note: you need PyQt6 to use this version

## Special Thanks

* [n123git](https://github.com/n123git) for giving me detailed explanations about the format. I recommend [his version of condition parser optimize for ykw](https://github.com/n123git/yw-cond)

## Notes
* It's not possible to convert code to base64 at this time.
* The tool can make mistakes, the logic was written by a human :)
* This tool is intended for research and educational purposes
* It does not modify or execute any game content.
* The generated code is fictitious, it's just a representation of how the engine works.
