import pytest
import uuid
from src.models.settings.db_connection_handler import db_connection_handler
from .participants_repository import ParticipantsRepository

db_connection_handler.connect()

@pytest.mark.skip(reason="Skipping due to database interaction")
def test_registry_participantes():
    conn = db_connection_handler.get_connection()
    participants_repository = ParticipantsRepository(conn)

    participant_id = str(uuid.uuid4())
    trip_id = str(uuid.uuid4())
    emails_to_invite_id = str(uuid.uuid4())

    participant_infos = {
        "id": participant_id,
        "trip_id": trip_id,
        "emails_to_invite_id": emails_to_invite_id,
        "name": "Cometa"
    }

    participants_repository.registry_participantes(participant_infos)
    
    cursor = participants_repository._ParticipantsRepository__conn.cursor()
    cursor.execute('SELECT * FROM participants WHERE id = ?', (participant_id,))
    result = cursor.fetchone()

    assert result is not None
    assert result[0] == participant_id
    assert result[1] == trip_id
    assert result[2] == emails_to_invite_id
    assert result[3] == "Cometa"

@pytest.mark.skip(reason="Skipping due to database interaction")
def test_find_participantes_from_trip():
    conn = db_connection_handler.get_connection()
    participants_repository = ParticipantsRepository(conn)
    
    trip_id = str(uuid.uuid4())

    participant_infos = {
        "id": str(uuid.uuid4()),
        "trip_id": trip_id,
        "emails_to_invite_id": str(uuid.uuid4()),
        "name": "Jane Doe"
    }

    # Insert a test participant
    participants_repository.registry_participantes(participant_infos)
    
    response = participants_repository.find_participantes_from_trip(trip_id)
    
    assert isinstance(response, list)
    assert len(response) > 0
    assert response[0][0] == participant_infos["id"]
    assert response[0][1] == participant_infos["name"]

@pytest.mark.skip(reason="Skipping due to database interaction")
def test_update_participant_status():
    conn = db_connection_handler.get_connection()
    participants_repository = ParticipantsRepository(conn)
    
    participant_id = str(uuid.uuid4())

    participant_infos = {
        "id": participant_id,
        "trip_id": str(uuid.uuid4()),
        "emails_to_invite_id": str(uuid.uuid4()),
        "name": "Jane Doe"
    }

    # Insert a test participant
    participants_repository.registry_participantes(participant_infos)
    
    participants_repository.update_participant_status(participant_id)
    
    cursor = participants_repository._ParticipantsRepository__conn.cursor()
    cursor.execute('SELECT is_confirmed FROM participants WHERE id = ?', (participant_id,))
    result = cursor.fetchone()

    assert result is not None
    assert result[0] == 1
