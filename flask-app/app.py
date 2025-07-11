from flask import Flask, jsonify
from flask_cors import CORS  # Import essentiel
import stripe

# Configuration cruciale de CORS
app = Flask(__name__)
CORS(app, resources={
    r"/create-checkout-session": {
        "origins": ["http://localhost:3000", "http://localhost:8080", "http://localhost"],
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

stripe.api_key = 'sk_test_51O51rjArOje5RHk1KrKULu6bGF8jzRCFg528h3wDLBNVPotsFxPzr6IYXbUDqNH0B7unFsvkHAh7bv2byTzrrDrI00fVkfonlt'

@app.route('/create-checkout-session', methods=['POST', 'OPTIONS'])  # OPTIONS requis
def create_checkout_session():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': 'price_1RjhWCArOje5RHk10CGPft8x',
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:3000/success',
            cancel_url='http://localhost:3000/cancel',
        )
        return _corsify_response(jsonify(sessionId=session.id))
    except Exception as e:
        return _corsify_response(jsonify(error=str(e)), 500)

def _build_cors_preflight_response():
    response = jsonify()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

def _corsify_response(response, status_code=200):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response