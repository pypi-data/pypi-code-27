from tornado.options import options


from middleware import config, model
from middleware.components.synchronization import ActiveDirectoryUserSync
from middleware.components.user_sync_processor import UserSyncProcessor

config.initialize()


class Sync:
    @staticmethod
    def run():
        model.Log.delete_logs(options.logs_expires)
        sync_id = model.Sync.add_sync()
        try:
            ActiveDirectoryUserSync(sync_id).start_sync()
            UserSyncProcessor(sync_id).start_sync()
        except Exception as e:
            args = {"message": "sync_failed", "success": False, "sync_id": sync_id, "data_1": str(e)}
            model.Log.add_log(**args)
            raise e
        else:
            args = {"message": "Sync successfully finished", "success": True, "sync_id": sync_id}
            model.Log.add_log(**args)
