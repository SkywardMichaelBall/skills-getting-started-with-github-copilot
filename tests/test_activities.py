EXPECTED_ACTIVITIES = {
    "Chess Club",
    "Programming Class",
    "Gym Class",
    "Soccer Club",
    "Basketball Club",
    "Art Club",
    "Drama Club",
    "Science Club",
    "Debate Club",
}


def test_get_activities_returns_all_seeded_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert set(response.json()) == EXPECTED_ACTIVITIES


def test_activity_payload_shape(client):
    activities = client.get("/activities").json()

    for name, details in activities.items():
        assert isinstance(details["description"], str), name
        assert isinstance(details["schedule"], str), name
        assert isinstance(details["max_participants"], int), name
        assert isinstance(details["participants"], list), name


def test_root_redirects_to_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.is_redirect
    assert response.headers["location"] == "/static/index.html"


def test_static_files_are_mounted(client):
    response = client.get("/static/index.html")

    assert response.status_code == 200


def test_seeded_state_is_restored_between_tests(client):
    chess_club = client.get("/activities").json()["Chess Club"]

    assert chess_club["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]
