# *taxi*

---

*taxi* is an opinionated Axidraw GUI. It is named this way because it opines that the [*Axi*draw](https://axidraw.com) is the best plotter, and it is best operated with a *t*ouch screen. Also, "saxi" is probably a better name but [is not available](https://github.com/nornagon/saxi).

Here are a few things *taxi* feels strongly about:
* Your main computer is best used for creating artwork. Let a [Raspberry Pi](https://www.raspberrypi.org) run the plotter.
* After experimenting with [a classical GUI which wouldn't fit on small screens](https://github.com/abey79/axigui), [a frankenstein CLI with remote capabilities](https://github.com/abey79/plottertools/tree/main/raxicli), and [an outright crazy TUI-MIDI-controller hybrid](https://github.com/abey79/plottertools/tree/main/aximix), the now-obvious path forward is a simple, touch-screen-based interface. 
* *taxi* doesn't handle the scaling, layout, optimisation, and previsualisation of your SVGs, because your workflow should. Use [*vpype*](https://github.com/abey79/vpype) and/or [*vsketch*](https://github.com/abey79/vsketch) if it doesn't.
* *taxi* is not web-based (it's based on [Kivy](https://kivy.org/) and runs locally). This choice may or may not be rational.


## Features

* Touch-screen-based UI
* Easy controls for pen up/down position setup
* First-class support of multi-pen plots  
* End-of-plot notification support (currently through Home Assistant only)

![](https://i.imgur.com/s8Yrwld.gif)

## Installation

*Note*: because of its dependencies, *taxi* is currently rather tricky to install on a Raspberry Pi (which, I will agree, is unfortunate). This installation procedure has been tested with Raspbian Testing.

A number of dependencies are required:

```
$ sudo apt-get install python3.9 "python3-pyside2.*" python3-shapely python3-pil python3-numpy python3-scipy python3-serial libsdl2-dev 
```

Using a virtual environment is mandatory *BUT* the global environment's PySide2 must be used as it is not available from PyPI. The virtual environment must thus allow reuse of package from the global environment:

```
$ python3 -m venv taxi-venv --system-site-packages
$ source taxi-venv/bin/activate
```

In my setup at least and for some odd reason, PySide2 *still* causes issue. Although it is properly working, it is not seen by `pip`:

```
$ python -c "import PySide2;print(PySide2.__version__)"
5.15.2
$ pip show PySide2
WARNING: Package(s) not found: PySide2
```

If you are lucky and the above command doesn't fail on your setup, you might have a chance at running:

```
$ pip install git+https://github.com/plottertools/taxi#egg=taxi
```

Otherwise, you're in for a ride with the next few steps. First, all of *vpype*'s dependencies must be installed "by hand" (except for PySide2):

```
$ pip install attrs cachetools click click-plugins glcontext matplotlib moderngl multiprocess pnoise setuptools svgelements svgwrite toml
```

*vpype* can then be installed:

```
$ pip install --no-deps vpype
```

Now *taxi*'s dependencies must be installed:

```
$ pip install kivy==2.0.0 watchgod aiohttp
$ pip install https://cdn.evilmadscientist.com/dl/ad/public/AxiDraw_API.zip
```

Finally, *taxi* can be installed:

```
$ pip install --no-deps git+https://github.com/plottertools/taxi#egg=taxi
```

## License

See [LICENSE](LICENSE)