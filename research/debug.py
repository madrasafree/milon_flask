import os
from source.sound_index_function import get_sound_index

print(get_sound_index("פיצ'ר מוזר לאללה"))

current_dir =  os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.abspath(current_dir + "/../")
file_dir = parent_dir + "\\App_Data\\arabicWords.mdb"
print(current_dir)
print(parent_dir)
print(file_dir)

# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def hello():
    # return 'Hello, World!'
	
# if __name__ == '__main__':
    # app.run(host="192.168.2.109", port=5000, debug=True)