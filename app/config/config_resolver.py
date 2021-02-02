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
    def rancher_timeout(self) -> int:
        return int(self._get_config_value("RANCHER_TIMEOUT", "rancher", "timeout"))
    
    @property
    def admin_group(self) -> str:
        return self._get_config_value("ADMIN_GROUP", "rbac", "admin_group")

    @property
    def argo_namespace(self) -> str:
        return self._get_config_value("ARGO_NAMESPACE", "argo", "namespace")

    def _get_config_value(
            self, environment_variable_name: str, config_name: str, config_attribute: str,
    ) -> str:
        return (
                os.getenv(environment_variable_name)
                or self._config.get(config_name, config_attribute)
        )
