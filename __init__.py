import logging

from flatland import Boolean, Integer, Float, Form
from flatland.validation import ValueAtLeast
from microdrop.app_context import get_app
from microdrop.plugin_helpers import (StepOptionsController, AppDataController)
from microdrop.plugin_manager import (IPlugin, Plugin, implements,
                                      PluginGlobals)
import conda_helpers as ch
import path_helpers as ph

logger = logging.getLogger(__name__)

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

# Add plugin to `"microdrop.managed"` plugin namespace.
PluginGlobals.push_env('microdrop.managed')


class MrBoxPeripheralBoardPlugin(Plugin, StepOptionsController, AppDataController):
    '''
    This class is automatically registered with the PluginManager.
    '''
    implements(IPlugin)

    plugin_name = ph.path(__file__).realpath().parent.name
    try:
        version = ch.package_version(plugin_name).get('version')
    except NameError:
        version = 'v0.0.0+unknown'

    AppFields = Form.of(Integer.named('int_field')
                        .using(default=1, optional=True,
                               validators=[ValueAtLeast(minimum=0)]))

    StepFields = Form.of(Boolean.named('bool_field')
                         .using(default=False, optional=True),
                         Float.named('float_field')
                         .using(default=0, optional=True,
                                validators=[ValueAtLeast(minimum=0)]))


    def __init__(self):
        super(MrBoxPeripheralBoardPlugin, self).__init__()

    def on_plugin_enable(self):
        super(MrBoxPeripheralBoardPlugin, self).on_plugin_enable()

    def on_plugin_disable(self):
        try:
            super(MrBoxPeripheralBoardPlugin, self).on_plugin_disable()
        except AttributeError:
            pass

    def on_app_exit(self):
        '''
        Handler called just before the Microdrop application exits.
        '''
        pass

    def on_protocol_swapped(self, old_protocol, protocol):
        '''
        Handler called when a new step is loaded/activated.

        Parameters
        ----------
        old_protocol : microdrop.protocol.Protocol
            Previously activated protocol.
        protocol : microdrop.protocol.Protocol
            Newly activated protocol.
        '''
        pass

    def on_app_options_changed(self, plugin_name):
        '''
        Handler called when application field values have changed for the
        specified plugin.

        Parameters
        ----------
        plugin_name : str
            Name of plugin.
        '''
        if plugin_name == self.name:
            # XXX Application field values have changed for current plugin.

            # Get latest application field values for this plugin.
            app_values = self.get_app_values()
            # ... Process application values, e.g., update UI ...

    def on_step_run(self):
        '''
        Handler called whenever a step is executed.

        Plugins that handle this signal **MUST** emit the ``on_step_complete``
        signal once they have completed the step.  The protocol controller will
        wait until all plugins have completed the current step before
        proceeding.
        '''
        # Get latest step field values for this plugin.
        options = self.get_step_options()
        # ... Perform step actions ...

    def on_protocol_run(self):
        '''
        Handler called when a protocol starts running.
        '''
        pass

    def on_protocol_pause(self):
        '''
        Handler called when a protocol is paused.
        '''
        app = get_app()
        self._kill_running_step()
        if self.control_board and not app.realtime_mode:
            # Turn off all electrodes
            logger.debug('Turning off all electrodes.')
            self.control_board.hv_output_enabled = False

    def on_experiment_log_selection_changed(self, data):
        '''
        Handler called whenever the experiment log selection changes.

        Parameters
        ----------
        data : dict
            Dictionary of experiment log data for the selected steps.
        '''
        pass

    def on_step_options_changed(self, plugin, step_number):
        '''
        Handler called when field values for the specified plugin and step.

        Parameters
        ----------
        plugin : str
            Name of plugin.
        step_number : int
            Step index number.
        '''
        pass

    def on_step_swapped(self, original_step_number, new_step_number):
        '''
        Handler called when a new step is activated/selected.

        Parameters
        ----------
        original_step_number : int
            Step number of previously activated step.
        new_step_number : int
            Step number of newly activated step.
        '''
        pass

    def get_schedule_requests(self, function_name):
        '''
        For example, to request to schedule the ``on_step_options_changed``
        callback to be called on this plugin before being the protocol grid UI
        is updated, use:

            >>>> from microdrop.plugin_manager import ScheduleRequest
            >>>>
            >>>> if function_name in ['on_step_options_changed']:
            >>>>     return [ScheduleRequest(self.name,
            >>>>                             'microdrop.gui.protocol_grid_controller'),
            >>>>             ScheduleRequest(self.name,
            >>>>                             'microdrop.gui.protocol_controller'),

        Returns
        -------
        list
            List of scheduling requests (i.e., ``ScheduleRequest`` instances)
            for the function specified by function_name.
        '''
        return []


PluginGlobals.pop_env()
