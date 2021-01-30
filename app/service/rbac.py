from kubernetes import client, config


class RbacService:

    def __init__(self, argo_namespace: str):
        config.load_kube_config()
        self._v1 = client.CoreV1Api()
        self._namespace = argo_namespace
        self._field_selector = "metadata.name=argocd-rbac-cm"

    def get_permissions(self) -> str:
        config_map_list = self._v1.list_namespaced_config_map(
            self._namespace, field_selector=self._field_selector
        )

        if not config_map_list.items:
            raise Exception(f"ConfigMap {self._field_selector} not found")

        rbac_config_map = config_map_list.items[0]
        return rbac_config_map.data

    def save_permissions(self):
        pass