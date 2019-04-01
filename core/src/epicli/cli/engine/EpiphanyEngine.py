import os
from cli.helpers.objdict_helpers import merge_objdict, dict_to_objdict
from cli.helpers.doc_list_helpers import select_first, select_single
from cli.helpers.defaults_loader import load_file_from_defaults, load_all_docs_from_defaults
from cli.helpers.build_saver import save_build
from cli.helpers.config_merger import merge_with_defaults
from cli.engine.aws.AWSConfigBuilder import AWSConfigBuilder
from cli.helpers.yaml_helpers import safe_load_all
from engine.SchemaValidator import SchemaValidator
from cli.engine.AnsibleRunner import AnsibleRunner
from modules.terraform_runner.TerraformRunner import TerraformRunner


class EpiphanyEngine:

    def __init__(self, input_data):

        self.BUILD_FOLDER_PATH = '../../build/'

        self.file_path = input_data.file
        self.context = input_data.context

    def __enter__(self):
        return self

    def run(self):
        docs = self.merge_with_user_input_with_defaults()
        cluster_model = select_single(docs, lambda x: x.kind == "epiphany-cluster")
        infrastructure_builder = self.get_infrastructure_builder_for_provider(cluster_model.provider)
        infrastructure = infrastructure_builder.build(cluster_model, docs)

        for component_key, component_value in cluster_model.specification.components.items():
            if component_value.count < 1:
                continue
            self.append_component_configuration(docs, component_key, component_value, cluster_model)

        result = docs + infrastructure
        save_build(result, cluster_model.specification.name)

        with SchemaValidator(docs) as schema_validator:
            schema_validator.validate()

        # todo generate .tf files
        script_dir = os.path.dirname(__file__)
        terraform_build_directory = os.path.join(script_dir, self.BUILD_FOLDER_PATH, self.context, "terraform")

        # todo run terraform
        # todo set path to terraform files
        with TerraformRunner(terraform_build_directory, cluster_model, infrastructure) as tf_runner:
            tf_runner.run()

        # todo validate
        print("Running ansible.")
        # todo generate ansible inventory
        with AnsibleRunner(dict_to_objdict(cluster_model), result) as runner:
            runner.run()

        # todo adjust ansible to new schema
        # todo run ansible

    def merge_with_user_input_with_defaults(self):
        if os.path.isabs(self.file_path):
            path_to_load = self.file_path
        else:
            path_to_load = os.path.join(os.getcwd(), self.file_path)

        user_file_stream = open(path_to_load, 'r')
        user_yaml_files = safe_load_all(user_file_stream)
        state_docs = []

        for user_file_yaml in user_yaml_files:
            files = load_all_docs_from_defaults(user_file_yaml.provider, user_file_yaml.kind)
            file_with_defaults = select_first(files, lambda x: x.name == "default")
            merge_objdict(file_with_defaults, user_file_yaml)
            state_docs.append(file_with_defaults)

        return state_docs

    def __exit__(self, exc_type, exc_value, traceback):
        print("close")

    @staticmethod
    def get_infrastructure_builder_for_provider(provider):
        if provider.lower() == "aws":
            return AWSConfigBuilder()

    @staticmethod
    def append_component_configuration(docs, component_key, component_value, cluster_model):

        features_map = select_first(docs, lambda x: x.kind == 'configuration/feature-mapping')
        if features_map is None:
            features_map = load_file_from_defaults('common', 'configuration/feature-mapping')
            docs.append(features_map)
        config_selector = component_value.configuration
        for feature_key in features_map.specification[component_key]:
            config = select_first(docs,
                                  lambda x: x.kind == 'configuration/' + feature_key and x.name == config_selector)
            if config is None:
                config = merge_with_defaults('common', 'configuration/' + feature_key, config_selector)
            docs.append(config)
