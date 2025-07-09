from typing import Union
import logging

from flask import Blueprint

from RHAPI import RHAPI
from RHUI import UIField, UIFieldType, UIFieldSelectOption
from Database import Pilot, SavedRaceLap
from eventmanager import Evt



import colorsys


DEBUG=True
logger = logging.getLogger(__name__)


def generate_high_contrast_palette(n, saturation=0.7, lightness=0.5):
    """
    Generate a list of n high-contrast hex color values using HSL color space.

    Args:
        n (int): Number of colors to generate.
        saturation (float): Saturation level (0 to 1).
        lightness (float): Lightness level (0 to 1).

    Returns:
        List[str]: List of hex color strings.
    """
    colors = []
    for i in range(n):
        hue = i / n  # Evenly spaced hues
        r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
        hex_color = '#{0:02x}{1:02x}{2:02x}'.format(int(r * 255), int(g * 255), int(b * 255))
        colors.append(hex_color)
    return colors

# Example usage:
#palette = generate_high_contrast_palette(10)
#print(palette)

def set_pilot_colours(args: dict) -> None:
    rhapi: Union[RHAPI, None] = args.get("rhapi", None)
    if rhapi is not None:
        logger.info("Setting high contrast pilot colours")
        pilots = rhapi.db.pilots
        npilots = len(pilots)
        hex_codes=generate_high_contrast_palette(npilots)
        if DEBUG:
           logger.info(hex_codes)
        for i in range(npilots):
            rhapi.db.pilot_alter(pilots[i].id, color = hex_codes[i])
            #pilots[i].color=hex_codes[i]
            if DEBUG:
               logger.info(f"Setting pilot {pilots[i].callsign} to color {hex_codes[i]}")





def init_plugin(args: dict) -> None:
    logger.info("Pilot Colours Plugin initialised")


def initialize(rhapi: RHAPI) -> None:
    # Event Startup creates the dataframes
    rhapi.events.on(Evt.STARTUP, init_plugin, default_args={"rhapi": rhapi})
    rhapi.ui.register_panel("pilot_colours_set", "Pilot Colour Format", "format")
    rhapi.ui.register_quickbutton(
        "pilot_colours_set",
        "pilot_colours_set_go",
        "Set High Contrast Pilot Colours",
        set_pilot_colours,
        {"rhapi": rhapi},
    )


#    erow_height_field = UIField(
#        name="event_plots_row_height",
#        label="Row Height",
#        field_type=UIFieldType.NUMBER,
#        desc=("This is the height of each row in the plots "),
#        value=100)
#    rhapi.fields.register_option(erow_height_field, "event_plots_set")
