from typing import Dict


class ConfigObject(object):

    def __init__(self, props: Dict) -> None:
        super().__init__()
        self.props = props

    def get(self, name, default=None):
        prop = self.props[name]
        if prop is None and default is not None:
            return default
        elif prop is None:
            # TODO raise
            pass
        return prop

    def merge(self, props: Dict):
        self.props.update(props)
