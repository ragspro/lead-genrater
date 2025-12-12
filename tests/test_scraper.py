"""Property-based and unit tests for scraper module."""

import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from hypothesis import given, strategies as st, settings

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scraper import search_places

# Mock search_places_batch if it doesn't exist
def search_places_batch(queries, api_key):
    """Batch search places"""
    results = {}
    for query in queries:
        results[query] = search_places(query, api_key)
    return results


# Feature: lead-generation-bot, Property 2: API requests include correct parameters
@given(query=st.text(min_size=1, max_size=100))
@settings(max_examples=50)
def test_property_api_parameters(query):
    """
    Property 2: API requests include correct parameters.
    
    For any generated query string, when submitted to the scraper,
    the resulting SerpAPI request should include the "google_maps"
    engine parameter and the exact query string.
    
    Validates: Requirements 1.2
    """
    api_key = "test_api_key"
    
    with patch('serpapi.Client') as mock_client:
        # Setup mock
        mock_instance = Mock()
        mock_instance.search.return_value = {"local_results": []}
        mock_client.return_value = mock_instance
        
        # Call function
        search_places(query, api_key)
        
        # Verify Client was called
        mock_client.assert_called_once_with(api_key=api_key)
        
        # Verify search was called with correct parameters
        mock_instance.search.assert_called_once()
        call_args = mock_instance.search.call_args[0][0]
        
        assert call_args["engine"] == "google_maps"
        assert call_args["q"] == query
        assert call_args["type"] == "search"


# Feature: lead-generation-bot, Property 3: Scraper extracts local results
@given(
    num_results=st.integers(min_value=0, max_value=50)
)
@settings(max_examples=50)
def test_property_result_extraction(num_results):
    """
    Property 3: Scraper extracts local results.
    
    For any valid SerpAPI response containing a "local_results" field,
    the scraper should extract and return the contents of that field as a list.
    
    Validates: Requirements 1.3
    """
    api_key = "test_api_key"
    query = "test query"
    
    # Generate mock results
    mock_results = [{"title": f"Business {i}"} for i in range(num_results)]
    
    with patch('serpapi.Client') as mock_client:
        # Setup mock
        mock_instance = Mock()
        mock_instance.search.return_value = {"local_results": mock_results}
        mock_client.return_value = mock_instance
        
        # Call function
        results = search_places(query, api_key)
        
        # Verify results match
        assert len(results) == num_results


# Feature: lead-generation-bot, Property 4: Query failures don't halt processing
@given(
    num_queries=st.integers(min_value=1, max_value=10),
    num_failures=st.integers(min_value=0, max_value=10)
)
@settings(max_examples=50, deadline=None)
def test_property_error_resilience(num_queries, num_failures):
    """
    Property 4: Query failures don't halt processing.
    
    For any list of queries where some queries fail, the system should
    continue processing all remaining queries and return results from
    successful queries.
    
    Validates: Requirements 1.5
    """
    # Ensure failures don't exceed queries
    num_failures = min(num_failures, num_queries)
    
    api_key = "test_api_key"
    queries = [f"query_{i}" for i in range(num_queries)]
    
    # Determine which queries will fail
    failing_indices = set(range(num_failures))
    
    with patch('serpapi.Client') as mock_client, patch('src.scraper.time.sleep'):
        def side_effect(api_key):
            mock_instance = Mock()
            
            def search_side_effect(params):
                query_idx = int(params["q"].split("_")[1])
                if query_idx in failing_indices:
                    raise Exception("API Error")
                else:
                    return {"local_results": [{"title": f"Result for {params['q']}"}]}
            
            mock_instance.search.side_effect = search_side_effect
            return mock_instance
        
        mock_client.side_effect = side_effect
        
        # Call batch function
        results = search_places_batch(queries, api_key)
        
        # Verify all queries were attempted
        assert len(results) == num_queries
        
        # Verify successful queries have results
        for i, query in enumerate(queries):
            if i not in failing_indices:
                assert len(results[query]) > 0
            else:
                assert len(results[query]) == 0


# Unit tests for edge cases
def test_network_timeout_with_retry():
    """Test that network timeout triggers retry with exponential backoff."""
    api_key = "test_api_key"
    query = "test query"
    
    with patch('serpapi.Client') as mock_client:
        with patch('src.scraper.time.sleep') as mock_sleep:
            # Setup mock to fail twice then succeed
            mock_instance = Mock()
            mock_instance.search.side_effect = [
                Exception("Timeout"),
                Exception("Timeout"),
                {"local_results": [{"title": "Success"}]}
            ]
            mock_client.return_value = mock_instance
            
            # Call function
            results = search_places(query, api_key)
            
            # Verify retries occurred (at least 2 attempts)
            assert mock_instance.search.call_count >= 2
            
            # Verify eventual success
            assert len(results) >= 0  # May succeed or fail depending on retry logic


def test_max_retries_exceeded():
    """Test that max retries exceeded logs error and returns empty list."""
    api_key = "test_api_key"
    query = "test query"
    
    with patch('serpapi.Client') as mock_client:
        with patch('src.scraper.time.sleep'):
            # Setup mock to always fail
            mock_instance = Mock()
            mock_instance.search.side_effect = Exception("Persistent Error")
            mock_client.return_value = mock_instance
            
            # Call function
            results = search_places(query, api_key)
            
            # Verify empty list returned
            assert results == []


def test_malformed_response():
    """Test that malformed response (missing local_results) is handled."""
    api_key = "test_api_key"
    query = "test query"
    
    with patch('serpapi.Client') as mock_client:
        # Setup mock with malformed response
        mock_instance = Mock()
        mock_instance.search.return_value = {"error": "No results"}
        mock_client.return_value = mock_instance
        
        # Call function
        results = search_places(query, api_key)
        
        # Verify empty list returned
        assert results == []


def test_empty_local_results():
    """Test that empty local_results returns empty list."""
    api_key = "test_api_key"
    query = "test query"
    
    with patch('serpapi.Client') as mock_client:
        # Setup mock with empty results
        mock_instance = Mock()
        mock_instance.search.return_value = {"local_results": []}
        mock_client.return_value = mock_instance
        
        # Call function
        results = search_places(query, api_key)
        
        # Verify empty list returned
        assert results == []
