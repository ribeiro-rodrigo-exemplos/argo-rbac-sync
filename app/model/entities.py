from dataclasses import dataclass


@dataclass
class Cluster:
    url: str
    name: str
    id: str


@dataclass
class ClusterRoleBinding:
    cluster_id: str
    principal_id: str
    is_group: bool


@dataclass
class ClusterMember:
    cluster: Cluster
    member: ClusterRoleBinding
