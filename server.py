from flask import Flask, request, jsonify
from flask_api import status
# from PIL import Image
from dejavu.logic.recognizer.file_recognizer import FileRecognizer
# import imagehash
# import tlsh
from dejavu import Dejavu
import os

app = Flask(__name__)

uploads_dir = os.path.join(app.instance_path, 'audio')
os.makedirs(uploads_dir, exist_ok=True)

config = {
    "database": {
        "host": "127.0.0.1",
        "user": "postgres",
        "password": "admin",
        "database": "dejavu"
    },
    "database_type": "postgres",
}

djv = Dejavu(config)


@app.route("/hash/audio",methods=['POST'])
def hashAudio():
    audioFile = request.files.get("audio")
    audioFile.save(os.path.join(uploads_dir, audioFile.filename))
    #results = djv.recognize(FileRecognizer, uploads_dir+'/'+audioFile.filename)
    
    
    isExist = djv.isExistHash(uploads_dir+'/'+audioFile.filename)
    if(isExist):
        return str(f"{audioFile.filename.split('.mp3')[0]} already fingerprinted, continuing..."), status.HTTP_400_BAD_REQUEST
    # results = djv.recognize(FileRecognizer, uploads_dir+'/'+audioFile.filename)
    results = djv.fingerprint_file(uploads_dir+'/'+audioFile.filename)
    # print(results)
    return str(results)
   
   # djv.fingerprint_directory(uploads_dir, [".mp3"])
    