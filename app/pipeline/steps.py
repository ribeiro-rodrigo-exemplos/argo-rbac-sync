from typing import List, Dict
import csv
from io import StringIO
from app.model.entities import Cluster, ClusterRoleBinding, ClusterMember
from app.service.rancher import RancherService


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


def remove_local_members(bindings: List[ClusterRoleBinding]) -> List[ClusterRoleBinding]:
    return list(
        filter(
            lambda binding: not binding.principal_id.startswith("local"),
            bindings
        )
    )


def aggregate_cluster_members(clusters: List[Cluster], bindings: List[ClusterRoleBinding]) -> List[ClusterMember]:

    map_cluster: Dict[str, Cluster] = {cluster.id: cluster for cluster in clusters}
    cluster_members: List[ClusterMember] = []

    for binding in bindings:
        cluster = map_cluster.get(binding.cluster_id)
        if cluster:
            cluster_members.append(ClusterMember(member=binding, cluster=cluster))

    return cluster_members


def generate_rbac_csv(cluster_members: List[ClusterMember]) -> str:

    def get_principal_name(cm: ClusterMember):
        return cm.member.principal_id.split(":")[1].replace("/", "")

    csv_lines = []

    for cluster_member in cluster_members:
        principal: str = get_principal_name(cluster_member)
        project_name = cluster_member.cluster.name
        project_permission = ["p", principal, "projects", "get", project_name, "allow"]
        application_permission = ["p", principal, "applications", "*", f"{project_name}/*", "allow"]
        csv_lines.append(project_permission)
        csv_lines.append(application_permission)

    data = StringIO(initial_value="")
    writer = csv.writer(data)
    writer.writerows(csv_lines)

    return data.getvalue()


def save_rbac(rbac_csv: str) -> object:
    print(f"{rbac_csv} - nada")
    pass



