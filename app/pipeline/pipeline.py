from typing import List
import attr

from app.service import RancherService, RbacService
from app.config.config_resolver import ConfigResolver
from app.model.entities import Cluster, ClusterRoleBinding, ClusterMember
from app.pipeline.steps import list_clusters, list_cluster_members, aggregate_cluster_members, \
    generate_rbac_csv, save_rbac, remove_local_members as rm_local_members


@attr.s(auto_attribs=True)
class PipelineState:
    rbac_csv: str = None
    clusters: List[Cluster] = attr.ib(default=[])
    bindings: List[ClusterRoleBinding] = attr.ib(default=[])
    members: List[ClusterMember] = attr.ib(default=[])


@attr.s(auto_attribs=True)
class Pipeline:
    _rancher_service: RancherService
    _rbac_service: RbacService
    _admin_group: str
    _rancher_url: str

    def __attrs_post_init__(self):
        self._state = PipelineState()

    def list_all_clusters(self):
        self._state.clusters = list_clusters(self._rancher_service, self._rancher_url)
        return self

    def list_all_members(self):
        self._state.bindings = list_cluster_members(self._rancher_service)
        return self

    def remove_local_members(self):
        self._state.bindings = rm_local_members(self._state.bindings)
        return self

    def aggregate_cluster_members(self):
        self._state.members = aggregate_cluster_members(self._state.clusters, self._state.bindings)
        return self

    def generate_rbac_csv(self):
        self._state.rbac_csv = generate_rbac_csv(self._state.members, self._admin_group)
        return self

    def save_configmap(self):
        save_rbac(self._state.rbac_csv, self._rbac_service)


@attr.s(auto_attribs=True)
class PipelineBuilder:
    _config: ConfigResolver

    def build(self) -> Pipeline:
        rancher_service = RancherService(
            url=self._config.rancher_url,
            token=self._config.rancher_token,
            timeout=self._config.rancher_timeout,
        )

        return Pipeline(
            rancher_url=self._config.rancher_url,
            rancher_service=rancher_service,
            rbac_service=RbacService(self._config.argo_namespace),
            admin_group=self._config.admin_group
        )
