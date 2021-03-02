# *taxi*

---

*taxi* is an opinionated Axidraw GUI. It is named this way because it opines that the [*Axi*draw](https://axidraw.com) is the best plotter, and it is best operated with a *t*ouch screen. Also, "saxi" is probably a better name but [is not available](https://github.com/nornagon/saxi).

Here are a few things *taxi* feels strongly about:
* Your main computer is best used for creating artwork. Let a [Raspberry Pi](https://www.raspberrypi.org) run the plotter.
* After experimenting with [a classical GUI which wouldn't fit on small screens](https://github.com/abey79/axigui), [a frankenstein CLI with remote capabilities](https://github.com/abey79/plottertools/tree/main/raxicli), and [an outright crazy TUI-MIDI-controller hybrid](https://github.com/abey79/plottertools/tree/main/aximix), the now-obvious path forward is a simple, touch-screen-based interface. 
* *taxi* doesn't handle the scaling, layout, optimisation, and previsualisation of your SVGs, because your workflow should. Use [*vpype*](https://github.com/abey79/vpype) and/or [*vsketch*](https://github.com/abey79/vsketch) if it doesn't.


## Features

* Touch-screen-based UI
* Easy controls for pen up/down position setup
* End-of-plot notification support (currently through Home Assistant only)