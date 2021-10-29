from flask import Flask, send_file, request, after_this_request
import process
import os
import cv2
import random

# Import the module
app = Flask(__name__)


# Create the index route that renders the sketch.html template in the templates folder
@app.route('/')
def index():
    return send_file('templates/sketch.html')


@app.route('/sketch', methods=['POST'])
def upload():
    # Get the file from post request
    file = request.files['file']

    # Save the file to ./uploads
    file.save(f"uploads/{file.filename}")
    sketch = process.get_sketch(f"./uploads/{file.filename}")
    file_name = f"{random.randint(1, 100)}.png"
    cv2.imwrite(f"./temp/{file_name}", sketch)

    @after_this_request
    def remove_file(response):

        try:
            os.remove(f"./temp/{file_name}")
            os.remove(f"./uploads/{file.filename}")

        except Exception as e:
            print(e)
            app.logger.error("Error removing or closing downloaded file")

        return response
    return send_file(f"./temp/{file_name}", mimetype='image/png')


app.run(host='localhost', port=5000, debug=True)
