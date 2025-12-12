# Implementation Plan

- [x] 1. Set up project structure and dependencies
  - Create directory structure: `config/`, `data/`, `logs/`, `src/`
  - Create `requirements.txt` with dependencies: `serpapi`, `gspread`, `oauth2client`, `python-dotenv`, `pytest`, `hypothesis`
  - Create `config/settings.example.json` template
  - Create `.gitignore` to exclude sensitive files and data directories
  - _Requirements: 9.1_

- [x] 2. Implement configuration module
  - Write `src/config.py` to load settings from JSON file
  - Implement validation for all required configuration fields
  - Export configuration constants for use by other modules
  - _Requirements: 8.1, 8.2, 8.4_

- [x] 2.1 Write property test for configuration loading
  - **Property 19: Configuration loads all required fields**
  - **Validates: Requirements 8.1**

- [x] 2.2 Write property test for invalid configuration handling
  - **Property 20: Invalid configuration produces descriptive errors**
  - **Validates: Requirements 8.4**

- [x] 2.3 Write unit tests for configuration edge cases
  - Test missing configuration file error
  - Test invalid JSON syntax error
  - Test environment variable fallback
  - _Requirements: 8.3, 8.5_

- [x] 3. Implement queries module
  - Create `src/queries.py` with predefined city and category lists
  - Implement `generate_queries()` function to create cartesian product
  - _Requirements: 1.1, 1.4_

- [x] 3.1 Write property test for query generation
  - **Property 1: Query generation produces cartesian product**
  - **Validates: Requirements 1.1**

- [x] 3.2 Write unit tests for query generation edge cases
  - Test empty city list
  - Test empty category list
  - Test single city and category
  - _Requirements: 1.1_

- [x] 4. Implement scraper module
  - Create `src/scraper.py` with SerpAPI integration
  - Implement `search_places()` function to query Google Maps
  - Add retry logic with exponential backoff for network errors
  - Extract local_results from API response
  - _Requirements: 1.2, 1.3, 1.5_

- [x] 4.1 Write property test for API parameter formatting
  - **Property 2: API requests include correct parameters**
  - **Validates: Requirements 1.2**

- [x] 4.2 Write property test for result extraction
  - **Property 3: Scraper extracts local results**
  - **Validates: Requirements 1.3**

- [x] 4.3 Write property test for error resilience
  - **Property 4: Query failures don't halt processing**
  - **Validates: Requirements 1.5**

- [x] 4.4 Write unit tests for scraper error handling
  - Test network timeout with retry
  - Test API rate limit handling
  - Test malformed response handling
  - _Requirements: 1.5_

- [x] 5. Implement filters module
  - Create `src/filters.py` with filtering and transformation logic
  - Implement `is_good_lead()` function to check rating, reviews, and website criteria
  - Implement `transform_place()` function to convert API data to lead record structure
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [x] 5.1 Write property test for filtering logic
  - **Property 5: Filter rejects unqualified businesses**
  - **Validates: Requirements 2.1, 2.2, 2.3**

- [x] 5.2 Write property test for transformation completeness
  - **Property 6: Transformation produces complete lead records**
  - **Validates: Requirements 2.4**

- [x] 5.3 Write unit tests for filter edge cases
  - Test business with exactly 4.0 rating
  - Test business with exactly 20 reviews
  - Test business with null vs empty string website
  - _Requirements: 2.1, 2.2, 2.3_

- [x] 6. Implement deduplication module
  - Create `src/dedupe.py` with Place ID tracking
  - Implement `load_seen_ids()` function to read from file
  - Implement `save_seen_ids()` function to append to file
  - Handle missing file gracefully by returning empty set
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 6.1 Write property test for Place ID loading
  - **Property 7: Processed IDs are loaded at startup**
  - **Validates: Requirements 3.1**

- [x] 6.2 Write property test for deduplication logic
  - **Property 8: Duplicate Place IDs are skipped**
  - **Validates: Requirements 3.2**

- [x] 6.3 Write property test for Place ID collection update
  - **Property 9: New Place IDs are added to collection**
  - **Validates: Requirements 3.3**

- [x] 6.4 Write property test for Place ID persistence
  - **Property 10: Place ID persistence round-trip**
  - **Validates: Requirements 3.4**

