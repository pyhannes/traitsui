#  Copyright (c) 2005-2020, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#
from traitsui.wx.range_editor import (
    LargeRangeSliderEditor,
    LogRangeSliderEditor,
    RangeTextEditor,
    SimpleSliderEditor,
)

from traitsui.testing.tester import command, locator
from traitsui.testing.tester._ui_tester_registry.wx import (
    _interaction_helpers,
    _registry_helper
)


class LocatedTextbox:
    """ Wrapper class for a located Textbox in Wx.

    Parameters
    ----------
    textbox : Instance of wx.TextCtrl
    """

    def __init__(self, textbox):
        self.textbox = textbox

    @classmethod
    def register(cls, registry):
        """ Class method to register interactions on a LocatedTextbox for the
        given registry.

        If there are any conflicts, an error will occur.

        Parameters
        ----------
        registry : TargetRegistry
            The registry being registered to.
        """
        _registry_helper.register_editable_textbox_handlers(
            registry=registry,
            target_class=cls,
            widget_getter=lambda wrapper: wrapper._target.textbox,
        )


class LocatedSlider:
    """ Wrapper class for a located Textbox in Wx.

    Parameters
    ----------
    slider : Instance of traitsui.wx.helper.Slider (wx.Slider)
    """

    def __init__(self, slider):
        self.slider = slider

    @classmethod
    def register(cls, registry):
        """ Class method to register interactions on a LocatedSlider for the
        given registry.

        If there are any conflicts, an error will occur.

        Parameters
        ----------
        registry : TargetRegistry
            The registry being registered to.
        """
        registry.register_handler(
            target_class=cls,
            interaction_class=command.KeyClick,
            handler=lambda wrapper, interaction:
                _interaction_helpers.key_click_slider(
                    wrapper._target.slider, interaction, wrapper.delay)
        )


def register(registry):
    """ Register interactions for the given registry.

    If there are any conflicts, an error will occur.

    Parameters
    ----------
    registry : TargetRegistry
        The registry being registered to.
    """

    targets = [SimpleSliderEditor,
               LogRangeSliderEditor,
               LargeRangeSliderEditor]
    for target_class in targets:
        registry.register_solver(
            target_class=target_class,
            locator_class=locator.Textbox,
            solver=lambda wrapper, _: LocatedTextbox(
                textbox=wrapper._target.control.text),
        )
        registry.register_solver(
            target_class=target_class,
            locator_class=locator.Slider,
            solver=lambda wrapper, _: LocatedSlider(
                slider=wrapper._target.control.slider),
        )
    _registry_helper.register_editable_textbox_handlers(
        registry=registry,
        target_class=RangeTextEditor,
        widget_getter=lambda wrapper: wrapper._target.control,
    )

    LocatedTextbox.register(registry)

    LocatedSlider.register(registry)