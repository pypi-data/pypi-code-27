import sys
import yt_api
import database
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import json
import isodate
import vimeo_api

#Initializes the communication to the youtube api
client = yt_api.get_yt_service()

#Allows the program to be run using Flask calls ***not sure the right way to articulate this***
app = Flask(__name__)

#Allows the methods to be called from a  different orgin IP address
CORS(app)

#Returns a youtube id of the video best suited to be show to a given user or user
@app.route("/videos", methods=["GET"])
def get_videos():
    db = database.get_database()

    region_id = request.args.get('region_id')
    max_results = request.args.get('max_results')
    category_id = str(request.args.get('category_id'))
    retrieval_count = int(request.args.get('retrieval_count'))
    user_ids = json.loads(request.args.get('user_ids'))

    #Returns a list of tuples [(id, duration), (id, duration)]
    # TODO parse date time format in yt_api
    vid_ids = yt_api.get_top_vids(client, region_id.replace("'", ""), max_results, category_id.replace("'", ""))

    #test id's
    if (retrieval_count % 2 == 0):
        vid_ids = [("9825762", isodate.parse_duration('PT4M27S').total_seconds()),("59829500", isodate.parse_duration('PT12S').total_seconds()) ,("43032498" , isodate.parse_duration('PT26S').total_seconds()),("5226362", isodate.parse_duration('PT49S').total_seconds())]
    else:
        vid_ids = [("59829500", isodate.parse_duration('PT12S').total_seconds()) ,("9825762", isodate.parse_duration('PT4M27S').total_seconds()),("5226362", isodate.parse_duration('PT49S').total_seconds()),("43032498" , isodate.parse_duration('PT26S').total_seconds())]

    #add each video that has been returned by the youtube call, to the data base if not in the data base
    for vid_id in vid_ids:
        if vid_id[0] not in db['videos']:
            db = database.add_video(db, vid_id[0], 'youtube', vid_id[0])

    #For each user in the room
    for user_id in user_ids:
        #Add user to the data base if not in the data base
        if user_id not in db['users']:
            db = database.add_user(db, user_id)
        #For each video that is returned to the kanvas
        for vid_id in vid_ids:
            db = database.add_video_view(db, vid_id[0])
            db = database.add_user_view(db, user_id, vid_id[0])

    database.save_database(db)
    return jsonify(vid_ids)

#Updates the like value of a given video for the given user

@app.route("/test", methods = ["GET"])
def test_videos():
    test = [ {"command" : {"type": command, "scene": "vimeo", "context" : {"type":"video", "id": "43032498", "loop": False}},"type":"command"}]

    return jsonify(test)

@app.route("/user/preferences/video", methods=["GET", "PUT"])
def update_response():
    db = database.get_database()

    user_id = request.args.get("uuid")
    preference = request.args.get("like")
    video_id = request.args.get("video_id")

    if user_id not in db['users']:
        db = database.add_user(db, user_id)

    if video_id not in db['videos']:
        db = database.add_video(db, video_id, 'youtube', video_id)

    db = database.update_user_response(db, user_id, video_id, preference)
    db = database.update_video_repsonses(db, video_id, user_id, preference)

    database.save_database(db)
    #return jsonify(database.get_stats(database, video_id))
    return('Like updated')