- [x] 6.5 Write unit test for missing file handling
  - Test that non-existent file returns empty set
  - _Requirements: 3.5_

- [ ] 7. Implement storage module
  - Create `src/storage.py` with Google Sheets and CSV storage
  - Implement `get_sheet()` function for Google Sheets authentication
  - Implement `append_to_sheet()` function to write leads to Google Sheets
  - Implement `append_to_csv()` function to write leads to CSV with UTF-8 encoding
  - Add error handling for storage failures (log and continue)
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ] 7.1 Write property test for Google Sheets row structure
  - **Property 11: Sheet rows contain all required fields**
  - **Validates: Requirements 4.3, 4.4**

- [ ] 7.2 Write property test for Google Sheets error handling
  - **Property 12: Sheet API failures are logged and handled**
  - **Validates: Requirements 4.5**

- [ ] 7.3 Write property test for CSV round-trip
  - **Property 13: CSV append preserves data**
  - **Validates: Requirements 5.1, 5.3, 5.4**

- [ ] 7.4 Write property test for CSV error handling
  - **Property 14: CSV write failures are logged and handled**
  - **Validates: Requirements 5.5**

- [ ] 7.5 Write unit tests for storage edge cases
  - Test CSV creation with headers when file doesn't exist
  - Test CSV append without headers when file exists
  - Test Google Sheets authentication with valid credentials
  - _Requirements: 5.2, 4.1_

- [ ] 8. Implement logging infrastructure
  - Set up Python logging with ISO 8601 timestamps
  - Configure daily log file rotation with date-based naming
  - Implement error logging with full exception details
  - Add execution summary logging with all metrics
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 8.1 Write property test for log timestamp format
  - **Property 21: Log entries include ISO 8601 timestamps**
  - **Validates: Requirements 10.1**

- [ ] 8.2 Write property test for error log completeness
  - **Property 22: Error logs include exception details**
  - **Validates: Requirements 10.2**

- [ ] 8.3 Write property test for execution summary logging
  - **Property 23: Execution summary logs all metrics**
  - **Validates: Requirements 10.3**

- [ ] 8.4 Write property test for log file naming
  - **Property 24: Log files are named by date**
  - **Validates: Requirements 10.4**

- [ ] 9. Implement main orchestrator
  - Create `src/main.py` with complete workflow orchestration
  - Load configuration and initialize logging
  - Load previously processed Place IDs
  - Generate and process queries with lead limit enforcement
  - Store qualified leads to both Google Sheets and CSV
  - Save newly processed Place IDs
  - Output execution summary
  - _Requirements: 1.1, 6.1, 6.2, 6.3, 6.5, 7.2_

- [ ] 9.1 Write property test for lead limit enforcement
  - **Property 15: Lead limit is enforced**
  - **Validates: Requirements 6.2, 6.5**

- [ ] 9.2 Write property test for limit termination behavior
  - **Property 16: Limit reached terminates search**
  - **Validates: Requirements 6.3**

- [ ] 9.3 Write property test for execution summary accuracy
  - **Property 17: Execution summary reports correct counts**
  - **Validates: Requirements 7.2**

- [ ] 9.4 Write property test for error logging during execution
  - **Property 18: Errors are logged with details**
  - **Validates: Requirements 7.3**

- [ ] 10. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. Create integration tests
  - Write end-to-end test with mocked SerpAPI and Google Sheets
  - Test execution with query failures
  - Test execution hitting lead limit mid-processing
  - Test execution with duplicate Place IDs
  - Test execution with storage failures
  - _Requirements: All_

- [ ] 12. Create deployment documentation
  - Write README.md with setup instructions
  - Document API account setup (SerpAPI, Google Cloud)
  - Document Google Sheets configuration
  - Document scheduler setup for cron and Task Scheduler
  - Add troubleshooting guide
  - _Requirements: 7.4, 7.5_

- [ ] 13. Final checkpoint - Verify complete system
  - Run full execution with real API keys (limited test)
  - Verify leads appear in Google Sheets
  - Verify CSV backup is created
  - Verify deduplication works across multiple runs
  - Verify logs are generated correctly
  - Ensure all tests pass, ask the user if questions arise.
