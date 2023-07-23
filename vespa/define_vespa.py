from pathlib import Path
from vespa.deployment import VespaDocker

from vespa.package import ApplicationPackage, Field, FieldSet, HNSW, RankProfile

if __name__ == '__main__':
    app_package = ApplicationPackage(name="images", create_query_profile_by_default=False)
    app_package.schema.add_fields(
        Field(name="id", type="string", indexing=["attribute", "summary"]),
        Field(name="filename", type="string", indexing=["summary"]),
        # innerproduct works well if we have the embeddings normalized for example with L2 :)
        Field(name="embedding", type="tensor<float>(x[1280])", indexing=["index", "attribute", "summary"],
              ann=HNSW(
                  distance_metric="innerproduct",
                  max_links_per_node=16,
                  neighbors_to_explore_at_insert=200,
              ))
    )
    app_package.schema.add_rank_profile(
        RankProfile(name="semantic-similarity", inherits="default", first_phase="closeness(embedding)",
                    inputs=[("query(query_embedding)", "tensor<float>(x[1280])")]))
    app_package.to_files(Path("."))
    vespa_container = VespaDocker()
    app_package = vespa_container.deploy_from_disk(application_name="myapp", application_root=Path("."))
