from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import datetime

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Base AudioModel
class AudioModel(db.Model):
    __abstract__ = True
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    uploaded_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

class SongModel(AudioModel):
    __tablename__ = 'songmodel'
    id = db.Column(db.Integer, primary_key=True)

class PodcastModel(AudioModel):
    __tablename__  = 'podcastmodel'
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(100), nullable=False)

class AudioBookModel(AudioModel):
    __tablename__ = 'audiobookmodel'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    narrator = db.Column(db.String(100), nullable=False )

# db.drop_all()
# db.create_all()

# Get Put Patch Delete endpoints for the requested audiofiletype
class AudioFile(Resource):
    def get(self,audioFileType,audioFileId):
        try:
            if audioFileType == "Podcast":
                res = PodcastModel.query.filter_by(id=audioFileId).first()
                return {"name":res.name,"duration":res.duration,"host":res.host,"uploaded_time":str(res.uploaded_time)}
            elif audioFileType == "Audiobook":
                res = AudioBookModel.query.filter_by(id=audioFileId).first()
                return {"title":res.name,"duration":res.duration,"narrator":res.narrator,"author":res.author,"uploaded_time":str(res.uploaded_time)}
            elif audioFileType == "Song":
                res = SongModel.query.filter_by(id=audioFileId).first()
                return {"name":res.name,"duration":res.duration,"uploaded_time":str(res.uploaded_time)}
            else:
                return {"message":f"{audioFileType} is not a valid audioFileType.."}, 400
        except AttributeError:
            return {"message":f"{audioFileType} with ID-{audioFileId} doesn't exists.."}, 400

    def put(self,audioFileType,audioFileId):
        try:
            if audioFileType == "Song":
                args = ("name","duration")
                req = request.form
                if req:
                    if len(req)==len(args):
                        for key in req:
                            if key not in args:
                                return {"message":f"{key} key in the request body is incorrect.."}, 400
                        name = req['name']
                        if not len(name)<101:
                            return {"message":"Please provide proper name within 100 characters.."}, 400
                        try:
                            duration = int(req['duration'])
                        except:
                            return {"message":"Type of duration is not int.."}, 400
                        
                        uploaded_time = datetime.datetime.now()
                    else:
                        return {"message":"Entered Request body is incorrect.."}, 400
                
                song = SongModel(id=audioFileId,
                                 name = name,
                                 duration = duration,
                                 uploaded_time = uploaded_time
                                 )
                db.session.add(song)

            elif audioFileType == "Podcast":
                args = ("name","duration","host")
                req = request.form
                if req:
                    if len(req)==len(args):
                        for key in req:
                            if key not in args:
                                return {"message":f"{key} key in the request body is incorrect.."}, 400
                        name = req['name']
                        if not len(name)<101:
                            return {"message":"Please provide proper name within 100 characters.."}, 400
                        try:
                            duration = int(req['duration'])
                        except:
                            return {"message":"Type of duration is not int.."}, 400
                        host = req['host']
                        if not len(host)<101:
                            return {"message":"Please provide proper host within 100 characters.."}, 400
                        
                        uploaded_time = datetime.datetime.now()
                    else:
                        return {"message":"Entered Request body is incorrect.."}, 400
                
                podcast = PodcastModel(id=audioFileId,
                                       name = name,
                                       duration = duration,
                                       host = host,
                                       uploaded_time = uploaded_time
                                       )
                db.session.add(podcast)
                
            elif audioFileType == "Audiobook":
                args = ("title","duration","author","narrator")
                req = request.form
                if req:
                    if len(req)==len(args):
                        for key in req:
                            if key not in args:
                                return {"message":f"{key} key in the request body is incorrect.."}, 400
                        name = req['title']
                        if not len(name)<101:
                            return {"message":"Please provide proper title within 100 characters.."}, 400
                        try:
                            duration = int(req['duration'])
                        except:
                            return {"message":"Type of duration is not int.."}, 400
                        author = req['author']
                        if not len(author)<101:
                            return {"message":"Please provide proper author name within 100 characters.."}, 400
                        narrator = req['narrator']
                        if not len(narrator)<101:
                            return {"message":"Please provide proper narrator name within 100 characters.."}, 400
                        uploaded_time = datetime.datetime.now()
                    else:
                        return {"message":"Entered Request body is incorrect.."}, 400
                
                audiobook = AudioBookModel(id=audioFileId,
                                           name=name,
                                           duration=duration,
                                           uploaded_time=uploaded_time, 
                                           author=author,
                                           narrator=narrator
                                           )
                db.session.add(audiobook)
            
            else:
                return {"message":f"{audioFileType} is not Valid.."}, 400
            
            db.session.commit()
            return {"message":"success"}

        except IntegrityError:
            db.session.rollback()
            return {"message":f"{audioFileType} of ID {audioFileId} has already existed"}, 400

        except Exception as e:
            return {"message":"Please check the Payload"}, 400
        

    def patch(self,audioFileType,audioFileId):
        if audioFileType in ("Song","Podcast","Audiobook"):
            try:
                if audioFileType == "Song":
                    args = ("name","duration")
                    req = request.form
                    if req:
                        for key in req:
                            if key not in args:
                                return {"message":f"{key} key in the request body is incorrect.."}, 400
                        song = SongModel.query.filter_by(id=audioFileId).first()
                        if 'name' in req:
                            if len(req["name"])>100:
                                return {"message":"Name is more than 100 characters"}, 400
                            else:
                                song.name = req["name"]
                        if 'duration' in req:
                            try:
                                song.duration = int(req["duration"])
                            except:
                                return {"message":"Type of duration is not int.."}, 400
                        db.session.commit()

                elif audioFileType == "Podcast":
                    args = ("name", "duration", "host")
                    req = request.form
                    if req:
                        for key in req:
                            if key not in args:
                                return {"message":f"{key} key in the request body is incorrect.."}, 400
                        podcast = PodcastModel.query.filter_by(id=audioFileId).first()
                        if 'name' in req:
                            if len(req["name"])>100:
                                return {"message":"Name is more than 100 characters"}, 400
                            else:
                                podcast.name = req["name"]
                        if 'duration' in req:
                            try:
                                podcast.duration = int(req["duration"])
                            except:
                                return {"message":"Type of duration is not int.."}, 400
                        if 'host' in req:
                            if len(req["host"])>100:
                                return {"message":"Host is more than 100 characters"}, 400
                            else:
                                podcast.host = req["host"]
                            
                        db.session.commit()

                elif audioFileType == "Audiobook":
                    args = ("title", "duration", "narrator", "author")
                    req = request.form
                    if req:
                        for key in req:
                            if key not in args:
                                return {"message":f"{key} key in the request body is incorrect.."}, 400

                        audiobook = AudioBookModel.query.filter_by(id=audioFileId).first()
                        if 'title' in req:
                            if len(req["title"])>100:
                                return {"message":"Title is more than 100 characters"}, 400
                            else:
                                audiobook.name = req["title"]
                        if 'duration' in req:
                            try:
                                audiobook.duration = int(req["duration"])
                            except:
                                return {"message":"Type of duration is not int.."}, 400
                        if 'narrator' in req:
                            if len(req["narrator"])>100:
                                return {"message":"Narrator is more than 100 characters"}, 400
                            else:
                                audiobook.narrator = req["narrator"]
                        if 'author' in req:
                            if len(req["author"])>100:
                                return {"message":"Author is more than 100 characters"}, 400
                            else:
                                audiobook.author = req["author"]

                        db.session.commit()
            
                return {"message":"Success"}

            except AttributeError:
                return {"message":f"{audioFileType} with ID-{audioFileId} doesn't exists.."}, 400

        else:
            return {"message":f"{audioFileType} is not valid.."}, 400
            
    def delete(self,audioFileType,audioFileId):
        if audioFileType in ("Song","Podcast","Audiobook"):
            try:
                if audioFileType == "Song":
                    song = SongModel.query.filter_by(id=audioFileId).first()
                    db.session.delete(song)
                if audioFileType == "Podcast":
                    podcast = PodcastModel.query.filter_by(id=audioFileId).first()
                    db.session.delete(podcast)
                if audioFileType == "Audiobook":
                    audiobook = AudioBookModel.query.filter_by(id=audioFileId).first()
                    db.session.delete(audiobook)
                db.session.commit()
                return {"message":"success"}
            except AttributeError:
                return {"message":f"{audioFileType} with ID-{audioFileId} doesn't exists.."}, 400
        else:
            return {"message":f"{audioFileType} is not valid.."}, 400

