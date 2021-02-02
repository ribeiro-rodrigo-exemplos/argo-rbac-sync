from kubernetes import client, config
from kubernetes.client import V1ConfigMap


class RbacService:

    def __init__(self, argo_namespace: str):
        config.load_kube_config()
        self._v1 = client.CoreV1Api()
        self._namespace = argo_namespace
        self._configmap_name = "argocd-rbac-cm"

    def get_permissions(self) -> str:

        field_selector = f"metadata.name={self._configmap_name}"

        config_map_list = self._v1.list_namespaced_config_map(
            self._namespace, field_selector=field_selector,
        )

        if not config_map_list.items:
            raise Exception(f"ConfigMap {self._configmap_name} not found")

        rbac_config_map = config_map_list.items[0]
        return rbac_config_map.data.get("policy.csv")

    def save_permissions(self, rbac_csv: str):
        body = {
            "data": {
                "policy.csv": rbac_csv
            }
        }
        response = self._v1.patch_namespaced_config_map(self._configmap_name, self._namespace, body)
        if not isinstance(response, V1ConfigMap):
            response.raise_for_status()



