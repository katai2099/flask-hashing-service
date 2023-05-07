from flask import Flask, request, jsonify
from flask_api import status
from PIL import Image
from dejavu.logic.recognizer.file_recognizer import FileRecognizer
from dejavu import Dejavu
import os

app = Flask(__name__)

audio_uploads_dir = os.path.join(app.instance_path, 'audio')
os.makedirs(audio_uploads_dir, exist_ok=True)


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


@app.route("/hash/audio", methods=['POST'])
def hashAudio():
    audioFile = request.files.get("audio")
    audioFile.save(os.path.join(audio_uploads_dir, audioFile.filename))
    # results = djv.recognize(FileRecognizer, audio_uploads_dir+'/'+audioFile.filename)
    # file already existed
    existingHash = djv.isExistHash(audio_uploads_dir+'/'+audioFile.filename)
    if (existingHash != ""):
        return jsonify(existingHash), status.HTTP_400_BAD_REQUEST
    # check if file duplicate in database
    recognizedLists = djv.recognize(
        FileRecognizer, audio_uploads_dir+'/'+audioFile.filename)
    # print(recognizedLists)
    recognizedResults = list(recognizedLists['results'])
    for song in recognizedResults:
        if (song['input_confidence'] > 0.8):
            print(f"audio already existed with hash id {song['file_sha1']}")
            return jsonify(song['file_sha1']), status.HTTP_400_BAD_REQUEST
    fileHash = djv.fingerprint_file(audio_uploads_dir+'/'+audioFile.filename)
    print(fileHash)
    return jsonify(fileHash)

   # djv.fingerprint_directory(audio_uploads_dir, [".mp3"])


@app.route("/hash/recognise", methods=['POST'])
def recognize():
    audioFile = request.files.get("audio")
    audioFile.save(os.path.join(audio_uploads_dir, audioFile.filename))
    # file already existed
    existingHash = djv.isExistHash(audio_uploads_dir+'/'+audioFile.filename)
    if (existingHash != ""):
        return jsonify(existingHash), status.HTTP_400_BAD_REQUEST
    # check if file duplicate in database
    recognizedLists = djv.recognize(
        FileRecognizer, audio_uploads_dir+'/'+audioFile.filename)
    # print(recognizedLists)
    recognizedResults = list(recognizedLists['results'])
    for song in recognizedResults:
        if (song['input_confidence'] > 0.8):
            print(f"audio already existed with hash id {song['file_sha1']}")
            return jsonify(song['file_sha1']), status.HTTP_400_BAD_REQUEST
    return jsonify("File is unique"), status.HTTP_200_OK
