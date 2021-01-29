from typing import List, Dict
import csv
from io import StringIO
from app.entities import Cluster, ClusterRoleBinding, ClusterMember
from app.rancher import RancherService


def list_cluster_members(rancher_service: RancherService) -> List[ClusterRoleBinding]:
    return list(
        map(
            lambda binding_dto: ClusterRoleBinding(
                    principal_id=binding_dto["userPrincipalId"] or binding_dto["groupPrincipalId"],
                    cluster_id=binding_dto["clusterId"],
                    is_group=binding_dto["userPrincipalId"] is None
                ),
            rancher_service.list_cluster_role_bindings()
        )
    )


def list_clusters(rancher_service: RancherService) -> List[Cluster]:
    return list(
        map(
            lambda cluster_dto: Cluster(
                name=cluster_dto["name"],
                id=cluster_dto["id"],
            ),
            rancher_service.list_clusters(),
        )
    )


def aggregate_cluster_members(clusters: List[Cluster], bindings: List[ClusterRoleBinding]) -> List[ClusterMember]:
    map_bindings: Dict[str, List[ClusterRoleBinding]] = {}

    for binding in bindings:
        if map_bindings.get(binding.cluster_id):
            map_bindings[binding.cluster_id].append(binding)
        else:
            map_bindings[binding.cluster_id] = [binding]

    cluster_members: List[ClusterMember] = []

    for cluster in clusters:
        if map_bindings.get(cluster.id):
            cluster_members.append(ClusterMember(cluster=cluster, members=map_bindings.get(cluster.id)))

    return cluster_members


def generate_rbac_csv(cluster_members: List[ClusterMember]) -> str:
    #print(cluster_members)
    matriz = [["rodrigo", 31, "masculino"], ["lais", 32, "feminino"]]
    data = StringIO(initial_value="")
    writer = csv.writer(data)
    writer.writerows(matriz)

    print(data.getvalue())
    return ""


def save_rbac(rbac_csv: str) -> object:
    pass



