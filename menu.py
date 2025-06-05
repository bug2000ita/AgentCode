print(r"""
---------------------------------------------------------------
|                         thermo scientific                   |
---------------------------------------------------------------

Start
 ├── Session Creation
Preparation
 ├── Session Setup
 ├── Square Selection
 ├── Image Selection
 ├── Template Definition
Execution
 └── Automated Acquisition

---------------------------------------------------------------
|                           Session                            |
|-------------------------------------------------------------|
| General session settings                                    |
|-------------------------------------------------------------|
| Session name: giovanni.mariotta_20240603_101250_59         |
| Grid type:  ○ Holey carbon  ● Lacey carbon  ○ Holey gold    |
| Geometry type:  ● Square  ○ Hexagonal  ○ Unknown            |
| Session type:  ● Automated  ○ Manual                        |
| Acquisition Mode:  ● Accurate  ○ Faster                     |
| Tilted Acquisition: (checkbox, not visible)                 |
|-------------------------------------------------------------|
| Output settings                                             |
|-------------------------------------------------------------|
| Image format:  ● MRC  ○ TIFF                                |
| Output folder:                                              |
|   C:\\Users\\giovanni.mariotta\\OneDrive - Thermo Fisher S... |
|   [x] Set as default storage folder                         |
|-------------------------------------------------------------|
| Email settings                                              |
| Email recipients:                                           |
|   [                    ]  [Test]                            |
|-------------------------------------------------------------|
|                        [ Apply ]                            |
---------------------------------------------------------------

Messages
---------------------------------------------------------------
Filtering:  [0 Error(s)]  [0 Notification(s)]

Status
---------------------------------------------------------------
EPU Assistant
  ● llama3
  ○ llama3Multi

[ Ask To AI Assistant ]  [ ] Content-Aware
""")

input("Press Enter to start the snake game...")

from snake import main
main()
