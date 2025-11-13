from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Player properties
player_size = 50
player_x = SCREEN_WIDTH // 2 - player_size // 2
player_y = SCREEN_HEIGHT // 2 - player_size // 2
player_speed = 5

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/update', methods=['POST'])
def update_game():
    """Handle game state updates from client"""
    global player_x, player_y
    
    data = request.json
    keys = data.get('keys', {})
    
    # Validate keys input
    if not isinstance(keys, dict):
        return jsonify({'error': 'Invalid keys format: must be a dictionary'}), 400
    if not all(isinstance(v, bool) for v in keys.values()):
        return jsonify({'error': 'Invalid keys values: all values must be booleans'}), 400
    
    # Move player based on key input
    if keys.get('ArrowLeft') or keys.get('KeyA'):
        player_x -= player_speed
    if keys.get('ArrowRight') or keys.get('KeyD'):
        player_x += player_speed
    if keys.get('ArrowUp') or keys.get('KeyW'):
        player_y -= player_speed
    if keys.get('ArrowDown') or keys.get('KeyS'):
        player_y += player_speed
    
    # Keep player on screen
    player_x = max(0, min(player_x, SCREEN_WIDTH - player_size))
    player_y = max(0, min(player_y, SCREEN_HEIGHT - player_size))
    
    # Return game state
    return jsonify({
        'player_x': player_x,
        'player_y': player_y,
        'player_size': player_size,
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
