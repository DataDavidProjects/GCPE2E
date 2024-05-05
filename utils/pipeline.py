import os
from dataclasses import dataclass
from dotenv import find_dotenv, load_dotenv

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

    def magic(self):
        """
        Define and run the pipeline.
        """
        self.create_container()
        self.define_pipeline()
        self.run_pipeline()
