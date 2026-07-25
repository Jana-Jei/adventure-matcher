from flask import Flask, render_template, jsonify, request, send_from_directory
import os
from engine import InferenceEngine, QUESTIONS, RULES, get_gallery_images_for_folder

app = Flask(__name__, static_folder='static', template_folder='templates')
engine = InferenceEngine(rules=RULES, questions=QUESTIONS)

# Route to serve images from root level 'images' folder if present, or static/images
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = BASE_DIR
STATIC_IMAGES_DIR = os.path.join(BASE_DIR, 'static', 'images')

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/matcher')
def matcher():
    return render_template('index.html')

@app.route('/api/questions', methods=['GET'])
def get_questions():
    return jsonify({"questions": QUESTIONS})

@app.route('/api/infer', methods=['POST'])
def infer():
    data = request.get_json() or {}
    facts = data.get('facts', {})

    next_question_id = engine.get_next_question_id(facts)
    final_facts, rules_fired = engine.forward_chain(facts)

    # Resolve recommendations and images if complete
    recommendations = final_facts.get('recommendation', [])
    warning = final_facts.get('warning', '')
    rating = final_facts.get('rating', '')
    folder_key = final_facts.get('folder_key', '')

    # Check images folder locations
    active_img_dir = IMAGES_DIR if os.path.exists(IMAGES_DIR) else STATIC_IMAGES_DIR
    gallery_images = []

    if folder_key and os.path.exists(active_img_dir):
        gallery_images = get_gallery_images_for_folder(folder_key, active_img_dir)

    # Format fired rules for explanation trace window
    trace = []
    for r in rules_fired:
        trace.append({
            "id": r["id"],
            "conditions": r["conditions"],
            "conclusions": r["conclusions"],
            "explanation_en": r.get("explanation_en", "")
        })

    return jsonify({
        "completed": next_question_id is None,
        "next_question_id": next_question_id,
        "facts": final_facts,
        "recommendations": recommendations,
        "warning": warning,
        "rating": rating,
        "folder_key": folder_key,
        "gallery_images": gallery_images,
        "rules_fired": trace
    })

@app.route('/images/<path:filename>')
def serve_custom_image(filename):
    if os.path.exists(os.path.join(IMAGES_DIR, filename)):
        return send_from_directory(IMAGES_DIR, filename)
    elif os.path.exists(os.path.join(STATIC_IMAGES_DIR, filename)):
        return send_from_directory(STATIC_IMAGES_DIR, filename)
    return "Image not found", 404

if __name__ == '__main__':
    print("Starting Adventure Matcher Expert System Flask Server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
