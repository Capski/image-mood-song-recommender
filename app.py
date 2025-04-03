import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

from image_analysis import analyze_image
from spotify_integration import get_spotify_recommendations

load_dotenv()

app = Flask(__name__)

# Ensure 'uploads' directory exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = os.path.join('uploads', file.filename)
        file.save(filename)

        try:
            dominant_colors, mood = analyze_image(filename)
            recommendation = get_spotify_recommendations(mood)

            # Convert numpy arrays to lists for JSON serialization
            dominant_colors_list = [list(map(int, color)) for color in dominant_colors]

            response = {
                'dominant_colors': dominant_colors_list,
                'mood': mood,
                'recommendation': recommendation
            }
            return jsonify(response)

        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            # Clean up the uploaded file
            if os.path.exists(filename):
                os.remove(filename)

if __name__ == '__main__':
    app.run(debug=True)