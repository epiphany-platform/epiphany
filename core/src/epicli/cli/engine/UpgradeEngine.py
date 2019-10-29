import os
import time
import shutil
import re

from cli.helpers.Step import Step
from cli.engine.ansible.AnsibleCommand import AnsibleCommand
from cli.engine.ansible.AnsibleRunner import AnsibleRunner
from cli.engine.ansible.AnsibleInventoryUpgrade import AnsibleInventoryUpgrade
from cli.helpers.build_saver import check_build_output_version, get_inventory_path_for_build, BUILD_EPICLI


class UpgradeEngine(Step):
    def __init__(self, input_data):
        super().__init__(__name__)
        self.build_dir = input_data.build_directory
        self.build_version = BUILD_EPICLI
        self.backup_build_dir = ''
        self.ansible_command = AnsibleCommand()

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)

    def get_backup_dirs(self):
        result = []
        for d in os.listdir(self.build_dir):
            bd = os.path.join(self.build_dir, d)
            if os.path.isdir(bd) and re.match(r'backup_\d', d): result.append(bd)
        return result        

    def backup_build(self):
        # check if there are backup dirs and if so take the latest to work with.
        backup_dirs = self.get_backup_dirs()
        if len(backup_dirs) > 0:
            self.backup_build_dir = max(backup_dirs , key=os.path.getmtime)
            self.logger.info(f'There is already a backup present. Using latest for upgrade: "{self.backup_build_dir}"')
            return

        # no backup dir so use the latest
        backup_dir_name = f'backup_{int(round(time.time() * 1000))}'
        backup_temp_dir = os.path.join(self.build_dir, '../', backup_dir_name)
        self.backup_build_dir = os.path.join(self.build_dir, backup_dir_name )
        self.logger.info(f'Backing up old build files to "{self.backup_build_dir}"')
        shutil.move(self.build_dir, backup_temp_dir, copy_function = shutil.copytree) 
        if not os.path.exists(self.build_dir):
            os.mkdir(self.build_dir)        
        shutil.move(backup_temp_dir, self.backup_build_dir, copy_function = shutil.copytree)

    def upgrade(self):
        # backup existing build
        self.backup_build()

        # upgrade inventory
        self.build_version = check_build_output_version(self.backup_build_dir)
        with AnsibleInventoryUpgrade(self.build_dir, self.backup_build_dir, self.build_version) as inventory_upgrade:
            inventory_upgrade.upgrade()

        # do ansible stuff

        return 0      