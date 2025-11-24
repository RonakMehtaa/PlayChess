"""
API Test Script
Tests all backend endpoints to verify functionality
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a section header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_response(response):
    """Pretty print response."""
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

def test_health_check():
    """Test health check endpoint."""
    print_section("1. Health Check")
    response = requests.get(f"{BASE_URL}/")
    print_response(response)
    return response.status_code == 200

def test_start_game():
    """Test starting a new game."""
    print_section("2. Start New Game (White, Level 5)")
    
    data = {
        "player_color": "white",
        "bot_level": 5
    }
    
    response = requests.post(f"{BASE_URL}/start_game", json=data)
    print_response(response)
    
    if response.status_code == 200:
        return response.json()["game_id"]
    return None

def test_player_move(game_id):
    """Test making a player move."""
    print_section("3. Make Player Move (e2e4)")
    
    data = {
        "game_id": game_id,
        "move": "e2e4"
    }
    
    response = requests.post(f"{BASE_URL}/player_move", json=data)
    print_response(response)
    
    return response.status_code == 200

def test_get_state(game_id):
    """Test getting game state."""
    print_section("4. Get Game State")
    
    response = requests.get(f"{BASE_URL}/state/{game_id}")
    print_response(response)
    
    return response.status_code == 200

def test_list_games():
    """Test listing all games."""
    print_section("5. List All Games")
    
    response = requests.get(f"{BASE_URL}/games")
    print_response(response)
    
    return response.status_code == 200

def test_invalid_move(game_id):
    """Test making an invalid move."""
    print_section("6. Test Invalid Move")
    
    data = {
        "game_id": game_id,
        "move": "e2e5"  # Invalid - pawn can't move 3 squares
    }
    
    response = requests.post(f"{BASE_URL}/player_move", json=data)
    print_response(response)
    
    # Should return error
    return response.status_code == 400

def test_delete_game(game_id):
    """Test deleting a game."""
    print_section("7. Delete Game")
    
    response = requests.delete(f"{BASE_URL}/game/{game_id}")
    print_response(response)
    
    return response.status_code == 200

def run_all_tests():
    """Run all tests."""
    print("\n" + "🎯 Chess API Test Suite")
    print("Starting tests...\n")
    
    results = []
    
    try:
        # Test 1: Health Check
        success = test_health_check()
        results.append(("Health Check", success))
        
        if not success:
            print("\n❌ Backend not running! Start the backend first.")
            return
        
        time.sleep(0.5)
        
        # Test 2: Start Game
        game_id = test_start_game()
        results.append(("Start Game", game_id is not None))
        
        if not game_id:
            print("\n❌ Could not start game. Stopping tests.")
            return
        
        time.sleep(0.5)
        
        # Test 3: Player Move
        success = test_player_move(game_id)
        results.append(("Player Move", success))
        time.sleep(0.5)
        
        # Test 4: Get State
        success = test_get_state(game_id)
        results.append(("Get State", success))
        time.sleep(0.5)
        
        # Test 5: List Games
        success = test_list_games()
        results.append(("List Games", success))
        time.sleep(0.5)
        
        # Test 6: Invalid Move
        success = test_invalid_move(game_id)
        results.append(("Invalid Move Handling", success))
        time.sleep(0.5)
        
        # Test 7: Delete Game
        success = test_delete_game(game_id)
        results.append(("Delete Game", success))
        
        # Print results
        print_section("Test Results Summary")
        
        passed = 0
        failed = 0
        
        for test_name, success in results:
            status = "✓ PASS" if success else "✗ FAIL"
            color = "\033[92m" if success else "\033[91m"
            reset = "\033[0m"
            print(f"{color}{status}{reset} - {test_name}")
            
            if success:
                passed += 1
            else:
                failed += 1
        
        print(f"\nTotal: {passed + failed} tests")
        print(f"✓ Passed: {passed}")
        print(f"✗ Failed: {failed}")
        
        if failed == 0:
            print("\n🎉 All tests passed! Backend is working correctly.")
        else:
            print(f"\n⚠️  {failed} test(s) failed. Check the output above.")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to backend!")
        print("Make sure the backend is running at http://localhost:8000")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    run_all_tests()
