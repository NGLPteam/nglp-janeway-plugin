import functools

from events import logic as events_logic
from utils import plugins
from utils.install import update_settings


class NGLPPlugin(plugins.Plugin):
    plugin_name = "NGLP Plugin"
    display_name = "NGLP"
    description = "NGLP event integration"
    author = "Cottage Labs"
    short_name = "nglp"
    # stage = "nglp_plugin"

    # manager_url = MANAGER_URL

    version = "0.1"
    janeway_version = "1.3.9"

    is_workflow_plugin = False
    # handshake_url = HANDSHAKE_URL
    # article_pk_in_handshake_url = ARTICLE_PK_IN_HANDSHAKE_URL


def install():
    NGLPPlugin.install()
    update_settings(
        file_path='plugins/nglp/install/settings.json'
    )

def hook_registry():
    return

def register_for_events():
    # plugin modules can't be imported until plugin is loaded
    # plugin will need to be written elsewhere first before we can load it.
    from plugins.nglp import events


    events_logic.Events.register_for_event(
        events_logic.Events.ON_ARTICLE_ACCESS,
        events.on_article_access,
    )

    for key in events.NGLP_ANALYTICS_EVENT_CONFIG:
        events_logic.Events.register_for_event(
            key,
            events.on_workflow_event,
        )

