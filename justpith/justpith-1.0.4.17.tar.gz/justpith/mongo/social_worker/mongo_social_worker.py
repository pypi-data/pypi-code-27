# encoding: utf-8
import traceback
from ..mongo import Mongo

class MongoSocialWorker(Mongo):
    def __init__(self,host, port, db):
        super(MongoSocialWorker,self).__init__(host, port, db)
        self.collection_feed_room = "Users_Social_Feed_Room"


    def set_feed_room_id(self, user_id, feed_room_id):
        try:
            selected_collection = self.connection[self.collection_feed_room]
            selected_collection.update({"_id": user_id}, {"$set": {"feed_room_id": feed_room_id}}, upsert=True)
            return 1
        except Exception as e:
            traceback.print_exc()
            return None


    def get_feed_room_id(self, user_id):
        try:
            selected_collection = self.connection[self.collection_feed_room]
            result = selected_collection.find_one({"_id": int(user_id)}, {"feed_room_id":1})
            if result is not None and "feed_room_id" in result:
                return result["feed_room_id"]
            else:
                return None
        except Exception as e:
            traceback.print_exc()
            return None

