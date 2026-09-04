from tests.conftest import EMPTY_ACTIVITY, EXISTING_PARTICIPANT, EXISTING_ACTIVITY, NEW_PARTICIPANT


def signup(client, activity, email):
    return client.post(f"/activities/{activity}/signup", params={"email": email})


def test_signup_adds_participant(client):
    response = signup(client, EMPTY_ACTIVITY, NEW_PARTICIPANT)

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {NEW_PARTICIPANT} for {EMPTY_ACTIVITY}"
    }

    activities = client.get("/activities").json()
    assert NEW_PARTICIPANT in activities[EMPTY_ACTIVITY]["participants"]


def test_signup_twice_is_rejected(client):
    response = signup(client, EXISTING_ACTIVITY, EXISTING_PARTICIPANT)

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

    activities = client.get("/activities").json()
    participants = activities[EXISTING_ACTIVITY]["participants"]
    assert participants.count(EXISTING_PARTICIPANT) == 1


def test_signup_for_unknown_activity(client):
    response = signup(client, "Underwater Basket Weaving", NEW_PARTICIPANT)

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_without_email_is_invalid(client):
    response = client.post(f"/activities/{EMPTY_ACTIVITY}/signup")

    assert response.status_code == 422
