from app.pipeline import PipelineBuilder
from app.config.config_resolver import ConfigResolver
from app.infra import get_logger


def main():

    pipeline = PipelineBuilder(ConfigResolver()).build()

    logger = get_logger(__name__)

    logger.info("Inicializando pipeline de sincronismo rbac")
    logger.debug("teste debug")

    pipeline.list_all_clusters() \
            .list_all_members() \
            .remove_local_members() \
            .aggregate_cluster_members() \
            .generate_rbac_csv() \
            .save_configmap()


if __name__ == "__main__":
    main()
