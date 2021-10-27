import os

from deploy.installer import GitManager
from module.handler.login import LoginHandler
from module.logger import logger


class AzurLaneUncensored(LoginHandler):
    def run(self):
        """
        This will do:
        1. Update AzurLaneUncensored repo
        2. Adb push to emulator
        3. Restart game
        """
        repo = self.config.AzurLaneUncensored_Repository
        folder = './toolkit/AzurLaneUncensored'

        logger.hr('Update AzurLaneUncensored', level=1)
        logger.info('This will take a while at first use')
        manager = GitManager()
        os.makedirs(folder, exist_ok=True)
        prev = os.getcwd()
        os.chdir(folder)
        manager.git_repository_init(
            repo=repo,
            source='origin',
            branch='master',
            proxy=manager.config['GitProxy'],
            keep_changes=False
        )

        logger.hr('Push Uncensored Files', level=1)
        command = ['push', 'files', f'/sdcard/Android/data/{self.config.Emulator_PackageName}']
        logger.info(f'Command: {command}')
        self.device.adb_command(command)
        logger.info('Push success')

        os.chdir(prev)
        logger.hr('Restart AzurLane', level=1)
        self.device.app_stop()
        self.device.app_start()
        self.handle_app_login()

        logger.info('Uncensored Finished')


if __name__ == '__main__':
    AzurLaneUncensored('alas', task='AzurLaneUncensored').run()
