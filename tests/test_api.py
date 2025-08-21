import json
import pytest
from backend.app import app, _write, _read

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_test_data():
    """Set up test data before each test"""
    # Reset databases
    for name in ["students", "results", "rewards"]:
        _write(name, [])
    
    # Add test videos
    test_videos = [
        {
            "id": "test_vid_1",
            "subject": "Matemáticas",
            "title": "Test Video Math",
            "description": "Test description",
            "duration": "05:00",
            "url": "https://www.youtube.com/embed/test1"
        },
        {
            "id": "test_vid_2", 
            "subject": "Lengua",
            "title": "Test Video Lang",
            "description": "Test description",
            "duration": "10:30",
            "url": "https://www.youtube.com/embed/test2"
        }
    ]
    _write("videos", test_videos)
    
    # Add test questions
    test_questions = [
        {
            "id": "test_q1",
            "level": 1,
            "text": "Test question level 1",
            "options": ["A", "B", "C", "D"],
            "answer_index": 0
        },
        {
            "id": "test_q2",
            "level": 2,
            "text": "Test question level 2", 
            "options": ["A", "B", "C", "D"],
            "answer_index": 1
        },
        {
            "id": "test_q3",
            "level": 3,
            "text": "Test question level 3",
            "options": ["A", "B", "C", "D"],
            "answer_index": 2
        }
    ]
    _write("questions", test_questions)

class TestStudentManagement:
    def test_create_student_success(self, client):
        """Test successful student creation"""
        response = client.post("/api/students", json={
            "name": "Ana García",
            "course": "1ro"
        })
        assert response.status_code == 200
        data = response.get_json()
        assert "id" in data
        assert data["name"] == "Ana García"
        assert data["course"] == "1ro"
        assert "created_at" in data

    def test_create_student_duplicate(self, client):
        """Test that duplicate students return existing record"""
        student_data = {"name": "Ana García", "course": "1ro"}
        
        # Create first time
        response1 = client.post("/api/students", json=student_data)
        data1 = response1.get_json()
        
        # Create second time (should return same student)
        response2 = client.post("/api/students", json=student_data)
        data2 = response2.get_json()
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert data1["id"] == data2["id"]

    def test_create_student_missing_data(self, client):
        """Test student creation with missing required fields"""
        response = client.post("/api/students", json={"name": "Ana García"})
        assert response.status_code == 400
        
        response = client.post("/api/students", json={"course": "1ro"})
        assert response.status_code == 400

    def test_get_student_stats(self, client):
        """Test getting comprehensive student statistics"""
        # Create student
        student_response = client.post("/api/students", json={
            "name": "Ana García", 
            "course": "1ro"
        })
        student = student_response.get_json()
        
        # Get stats
        response = client.get(f"/api/student-stats/{student['id']}")
        assert response.status_code == 200
        
        data = response.get_json()
        assert "student" in data
        assert "stats" in data
        assert "recent_activity" in data
        
        stats = data["stats"]
        assert "total_points" in stats
        assert "tests_completed" in stats
        assert "videos_watched" in stats
        assert "suggested_level" in stats
        assert "avg_score" in stats

class TestVideoSystem:
    def test_get_materias(self, client):
        """Test getting list of available subjects"""
        response = client.get("/api/materias")
        assert response.status_code == 200
        
        materias = response.get_json()
        assert isinstance(materias, list)
        assert "Matemáticas" in materias
        assert "Lengua" in materias

    def test_get_videos_by_subject(self, client):
        """Test getting videos filtered by subject"""
        response = client.get("/api/videos?materia=Matemáticas")
        assert response.status_code == 200
        
        videos = response.get_json()
        assert isinstance(videos, list)
        assert len(videos) == 1
        assert videos[0]["subject"] == "Matemáticas"

    def test_get_videos_with_completion_status(self, client):
        """Test getting videos with completion status for student"""
        # Create student
        student_response = client.post("/api/students", json={
            "name": "Ana García",
            "course": "1ro"
        })
        student = student_response.get_json()
        
        # Get videos with student ID
        response = client.get(f"/api/videos?materia=Matemáticas&student_id={student['id']}")
        assert response.status_code == 200
        
        videos = response.get_json()
        assert len(videos) == 1
        assert "completed" in videos[0]
        assert videos[0]["completed"] is False

    def test_mark_video_complete(self, client):
        """Test marking a video as completed"""
        # Create student
        student_response = client.post("/api/students", json={
            "name": "Ana García",
            "course": "1ro"
        })
        student = student_response.get_json()
        
        # Mark video as complete
        response = client.post("/api/video-completo", json={
            "student_id": student["id"],
            "video_id": "test_vid_1"
        })
        assert response.status_code == 200
        
        data = response.get_json()
        assert data["ok"] is True
        assert data["awarded"] >= 10  # Should award at least base points

    def test_mark_video_complete_duplicate(self, client):
        """Test that marking same video twice doesn't award points again"""
        # Create student
        student_response = client.post("/api/students", json={
            "name": "Ana García",
            "course": "1ro"
        })
        student = student_response.get_json()
        
        # Mark video complete first time
        response1 = client.post("/api/video-completo", json={
            "student_id": student["id"],
            "video_id": "test_vid_1"
        })
        assert response1.get_json()["awarded"] > 0
        
        # Mark video complete second time
        response2 = client.post("/api/video-completo", json={
            "student_id": student["id"],
            "video_id": "test_vid_1"
        })
        assert response2.get_json()["awarded"] == 0

