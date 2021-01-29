import configparser
import os


class ConfigResolver:

    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read("config.ini")
        self._config = config

    @property
    def rancher_url(self) -> str:
        return self._get_config_value('RANCHER_URL', 'rancher', 'url')

    @property
    def rancher_token(self) -> str:
        return self._get_config_value('RANCHER_TOKEN', 'rancher', 'token')
    
    @property
    def group_admin(self) -> str:
        return self._get_config_value("GROUP_ADMIN", "rbac", "group_admin")

    def _get_config_value(
            self, environemnt_variable_name: str, config_name: str, config_attribute: str,
    ) -> str:
        return (
                os.getenv(environemnt_variable_name)
                or self._config.get(config_name, config_attribute)
        )
