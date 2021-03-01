import copy
import io
import math
import os
import pathlib
import sys
import threading
from time import sleep
from typing import Mapping, Optional

import vpype as vp
from kivy.app import App
from kivy.clock import Clock, ClockEvent
from kivy.logger import Logger
from kivy.properties import (
    BooleanProperty,
    ConfigParserProperty,
    DictProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.stacklayout import StackLayout
from kivy.uix.togglebutton import ToggleButton

if len(sys.argv) > 1 and sys.argv[1] == "stub":
    from .axy.stub import axy
else:
    from .axy.axidraw import axy


class FileChooserButton(Button):
    path = ObjectProperty()


class FileListLayout(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "lr-tb"

        for path in sorted(
            pathlib.Path(App.get_running_app().config.get("taxi", "svg_dir")).iterdir(),
            key=os.path.getmtime,
            reverse=True,
        ):
            if path.is_file() and path.name.lower().endswith(".svg"):
                self.add_path(path)

    def add_path(self, path: pathlib.Path) -> None:
        self.add_widget(FileChooserButton(text=path.name, path=path))


class LayerToggleButton(ToggleButton):
    layer_id = NumericProperty()


class LayerListLayout(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "lr-tb"
        App.get_running_app().layer_list = self

    def populate(self, doc: vp.Document) -> None:
        self.clear_widgets()
        if doc is not None:
            for layer_id in sorted(doc.layers):
                w = LayerToggleButton(text=str(layer_id), state="down", layer_id=layer_id)
                self.add_widget(w)

    def select_all(self):
        for child in self.children:
            child.state = "down"

    def deselect_all(self):
        for child in self.children:
            child.state = "normal"


class FileChooserScreen(Screen):
    pass


class ParamsScreen(Screen):
    pass


class LayersScreen(Screen):
    pass


class PlottingScreen(Screen):
    pass


# noinspection PyArgumentList
class TaxiApp(App):
    pen_pos_up = ConfigParserProperty(60, "axidraw", "pen_pos_up", "app")
    pen_pos_down = ConfigParserProperty(40, "axidraw", "pen_pos_down", "app")
    speed = ConfigParserProperty(25, "axidraw", "speed_pendown", "app")
    accel = ConfigParserProperty(75, "axidraw", "accel", "app")
    const_speed = ConfigParserProperty(False, "axidraw", "const_speed", "app")
    rotate = ConfigParserProperty(False, "axidraw", "rotate", "app")
    path = ObjectProperty()
    layer_list = ObjectProperty()
    layer_visibility = DictProperty()
    plot_running = BooleanProperty()
    page_format = StringProperty("n/a")

    def __init__(self):
        super().__init__()
        self.document: Optional[vp.Document] = None
        self._plot_thread: Optional[threading.Thread] = None
        self._clock: Optional[ClockEvent] = None
        self.plot_running = False

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(FileChooserScreen(name="file"))
        sm.add_widget(ParamsScreen(name="params"))
        sm.add_widget(LayersScreen(name="layers"))
        sm.add_widget(PlottingScreen(name="plot"))

        return sm

    def get_application_config(self, *args, **kwargs):
        return super().get_application_config("~/.taxi.ini")

    def build_config(self, config):
        config.setdefaults(
            "axidraw",
            {
                "speed_pendown": 25,
                "speed_penup": 75,
                "accel": 75,
                "pen_pos_down": 40,
                "pen_pos_up": 60,
                "pen_rate_lower": 50,
                "pen_rate_raise": 75,
                "pen_delay_down": 0,
                "pen_delay_up": 0,
                "const_speed": False,
                "model": 2,
                "port": "/dev/tty.usb",
            },
        )
        config.setdefaults(
            "taxi",
            {
                "svg_dir": os.path.expanduser("~/.taxi_svgs"),
                "rotate": False,
            },
        )

    def build_settings(self, settings):
        settings.add_json_panel(
            "Taxi", self.config, str(pathlib.Path(__file__).parent / "settings.json")
        )

    def load_svg(self) -> None:
        self.document = vp.read_multilayer_svg(str(self.path), quantization=0.1)
        self.layer_list.populate(self.document)

        # create page size label
        page_size = self.document.page_size
        if page_size[0] < page_size[1]:
            landscape = False
        else:
            page_size = tuple(reversed(page_size))
            landscape = True

        format_name = ""
        for name, sz in vp.PAGE_SIZES.items():
            if math.isclose(sz[0], page_size[0], abs_tol=0.01) and math.isclose(
                sz[1], page_size[1], abs_tol=0.01
            ):
                format_name = name
                break
        s = (
            f"{self.document.page_size[0] / 96 * 25.4:.1f}x"
            f"{self.document.page_size[1] / 96 * 25.4:.1f}mm"
        )
        if format_name != "":
            s += f" ({format_name} {'landscape' if landscape else'portrait'})"
        self.page_format = s

    def apply_axy_options(self):
        axy.set_option(
            "speed_pendown", round(float(self.config.get("axidraw", "speed_pendown")))
        )
        axy.set_option("speed_penup", round(float(self.config.get("axidraw", "speed_penup"))))
        axy.set_option("accel", round(float(self.config.get("axidraw", "accel"))))
        axy.set_option(
            "pen_pos_down", round(float(self.config.get("axidraw", "pen_pos_down")))
        )
        axy.set_option("pen_pos_up", round(float(self.config.get("axidraw", "pen_pos_up"))))
        axy.set_option(
            "pen_rate_lower", round(float(self.config.get("axidraw", "pen_rate_lower")))
        )
        axy.set_option(
            "pen_rate_raise", round(float(self.config.get("axidraw", "pen_rate_raise")))
        )
        axy.set_option(
            "pen_delay_down", round(float(self.config.get("axidraw", "pen_delay_down")))
        )
        axy.set_option(
            "pen_delay_up", round(float(self.config.get("axidraw", "pen_delay_up")))
        )
        axy.set_option("const_speed", bool(self.config.get("axidraw", "const_speed")))
        axy.set_option("model", round(float(self.config.get("axidraw", "model"))))
        axy.set_option("port", str(self.config.get("axidraw", "port")))

        # default option
        axy.set_option("auto_rotate", False)

    def pen_up(self):
        self.apply_axy_options()
        axy.pen_up()

    def pen_down(self):
        self.apply_axy_options()
        axy.pen_down()

    def motor_off(self):
        Logger.info("disabling XY motors")
        self.apply_axy_options()
        axy.shutdown()

    def on_start(self):
        self.motor_off()

    def on_stop(self):
        self.motor_off()

    def start_plot(self):
        self.apply_axy_options()
        self._plot_thread = threading.Thread(
            target=self.run_plot, args=(self.document, self.rotate, self.layer_visibility)
        )

        Logger.info("starting plot")
        self.plot_running = True
        self._plot_thread.start()
        self._clock = Clock.schedule_interval(self.check_plot, 0.1)

    # noinspection PyUnusedLocal
    def check_plot(self, dt):
        if self._plot_thread is not None and not self._plot_thread.is_alive():
            Logger.info("plot completed")
            self._plot_thread = None
            self._clock.cancel()
            self.plot_running = False

    @staticmethod
    def run_plot(
        document: vp.Document,
        rotate: bool,
        layer_visibility: Mapping[int, bool],
    ):
        """caution: axy must be pre-configured!"""
        if document is None:
            Logger.warning("self.document is None")
            return

        doc = document.empty_copy()

        for layer_id in document.layers:
            if layer_visibility.get(layer_id, True):
                Logger.info(f"adding layer {layer_id}")
                doc.layers[layer_id] = document.layers[layer_id]

        if rotate:
            Logger.info("rotating SVG")
            doc = copy.deepcopy(doc)
            doc.rotate(-math.pi / 2)
            doc.translate(0, doc.page_size[1])
            doc.page_size = tuple(reversed(doc.page_size))

        # convert to SVG
        str_io = io.StringIO()
        vp.write_svg(str_io, doc)
        svg = str_io.getvalue()

        # plot
        axy.plot_svg(svg)


if __name__ == "__main__":
    TaxiApp().run()
