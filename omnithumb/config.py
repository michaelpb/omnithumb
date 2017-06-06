import os

def load_settings():
    from omnithumb import default_settings
    from omnithumb.conversion.converter import ConverterGraph
    from omnithumb.responses.placeholder import PlaceholderSelector
    settings = default_settings
    custom_settings_path = os.environ.get('OMNIC_SETTINGS')
    if custom_settings_path:
        # TODO import here
        pass
    settings.converter_graph = ConverterGraph(settings.CONVERTERS)
    settings.placeholders = PlaceholderSelector(settings)
    return default_settings

def override_settings(new_settings):
    global settings
    settings = new_settings

settings = load_settings()