# Route to get the data of all the audiofiles of the requested type        
class GetAudioFiles(Resource):
    def get(self,audioFileType):
        if audioFileType in ("Song","Podcast","Audiobook"):
            data = {}
            if audioFileType == "Song":
                songs = SongModel.query.all()
                for song in songs:
                    song_data = {"name":song.name,"duration":song.duration,"uploaded_time":str(song.uploaded_time)}
                    data[f'{song.id}'] = song_data
                return {"Songs":data}

            if audioFileType == "Audiobook":
                audiobooks = AudioBookModel.query.all()
                for audiobook in audiobooks:
                    audiobook_data = {"title":audiobook.name,"duration":audiobook.duration,"author":audiobook.author,
                                    "narrator":audiobook.narrator,"uploaded_time":str(audiobook.uploaded_time)}
                    data[f'{audiobook.id}'] = audiobook_data
                return {"Audiobooks":data}

            if audioFileType == "Podcast":
                podcasts = PodcastModel.query.all()
                for podcast in podcasts:
                    podcast_data = {"name":podcast.name,"duration":podcast.duration,"host":podcast.host,
                                    "uploaded_time":str(podcast.uploaded_time)}
                    data[f'{podcast.id}'] = podcast_data
                return {"Podcasts":data}
        else:
            return {"message":f"{audioFileType} is not valid.."}, 400

# Adding routes            
api.add_resource(AudioFile,"/<string:audioFileType>/<int:audioFileId>")
api.add_resource(GetAudioFiles,"/<string:audioFileType>")

if __name__ == "__main__":
    app.run(debug=True)