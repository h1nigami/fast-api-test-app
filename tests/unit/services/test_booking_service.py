import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch, Mock
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app import BookingService

class TestBookingService:
    
    @pytest.fixture
    def mock_db(self):
        db = AsyncMock(spec=AsyncSession)
        transatcion = AsyncMock()
        transatcion.__aenter__ = AsyncMock(return_value=db)
        transatcion.__aexit__= AsyncMock(return_value=None)
        db.begin.return_value = transatcion
        return db
    
    @pytest.fixture
    def booking_service(self):
        return BookingService()
    
    @pytest.fixture
    def mock_event(self):
        mock_event = MagicMock()
        mock_event.id = 1
        mock_event.total_seats = 10
        return mock_event
    
    @pytest.mark.asyncio
    async def test_reserve_succes(self, booking_service:BookingService, mock_db:AsyncMock, mock_event):
        event_id = 1
        user_id = "user123"
        booking_service.event_repo.get_by_id = AsyncMock(return_value=[mock_event])
        booking_service.booking_repo.count_by_event = AsyncMock(return_value=5)
        booking_service.booking_repo.create = Mock(
            return_value={"id":1, "event_id":event_id, "user_id":user_id}
        )
        result = await booking_service.reserve(mock_db, event_id, user_id)

        booking_service.event_repo.get_by_id.assert_called_once_with(mock_db, event_id)
        booking_service.booking_repo.count_by_event.assert_called_once_with(mock_db, event_id)
        booking_service.booking_repo.create.assert_called_once_with(mock_db, event_id, user_id)

        assert result["id"] == 1
        assert result["event_id"] == event_id
        assert result["user_id"] == user_id

        mock_db.begin.assert_called_once()

    @pytest.mark.asyncio
    async def test_reserve_event_not_found(self, booking_service: BookingService, mock_db: AsyncMock):
        event_id = 999
        user_id = "user123"
        
        booking_service.event_repo.get_by_id = AsyncMock(return_value=[])

        with pytest.raises(HTTPException) as info:
            await booking_service.reserve(mock_db, event_id, user_id)

        assert info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Мероприятие не найдено" in str(info.value.detail)

    @pytest.mark.asyncio
    async def test_no_seats_available(self, booking_service: BookingService, mock_db: AsyncMock, mock_event: MagicMock):
        event_id = 1
        user_id = "user123"
        
        booking_service.event_repo.get_by_id = AsyncMock(return_value=[mock_event])
        booking_service.booking_repo.count_by_event = AsyncMock(return_value=10)

        with pytest.raises(HTTPException) as info:
            await booking_service.reserve(mock_db, event_id, user_id)
            
        assert info.value.status_code == status.HTTP_409_CONFLICT
        assert "Нет свободных мест" in str(info.value.detail)

    @pytest.mark.asyncio
    async def test_booking_conflict(self, booking_service: BookingService, mock_db: AsyncMock, mock_event: MagicMock):
        event_id = 1
        user_id = "user123"
        booking_service.event_repo.get_by_id = AsyncMock(return_value=[mock_event])
        call_count = 0
        booking_service.booking_repo.count_by_event = AsyncMock(return_value=5)
        def mock_side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return {"id":1, "event_id":event_id, "user_id":user_id}
            else:
                raise IntegrityError("UNIQUE constraint failed", None, None)
        booking_service.booking_repo.create = Mock(
            side_effect=mock_side_effect
        )
        succes = await booking_service.reserve(mock_db, event_id, user_id)

        assert succes["id"] == 1
        assert succes["user_id"] == user_id

        with pytest.raises(HTTPException) as info: 
            await booking_service.reserve(mock_db, event_id, user_id)

        

        assert info.value.status_code == status.HTTP_409_CONFLICT
        assert "Пользователь уже забронирован" in str(info.value.detail)