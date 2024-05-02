# VertexAI-E2E Template

Vertex AI End2End Template for Training and Deployment of Supervised ML

Using main.py:

- Initialize Environment Variables
- Create a Bucket in Cloud Storage
- Create a Pseudo File System for each Pipeline inside the newly created Bucket

Using container.py:

- Create a Repository in Artifact Registry for Docker Images

#### Pipeline and Components

The pipeline is made by components.
Each component has a parameter input named `component_args` of type Dict[str,str].
Each pipeline has a parameter input named `pipeline_args` of type Dict[`component_args`].

#### Definition of components and their parameters

Each pipeline is compiled alongside all of the components.
The output is a json file with the pipeline instructions for VertexAI.
Once a component is compiled it is possible to inspect its own definition inside the component folder.

The file `definition.py` is used in both context of pipeline and component.
