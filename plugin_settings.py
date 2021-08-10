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