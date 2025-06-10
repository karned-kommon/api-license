import pytest
import asyncio
from unittest.mock import patch, MagicMock
from decorators.log_time import log_time, log_time_async

# Test log_time decorator
def test_log_time():
    # Create a mock function to decorate
    mock_func = MagicMock(return_value="test result")
    mock_func.__name__ = "mock_func"
    
    # Apply the decorator
    decorated_func = log_time(mock_func)
    
    # Mock the logging and time functions
    with patch('decorators.log_time.logging.info') as mock_logging, \
         patch('decorators.log_time.time.time', side_effect=[100, 105]):  # Start time, end time
        
        # Call the decorated function
        result = decorated_func("arg1", kwarg1="value1")
        
        # Verify the result
        assert result == "test result"
        
        # Verify that the original function was called with the correct arguments
        mock_func.assert_called_once_with("arg1", kwarg1="value1")
        
        # Verify that logging.info was called twice (start and end)
        assert mock_logging.call_count == 2
        
        # Verify the content of the log messages
        start_call_args = mock_logging.call_args_list[0][0]
        assert "mock_func: Start" in start_call_args[0]
        
        end_call_args = mock_logging.call_args_list[1][0]
        assert "mock_func: End" in end_call_args[0]
        assert "Execution time: 5.0000 seconds" in end_call_args[0]

# Test log_time_async decorator
@pytest.mark.asyncio
async def test_log_time_async():
    # Create a mock async function to decorate
    async def mock_async_func(*args, **kwargs):
        return "async test result"
    
    mock_async_func.__name__ = "mock_async_func"
    
    # Apply the decorator
    decorated_func = log_time_async(mock_async_func)
    
    # Mock the logging and time functions
    with patch('decorators.log_time.logging.info') as mock_logging, \
         patch('decorators.log_time.time.time', side_effect=[200, 207]):  # Start time, end time
        
        # Call the decorated function
        result = await decorated_func("arg1", kwarg1="value1")
        
        # Verify the result
        assert result == "async test result"
        
        # Verify that logging.info was called twice (start and end)
        assert mock_logging.call_count == 2
        
        # Verify the content of the log messages
        start_call_args = mock_logging.call_args_list[0][0]
        assert "mock_async_func: Start" in start_call_args[0]
        
        end_call_args = mock_logging.call_args_list[1][0]
        assert "mock_async_func: End" in end_call_args[0]
        assert "Execution time: 7.0000 seconds" in end_call_args[0]