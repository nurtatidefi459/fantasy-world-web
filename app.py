import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-123')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-dev-456')
    
    # Basic routes
    @app.route('/')
    def home():
        return jsonify({
            "message": "🎮 Fantasy World RPG - Server Online!",
            "status": "success",
            "version": "1.0.0",
            "endpoints": {
                "game_status": "/api/status",
                "character_create": "/api/character/create",
                "world_info": "/api/world/info"
            }
        })
    
    @app.route('/health')
    def health_check():
        return jsonify({"status": "healthy"}), 200
    
    @app.route('/api/status')
    def api_status():
        return jsonify({
            "game": "Fantasy World RPG",
            "status": "online", 
            "players_online": 0,
            "server_time": "2024",
            "maintenance": False
        })
    
    @app.route('/api/world/info')
    def world_info():
        return jsonify({
            "world_name": "Aetheria",
            "zones": ["Starting Village", "Dark Forest", "Dragon Mountains"],
            "current_event": "Dragon Festival",
            "weather": "sunny"
        })
    
    @app.route('/api/character/create', methods=['POST', 'GET'])
    def create_character():
        if request.method == 'POST':
            data = request.get_json() or {}
            name = data.get('name', 'Adventurer')
            char_class = data.get('class', 'Warrior')
            
            return jsonify({
                "message": "Character created successfully!",
                "character": {
                    "name": name,
                    "class": char_class,
                    "level": 1,
                    "health": 100,
                    "mana": 50,
                    "gold": 100,
                    "inventory": ["Health Potion", "Basic Sword"]
                }
            })
        else:
            return jsonify({
                "message": "Send POST request with: name, class",
                "example_classes": ["Warrior", "Mage", "Archer", "Rogue"]
            })
    
    @app.route('/api/game/start', methods=['GET'])
    def game_start():
        return jsonify({
            "message": "Welcome to Fantasy World! Your adventure begins...",
            "starting_zone": "Village of Beginnings",
            "available_quests": ["Find the Lost Amulet", "Defeat the Goblin King"],
            "next_step": "Create your character at /api/character/create"
        })
    
    logger.info("🚀 Fantasy World Server initialized!")
    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"🎮 Starting Fantasy World on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
