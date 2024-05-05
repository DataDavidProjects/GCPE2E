import os
from dataclasses import dataclass
from dotenv import find_dotenv, load_dotenv
from google.cloud import artifactregistry, storage

from utils.project import ArtifactRegistryConfig, CloudStorageConfig, ProjectConfig

# specify utils in import for import in main.py
from utils.project import DockerConfig


# Load environment variables from .env file
load_dotenv(find_dotenv())


@dataclass
class LazyPipe:
    """
    A class to encapsulate the pipeline creation and execution process.
    """

    pipe: str

    def __post_init__(self):
        """
        Initialize the DockerConfig instance and create the Docker container.
        """
        self.container_args = {
            self.pipe: {
                "image_name": self.pipe,
                "image_tag": "latest",
                "dockerfile_path": f"pipelines/{self.pipe}/Dockerfile",
                "repository_id": os.environ.get("BUCKET_NAME"),
                "project_id": os.environ.get("PROJECT_ID"),
                "region": os.environ.get("REGION"),
            }
        }
        self.project_config = {
            # Environment Variables
            "project_id": os.environ.get("PROJECT_ID"),
            "project_number": os.environ.get("PROJECT_NUMBER"),
            "region": os.environ.get("REGION"),
            "service_account": os.environ.get("SERVICE_ACCOUNT"),
            "bucket_name": os.environ.get("BUCKET_NAME"),
            # Note: match directory names with pipeline names in pipelines directory
            "directories": self.pipe,
        }
        # Initialzie Cloud Storage Client
        self.storage_client = storage.Client()
        # Initialize Artifact Registry Client
        self.artifactregistry_client = artifactregistry.ArtifactRegistryClient()
        # Initialize Project Config
        self.project_config = ProjectConfig(config=self.project_config)
        # Initialize Artifact Registry Config
        self.artifactregistry_config = ArtifactRegistryConfig(
            client=self.artifactregistry_client, config=self.project_config
        )
        # Initialize Cloud Storage Config
        self.cloud_storage_config = CloudStorageConfig(
            client=self.storage_client, config=self.project_config
        )
        # Initialize Artifact Registry Config
        self.artifactregistry_config = ArtifactRegistryConfig(
            client=self.artifactregistry_client, config=self.project_config
        )

    def enable_resources(self):
        """
        Enable the required resources for the pipeline.
        """

        # Enable APIs
        self.project_config.enable_apis()

    def set_up_storage(self):
        """
        Set up the Cloud Storage bucket and template directories.
        """
        self.cloud_storage_config.create_bucket().template_directories()

    def set_up_artifact_registry(self):
        """
        Set up the Artifact Registry repository.
        """
        self.artifactregistry_config.create_repository()

    def create_container(self):
        """
        Create the Docker container.
        """
        docker_config = DockerConfig(config=self.container_args[self.pipe])
        docker_config.create_container()

    def define_pipeline(self):
        """
        Define the pipeline by running the definition script.
        """
        os.system(f"python pipelines/{self.pipe}/definition.py")

    def run_pipeline(self):
        """
        Run the pipeline by running the run script.
        """
        os.system(f"python pipelines/{self.pipe}/run.py")

    def magic(self, setup=False):
        """
        Define and run the pipeline.
        """
        if setup:
            self.enable_resources()
            self.set_up_storage()
            self.set_up_artifact_registry()

        self.create_container()
        self.define_pipeline()
        self.run_pipeline()
