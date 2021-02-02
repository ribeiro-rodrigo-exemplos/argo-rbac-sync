from app.pipeline import PipelineBuilder
from app.config.config_resolver import ConfigResolver


def main():

    pipeline = PipelineBuilder(ConfigResolver()).build()

    pipeline.list_all_clusters() \
            .list_all_members() \
            .remove_local_members() \
            .aggregate_cluster_members() \
            .generate_rbac_csv() \
            .save_configmap()


if __name__ == "__main__":
    main()
