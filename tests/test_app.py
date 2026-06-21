from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def reset_activities():
    activities.clear()
    activities.update(
        {
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
            },
            "Programming Class": {
                "description": "Learn programming fundamentals and build software projects",
                "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                "max_participants": 20,
                "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
            },
            "Gym Class": {
                "description": "Physical education and sports activities",
                "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
                "max_participants": 30,
                "participants": ["john@mergington.edu", "olivia@mergington.edu"],
            },
            "Soccer Team": {
                "description": "Practice teamwork and compete in soccer matches",
                "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
                "max_participants": 18,
                "participants": [],
            },
            "Basketball Club": {
                "description": "Work on shooting, defense, and game strategy",
                "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
                "max_participants": 15,
                "participants": [],
            },
            "Drama Club": {
                "description": "Explore acting, stage performance, and theater techniques",
                "schedule": "Mondays, 3:30 PM - 5:00 PM",
                "max_participants": 16,
                "participants": [],
            },
            "Art Workshop": {
                "description": "Create paintings, sketches, and mixed-media projects",
                "schedule": "Thursdays, 3:30 PM - 5:00 PM",
                "max_participants": 14,
                "participants": [],
            },
            "Math Olympiad": {
                "description": "Solve challenging problems and prepare for math competitions",
                "schedule": "Wednesdays, 4:00 PM - 5:00 PM",
                "max_participants": 10,
                "participants": [],
            },
            "Debate Team": {
                "description": "Practice public speaking, argumentation, and research skills",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": [],
            },
        }
    )


def test_root_redirects_to_static_index():
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")


def test_get_activities_returns_all_activities():
    reset_activities()

    response = client.get("/activities")

    assert response.status_code == 200
    assert response.json() == activities
    assert len(response.json()) == 9


def test_signup_for_activity_adds_participant():
    reset_activities()

    response = client.post(
        "/activities/Soccer Team/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up student@mergington.edu for Soccer Team"
    }
    assert "student@mergington.edu" in activities["Soccer Team"]["participants"]


def test_signup_fails_for_duplicate_email():
    reset_activities()

    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student already signed up for this activity"
    }


def test_signup_fails_for_unknown_activity():
    reset_activities()

    response = client.post(
        "/activities/Unknown Activity/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_removes_participant():
    reset_activities()

    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Removed michael@mergington.edu from Chess Club"
    }
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_fails_for_unknown_email():
    reset_activities()

    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "missing@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Student is not registered for this activity"
    }
