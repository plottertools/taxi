# *taxi*

---

*taxi* is an opinionated Axidraw GUI. Here are a few things *taxi* feels strongly about:
* The [Axidraw](https://axidraw.com) is the best plotter. *taxi* works ony with the Axidraw, and that's where the *axi* part of its name comes from.
* Your main computer is best used for creating artwork. Let a [Raspberry Pi](https://www.raspberrypi.org) run the plotter.
* After experimenting with [a classical GUI which wouldn't fit on small screens](https://github.com/abey79/axigui), [a frankenstein CLI with remote capabilities](https://github.com/abey79/plottertools/tree/main/raxicli), and [an outright crazy TUI-MIDI-controller hybrid](https://github.com/abey79/plottertools/tree/main/aximix), the now-obvious path forward is a touch-screen-based interface  (thus the *t* in the name – also [saxi](https://github.com/nornagon/saxi) was already taken).
* *taxi* doesn't handle the scaling, layout, optimisation, and previsualisation of your SVGs, because your workflow should. Use [*vpype*](https://github.com/abey79/vpype) and/or [*vsketch*](https://github.com/abey79/vsketch) if it doesn't.
* *taxi* is not web-based (it's based on [Kivy](https://kivy.org/) and runs locally). This choice may or may not be rational.


## Features

* Touch-screen-based UI
* Easy controls for pen up/down position setup
* First-class support of multi-pen plots  
* End-of-plot notification support (currently through Home Assistant only)

![](https://i.imgur.com/s8Yrwld.gif)

## Installation

*Note*: these instructions assumes a Rasberry Pi 4 with Raspbian. YMMV if your setup differs.

A number of dependencies must be installed:

```
$ sudo apt-get install python3.9 python3-dev python3-shapely python3-pil python3-numpy python3-scipy python3-serial python3-pygame libsdl2-dev 
```

Using a virtual environment is mandatory *BUT* using system packages makes the installation easier. Don't even try to skip this step:

```
$ python3 -m venv taxi-venv --system-site-packages
```

Activate the virtual environment (this must be done for each new terminal session):

```
$ source taxi-venv/bin/activate
```

Install *taxi*:

```
$ pip install git+https://github.com/plottertools/taxi#egg=taxi
```

## License

See [LICENSE](LICENSE)