class TestAdaptiveTests:
    def test_get_question_by_level(self, client):
        """Test getting questions by difficulty level"""
        for level in [1, 2, 3]:
            response = client.get(f"/api/pregunta?nivel={level}")
            assert response.status_code == 200
            
            question = response.get_json()
            assert "text" in question
            assert "options" in question
            assert "answer_index" in question
            assert len(question["options"]) == 4

    def test_get_question_invalid_level(self, client):
        """Test getting question for non-existent level falls back gracefully"""
        response = client.get("/api/pregunta?nivel=999")
        # Should fallback to closest available level
        assert response.status_code == 200

    def test_submit_test_result(self, client):
        """Test submitting test results with comprehensive data"""
        # Create student
        student_response = client.post("/api/students", json={
            "name": "Ana García",
            "course": "1ro"
        })
        student = student_response.get_json()
        
        # Submit test result
        response = client.post("/api/test-result", json={
            "student_id": student["id"],
            "correct": 4,
            "final_level": 3,
            "duration_seconds": 180
        })
        assert response.status_code == 200
        
        data = response.get_json()
        assert data["ok"] is True
        assert data["awarded"] > 0
        assert "breakdown" in data
        
        breakdown = data["breakdown"]
        assert "base" in breakdown
        assert "accuracy" in breakdown
        assert "speed" in breakdown
        assert "level" in breakdown

class TestRewardsAndResults:
    def test_get_rewards_with_summary(self, client):
        """Test getting rewards with summary statistics"""
        # Create student
        student_response = client.post("/api/students", json={
            "name": "Ana García",
            "course": "1ro"
        })
        student = student_response.get_json()
        
        # Complete a video and test to generate rewards
        client.post("/api/video-completo", json={
            "student_id": student["id"],
            "video_id": "test_vid_1"
        })
        
        client.post("/api/test-result", json={
            "student_id": student["id"],
            "correct": 3,
            "final_level": 2,
            "duration_seconds": 150
        })
        
        # Get rewards
        response = client.get(f"/api/rewards?student_id={student['id']}")
        assert response.status_code == 200
        
        data = response.get_json()
        assert "total" in data
        assert "items" in data
        assert "summary" in data
        assert data["total"] > 0
        assert len(data["items"]) == 2  # One video, one test
        
        summary = data["summary"]
        assert "video" in summary
        assert "test" in summary

    def test_get_results_with_analytics(self, client):
        """Test getting test results with analytics"""
        # Create student
        student_response = client.post("/api/students", json={
            "name": "Ana García",
            "course": "1ro"
        })
        student = student_response.get_json()
        
        # Submit multiple test results
        for i in range(3):
            client.post("/api/test-result", json={
                "student_id": student["id"],
                "correct": 2 + i,
                "final_level": 2,
                "duration_seconds": 120 + i * 30
            })
        
        # Get results
        response = client.get(f"/api/results?student_id={student['id']}")
        assert response.status_code == 200
        
        data = response.get_json()
        assert "results" in data
        assert "analytics" in data
        assert len(data["results"]) == 3
        
        analytics = data["analytics"]
        assert "total_tests" in analytics
        assert "avg_score" in analytics
        assert "best_score" in analytics
        assert "avg_level" in analytics
        assert analytics["total_tests"] == 3
        assert analytics["best_score"] == 4

class TestIntegrationWorkflows:
    def test_complete_student_journey(self, client):
        """Test a complete student learning journey"""
        # 1. Create student
        student_response = client.post("/api/students", json={
            "name": "María López",
            "course": "2do"
        })
        student = student_response.get_json()
        assert student["name"] == "María López"
        
        # 2. Watch videos
        client.post("/api/video-completo", json={
            "student_id": student["id"],
            "video_id": "test_vid_1"
        })
        client.post("/api/video-completo", json={
            "student_id": student["id"],
            "video_id": "test_vid_2"
        })
        
        # 3. Take tests
        for correct_answers in [2, 3, 4]:
            client.post("/api/test-result", json={
                "student_id": student["id"],
                "correct": correct_answers,
                "final_level": 2,
                "duration_seconds": 180
            })
        
        # 4. Check final stats
        stats_response = client.get(f"/api/student-stats/{student['id']}")
        stats_data = stats_response.get_json()
        
        assert stats_data["stats"]["videos_watched"] == 2
        assert stats_data["stats"]["tests_completed"] == 3
        assert stats_data["stats"]["total_points"] > 0
        assert len(stats_data["recent_activity"]) > 0

if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])