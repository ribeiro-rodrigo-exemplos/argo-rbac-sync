from app.rancher import RancherService
from app.pipeline import Pipeline


def main():
    url: str = "https://192.168.0.76"
    token: str = "token-q5bhr:xtcd5lbzlg6mhnvncwbrk55zvmhb849vzqm7wnv2xtrtzhs9sq6dss"

    service = RancherService(url=url, token=token)
    pipeline = Pipeline(rancher_service=service)

    pipeline.list_all_clusters() \
            .list_all_members() \
            .remove_local_members() \
            .aggregate_cluster_members() \
            .generate_rbac_csv() \
            .save_configmap()


if __name__ == "__main__":
    main()
