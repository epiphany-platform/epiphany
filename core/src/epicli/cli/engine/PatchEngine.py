import os

from cli.engine.AnsibleCommand import AnsibleCommand
from cli.engine.AnsibleRunner import AnsibleRunner
from cli.helpers.Step import Step
from cli.helpers.build_saver import get_inventory_path, copy_files_recursively, copy_file


class PatchEngine(Step):

    def __init__(self):
        super().__init__(__name__)
        self.ansible_command = AnsibleCommand()

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)

    def run(self):
        pass

    def run_upgrade(self, build_directory):
        build_roles_directory = os.path.join(build_directory, 'ansible/roles')

        upgrade_playbook_path = os.path.join(build_roles_directory, 'upgrade')
        backup_playbook_path = os.path.join(build_roles_directory, 'backup')
        recovery_playbook_path = os.path.join(build_roles_directory, 'recovery')

        upgrade_role_path = os.path.join(build_directory, 'ansible', 'upgrade.yml')

        epiphany_playbooks_path = os.path.dirname(__file__) + AnsibleRunner.ANSIBLE_PLAYBOOKS_PATH
        epiphany_roles_path = os.path.join(epiphany_playbooks_path, 'roles')

        upgrade_role_source_path = os.path.join(epiphany_roles_path, 'upgrade')
        backup_role_source_path = os.path.join(epiphany_roles_path, 'backup')
        restore_role_source_path = os.path.join(epiphany_roles_path, 'recovery')
        playbook_source_path = os.path.join(epiphany_playbooks_path, 'upgrade.yml')

        copy_files_recursively(upgrade_role_source_path, upgrade_playbook_path)
        copy_files_recursively(backup_role_source_path, backup_playbook_path)
        copy_files_recursively(restore_role_source_path, recovery_playbook_path)
        copy_file(playbook_source_path, upgrade_role_path)

        inventory_path = get_inventory_path(build_directory)
        self.ansible_command.run_playbook(inventory=inventory_path, playbook_path=upgrade_role_path)

    def run_backup(self, build_directory):
        backup_role_path = os.path.join(build_directory, 'ansible', 'backup.yml')
        inventory_path = get_inventory_path(build_directory)
        self.ansible_command.run_playbook(inventory=inventory_path, playbook_path=backup_role_path)

    def run_recovery(self, build_directory):
        backup_role_path = os.path.join(build_directory, 'ansible', 'recovery.yml')
        inventory_path = get_inventory_path(build_directory)
        self.ansible_command.run_playbook(inventory=inventory_path, playbook_path=backup_role_path)

    @staticmethod
    def get_inventory_path(build_directory):
        return os.path.join(build_directory, 'inventory')
