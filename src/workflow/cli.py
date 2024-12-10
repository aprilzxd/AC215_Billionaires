"""
Module that contains the command line app.

Typical usage example from command line:
        python cli.py
"""

import os
import argparse
import random
import string
from kfp import dsl
from kfp import compiler
import google.cloud.aiplatform as aip
# from model import model_training as model_training_job, model_deploy as model_deploy_job


GCP_PROJECT = os.environ["GCP_PROJECT"]
GCS_BUCKET_NAME = os.environ["GCS_BUCKET_NAME"]
BUCKET_URI = f"gs://{GCS_BUCKET_NAME}"
PIPELINE_ROOT = f"{BUCKET_URI}/pipeline_root/root"
GCS_SERVICE_ACCOUNT = os.environ["GCS_SERVICE_ACCOUNT"]
# GCS_PACKAGE_URI = os.environ["GCS_PACKAGE_URI"]
# GCP_REGION = os.environ["GCP_REGION"]

# DATA_COLLECTOR_IMAGE = "gcr.io/ac215-project/cheese-app-data-collector"
DATA_PIPELINE_IMAGE = "barrychang0527/datapipeline"
GEMINI_FINETUNER_IMAGE = "barrychang0527/gemini-finetuner"


def generate_uuid(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))




def pipeline():
    print("pipeline()")
    # Define a Container Component for data collector
    @dsl.container_component
    def data_collector():
        container_spec = dsl.ContainerSpec(
            image=DATA_PIPELINE_IMAGE,
            command=["pipenv", "run", "python"],
            args=[
                "dataloader.py",
                "raw"
            ],
        )
        return container_spec
    
    
    @dsl.container_component
    def data_processing():
        container_spec = dsl.ContainerSpec(
            image=DATA_PIPELINE_IMAGE,
            command=["pipenv", "run", "python"],
            args=[
                "dataloader.py",
                "reddit_500"
            ],
        )
        return container_spec

    # Define a Container Component for data processor
    @dsl.container_component
    def gemini_finetuner():
        container_spec = dsl.ContainerSpec(
            image=GEMINI_FINETUNER_IMAGE,
            command=["pipenv", "run", "python"],
            args=[
                "finetune_test.py"
            ],
        )
        return container_spec

    # Define a Pipeline
    @dsl.pipeline
    def ml_pipeline():
        # Data Collector
        data_collector_task = (
            data_collector()
            .set_display_name("Data Collector")
            .set_cpu_limit("500m")
            .set_memory_limit("2G")
        )
        
        # Data Processor
        data_processing_task = (
            data_processing()
            .set_display_name("Data Processor")
            .set_cpu_limit("500m")
            .set_memory_limit("2G")
            .after(data_collector_task)
        )
        
        
        # Data Processor
        gemini_finetuner_task = (
            gemini_finetuner()
            .set_display_name("Gemini Finetuner")
            .after(data_processing_task)
        )


    # Build yaml file for pipeline
    compiler.Compiler().compile(ml_pipeline, package_path="pipeline.yaml")

    # Submit job to Vertex AI
    aip.init(project=GCP_PROJECT, staging_bucket=BUCKET_URI)

    job_id = generate_uuid()
    DISPLAY_NAME = "billionairs-pipeline-" + job_id
    job = aip.PipelineJob(
        display_name=DISPLAY_NAME,
        template_path="pipeline.yaml",
        pipeline_root=PIPELINE_ROOT,
        enable_caching=False,
    )

    job.run(service_account=GCS_SERVICE_ACCOUNT)




# def main(args=None):
#     if args.pipeline:
#         pipeline()


# if __name__ == "__main__":
#     # Generate the inputs arguments parser
#     # if you type into the terminal 'python cli.py --help', it will provide the description
#     parser = argparse.ArgumentParser(description="Workflow CLI")

#     parser.add_argument(
#         "--pipeline",
#         action="store_true",
#         help="Cheese App Pipeline",
#     )


#     args = parser.parse_args()

#     main(args)


if __name__ == "__main__":
    pipeline()
