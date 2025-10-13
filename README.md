# Level5 Condition Converter

`level5_condition` is a **Python tool** that converts the internal condition data used in Level-5 Nintendo 3DS games into **human-readable code**.
These conditions are used by the game engine to determine when characters, talk events, quests, or other in-game elements should appear.

## Overview

Level-5 condition data is stored as **Base64-encoded binary**.
Once decoded, the data represents a **hexadecimal byte sequence**, formatted in **big-endian** order.

Conversion process:

```
Base64 → Hexadecimal → Human-readable code
```

Base64:

```
AAAAAA8FNZjuS0cAAQAyBfZ9VHg=
```

Hexadecimal:

```
000000000f053598ee4b470001003205f67d5478
```

Human-readable code (C code):

```c
bool condition()
{
    bool result = false;
    int variable0 = 100040020;
    if (getGameSubPhase() >= variable0) {
        result = true;
    }
    return result;
}
```

## Supported Condition Types

Currently supported condition types:

* `SubPhase`
* `BitFlag`

The following functions are referenced in the generated code:

| Function                     | Game Command (CMND)          | Description                                                                                                                                                         |
| ---------------------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `getGameSubPhase()`          | `CMND_GET_SUB_PHASE()`       | Returns the current game sub-phase.                                                                                                                                 |
| `getLastGlobalBitFlag()`     | *(simulated function)*       | Custom function based on observed behavior: returns the last initialized bit flag (for example, if bit 1 and bit 10 are true, the last initialized bit flag is 10). |
| `getGlobalBitFlag(flag)` | `CMND_GET_GLOBAL_BIT_FLAG()` | Returns true or false depending on whether the given bit flag is active.                                                                                            |

## Game Compatibility
- **Inazuma Eleven Go** ✅

## Supported Languages

* **C** (default)
* **Squirrel**

## Command Line Usage

### Generate C code (default)

```bash
python level5_condition.py -d AAAAAA8FNZjuS0cAAQAyBfZ9VHg=
```

### Force C generation

```bash
python level5_condition.py -d AAAAAA8FNZjuS0cAAQAyBfZ9VHg= -c
```

### Generate Squirrel code

```bash
python level5_condition.py -d AAAAAA8FNZjuS0cAAQAyBfZ9VHg= -sq
```

## Graphical User Interface (GUI)

A graphical version of the tool is available to easily decode and visualize the condition code.

<img width="1394" height="826" alt="image" src="https://github.com/user-attachments/assets/7b4e6f0c-76a3-4b4c-9451-862e2d50d22f" />

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

```bash
python level5_condition.py -d AAAAAA8FNZjuS0cAAQAyBfZ9VHg=
```

### GUI

1. Run the GUI:

   ```bash
   python level5_condition_gui.py
   ```
2. Paste the Base64 condition into the right text box.
3. Click **Convert to Code**.
4. Use **Clear** to reset both containers.

## Notes

* It's not possible to convert code to base64 at this time.
* The tool can make mistakes, the logic was written by a human :)
* This tool is intended for research and educational purposes
* It does not modify or execute any game content.
* The generated code is fictitious, it's just a representation of how the engine works.
