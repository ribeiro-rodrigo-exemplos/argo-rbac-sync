from typing import List, Dict
import csv
from io import StringIO

from app.infra import get_logger
from app.model.entities import Cluster, ClusterRoleBinding, ClusterMember
from app.service import RancherService, RbacService


_logger = get_logger(__name__)


def list_cluster_members(rancher_service: RancherService) -> List[ClusterRoleBinding]:
    _logger.debug("Listing all members in the Rancher")

    members = list(
        map(
            lambda binding_dto: ClusterRoleBinding(
                    principal_id=binding_dto["userPrincipalId"] or binding_dto["groupPrincipalId"],
                    cluster_id=binding_dto["clusterId"],
                    is_group=binding_dto["userPrincipalId"] is None
                ),
            rancher_service.list_cluster_role_bindings()
        )
    )

    _logger.debug(f"Rancher listed members {members}")

    return members


def list_clusters(rancher_service: RancherService, rancher_url: str) -> List[Cluster]:
    _logger.debug("Listing all clusters in the Rancher")

    clusters = list(
        map(
            lambda cluster_dto: Cluster(
                url=f"{rancher_url}/k8s/clusters/{cluster_dto['id']}",
                name=cluster_dto["name"],
                id=cluster_dto["id"],
            ),
            rancher_service.list_clusters(),
        )
    )

    _logger.debug(f"Rancher listed clusters {clusters}")

    return clusters


def remove_local_members(bindings: List[ClusterRoleBinding]) -> List[ClusterRoleBinding]:
    _logger.debug("Removing local members")

    return list(
        filter(
            lambda binding: not binding.principal_id.startswith("local"),
            bindings
        )
    )


def aggregate_cluster_members(clusters: List[Cluster], bindings: List[ClusterRoleBinding]) -> List[ClusterMember]:
    _logger.debug("Aggregating clusters and members")

    map_cluster: Dict[str, Cluster] = {cluster.id: cluster for cluster in clusters}
    cluster_members: List[ClusterMember] = []

    for binding in bindings:
        cluster = map_cluster.get(binding.cluster_id)
        if cluster:
            cluster_members.append(ClusterMember(member=binding, cluster=cluster))

    _logger.debug(f"Aggregation result {cluster_members}")

    return cluster_members


def generate_rbac_csv(cluster_members: List[ClusterMember], admin_group: str) -> str:
    _logger.debug("Generating CSV RBAC")

    def get_principal_name(cm: ClusterMember):
        return cm.member.principal_id.split(":")[1].replace("/", "")

    csv_lines = []

    for cluster_member in cluster_members:
        principal: str = get_principal_name(cluster_member)
        project_name = cluster_member.cluster.name
        project_permission = ["p", principal, "projects", "get", project_name, "allow"]
        application_permission = ["p", principal, "applications", "*", f"{project_name}/*", "allow"]
        gpg_keys_permission = ["p", principal, "gpgkeys", "get", "*", "allow"]
        cluster_permission = ["p", principal, "clusters", "get", cluster_member.cluster.url, "allow"]

        csv_lines.append(project_permission)
        csv_lines.append(application_permission)
        csv_lines.append(gpg_keys_permission)
        csv_lines.append(cluster_permission)

    csv_lines.append(["g", admin_group, "role:admin"])

    data = StringIO(initial_value="")
    writer = csv.writer(data)
    writer.writerows(csv_lines)

    csv_value = data.getvalue()

    _logger.debug(f"RBAC CSV permissions generated: {csv_value}")

    return data.getvalue()


def save_rbac(rbac_csv: str, rbac_service: RbacService):
    _logger.debug("Checking the need to update RBAC permissions")

    current_rbac_csv = rbac_service.get_permissions()

    if current_rbac_csv != rbac_csv:
        rbac_service.save_permissions(rbac_csv)
        _logger.debug("RBAC permissions saved successfully.")



