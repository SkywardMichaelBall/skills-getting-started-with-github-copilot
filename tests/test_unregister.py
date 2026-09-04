from tests.conftest import EMPTY_ACTIVITY, EXISTING_ACTIVITY, EXISTING_PARTICIPANT, NEW_PARTICIPANT


def unregister(client, activity, email):
    return client.delete(f"/activities/{activity}/unregister", params={"email": email})


def test_unregister_removes_participant(client):
    response = unregister(client, EXISTING_ACTIVITY, EXISTING_PARTICIPANT)

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {EXISTING_PARTICIPANT} from {EXISTING_ACTIVITY}"
    }

    activities = client.get("/activities").json()
    assert EXISTING_PARTICIPANT not in activities[EXISTING_ACTIVITY]["participants"]


def test_unregister_non_participant(client):
    response = unregister(client, EXISTING_ACTIVITY, NEW_PARTICIPANT)

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_from_unknown_activity(client):
    response = unregister(client, "Underwater Basket Weaving", NEW_PARTICIPANT)

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_then_unregister_round_trip(client):
    before = client.get("/activities").json()[EMPTY_ACTIVITY]["participants"]

    client.post(f"/activities/{EMPTY_ACTIVITY}/signup", params={"email": NEW_PARTICIPANT})
    unregister(client, EMPTY_ACTIVITY, NEW_PARTICIPANT)

    after = client.get("/activities").json()[EMPTY_ACTIVITY]["participants"]
    assert after == before
