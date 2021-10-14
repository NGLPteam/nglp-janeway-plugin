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

    events_logic.Events.register_for_event(
        events_logic.Events.ON_ARTICLE_SUBMITTED,
        events.on_article_submitted,
    )
    #
    # events_logic.Events.register_for_event(
    #     events_logic.Events.ON_ARTICLE_ACCEPTED,
    #     events.on_article_submitted,
    # )

    # for name in dir(events_logic.Events):
    #     event_name = getattr(events_logic.Events, name)
    #     if isinstance(event_name, str):
    #         events_logic.Events.register_for_event(event_name, functools.partial(on_any_event, event_name))


def on_any_event(event_name, /, *args, **kwargs):
    print("EVENT!", event_name, args, kwargs)

# functools.partial(f, a)(b, c) == f(a, b, c)
# functools.partial(f, x=x)(b, c) == f(b, c, x=x)