import pytest
import uuid
from datetime import datetime
from src.models.settings.db_connection_handler import db_connection_handler
from .activities_repository import ActivitiesRepository

db_connection_handler.connect()

@pytest.mark.skip(reason="Skipping due to database interaction")
def test_registry_activity():
    conn = db_connection_handler.get_connection()
    activities_repository = ActivitiesRepository(conn)

    activity_id = str(uuid.uuid4())
    trip_id = str(uuid.uuid4())

    activity_infos = {
        "id": activity_id,
        "trip_id": trip_id,
        "title": "Visit to Osaka Castle",
        "occurs_at": datetime.strptime("03-01-2024 10:00:00", "%d-%m-%Y %H:%M:%S")
    }

    activities_repository.registry_activity(activity_infos)
    
    cursor = activities_repository._ActivitiesRepository__conn.cursor()
    cursor.execute('SELECT * FROM activities WHERE id = ?', (activity_id,))
    result = cursor.fetchone()

    assert result is not None
    assert result[0] == activity_id
    assert result[1] == trip_id
    assert result[2] == "Visit to Osaka Castle"
    assert result[3] == activity_infos["occurs_at"]

@pytest.mark.skip(reason="Skipping due to database interaction")
def test_find_activities_from_trip():
    conn = db_connection_handler.get_connection()
    activities_repository = ActivitiesRepository(conn)
    
    trip_id = str(uuid.uuid4())

    activity_infos = {
        "id": str(uuid.uuid4()),
        "trip_id": trip_id,
        "title": "Visit to Osaka Castle",
        "occurs_at": datetime.strptime("03-01-2024 10:00:00", "%d-%m-%Y %H:%M:%S")
    }

    # Insert a test activity
    activities_repository.registry_activity(activity_infos)
    
    response = activities_repository.find_activities_from_trip(trip_id)
    
    assert isinstance(response, list)
    assert len(response) > 0
    assert response[0][0] == activity_infos["id"]
    assert response[0][1] == activity_infos["trip_id"]
    assert response[0][2] == activity_infos["title"]
    assert response[0][3] == activity_infos["occurs_at"]

