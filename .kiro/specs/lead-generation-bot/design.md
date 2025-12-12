# Design Document

## Overview

The Lead Generation Bot is a Python-based automation system that generates qualified business leads by searching Google Maps, applying quality filters, removing duplicates, and storing results in both Google Sheets and local CSV files. The system is designed to run unattended on a daily schedule, continuously building a database of potential sales prospects.

The architecture follows a modular pipeline design where each stage (query generation, scraping, filtering, deduplication, storage) is isolated into separate modules. This enables independent testing, easy maintenance, and future extensibility.

## Architecture

### High-Level Architecture

```
┌─────────────────┐
│   Scheduler     │ (cron / Task Scheduler)
│  (Daily 9 AM)   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│                    Main Orchestrator                     │
│                      (main.py)                           │
└─────────────────────────────────────────────────────────┘
         │
         ├──► Load Configuration (config.py)
         │
         ├──► Generate Queries (queries.py)
         │         │
         │         ▼
         ├──► Scrape Google Maps (scraper.py)
         │         │ via SerpAPI
         │         ▼
         ├──► Filter Results (filters.py)
         │         │ Rating ≥ 4.0
         │         │ Reviews ≥ 20
         │         │ No Website
         │         ▼
         ├──► Check Duplicates (dedupe.py)
         │         │ Place ID lookup
         │         ▼
         ├──► Store Leads (storage.py)
         │         ├──► Google Sheets
         │         └──► Local CSV
         │
         └──► Log Results (logging)
```

### Technology Stack

- **Language**: Python 3.10+
- **External APIs**:
  - SerpAPI (Google Maps search)
  - Google Sheets API v4
- **Key Libraries**:
  - `serpapi` - SerpAPI Python client
  - `gspread` - Google Sheets Python API
  - `oauth2client` - Google authentication
  - `pandas` - Data manipulation (optional)
  - `python-dotenv` - Environment variable management
- **Storage**:
  - Google Sheets (primary collaborative storage)
  - CSV files (local backup)
  - Text file (processed Place IDs)
- **Scheduler**:
  - Unix/Linux: cron
  - Windows: Task Scheduler

## Components and Interfaces

### 1. Configuration Module (`config.py`)

**Responsibility**: Load and validate all configuration settings from JSON file and environment variables.

**Interface**:
```python
def load_config() -> dict:
    """Load configuration from settings.json and environment variables."""
    pass

# Exported constants
SERPAPI_KEY: str
GOOGLE_SHEET_ID: str
GOOGLE_SERVICE_ACCOUNT_JSON: str
MIN_RATING: float
MIN_REVIEWS: int
MAX_LEADS_PER_RUN: int
```

**Configuration File Structure** (`config/settings.json`):
```json
{
  "SERPAPI_KEY": "your_serpapi_key",
  "GOOGLE_SHEET_ID": "your_sheet_id",
  "GOOGLE_SERVICE_ACCOUNT_JSON": "config/service_account.json",
  "MIN_RATING": 4.0,
  "MIN_REVIEWS": 20,
  "MAX_LEADS_PER_RUN": 50
}
```

### 2. Queries Module (`queries.py`)

**Responsibility**: Define cities and business categories, generate search queries.

**Interface**:
```python
CITIES: list[str]  # List of "City, Country" strings
CATEGORIES: list[str]  # List of business categories

def generate_queries() -> list[str]:
    """Generate all city × category query combinations."""
    pass
```

**Data**:
- Cities: Delhi, Gurgaon, Noida, Jaipur, Mumbai, Bangalore, Dubai, London, Toronto, etc.
- Categories: baby care, day care centre, cleaning services, salon, gym, law firm, etc.

### 3. Scraper Module (`scraper.py`)

**Responsibility**: Interface with SerpAPI to fetch Google Maps search results.

**Interface**:
```python
def search_places(query: str) -> list[dict]:
    """
    Search Google Maps via SerpAPI for the given query.
    
    Args:
        query: Search string (e.g., "day care in Gurgaon, India")
    
    Returns:
        List of business dictionaries from SerpAPI local_results
    """
    pass
```

**SerpAPI Request Parameters**:
```python
{
    "engine": "google_maps",
    "q": query,
    "type": "search",
    "api_key": SERPAPI_KEY
}
```

**Error Handling**:
- Network timeouts: Retry up to 3 times with exponential backoff
- API rate limits: Log error and skip query
- Invalid API key: Terminate with clear error message

### 4. Filters Module (`filters.py`)

**Responsibility**: Apply quality filters and transform raw API data into structured lead records.

**Interface**:
```python
def is_good_lead(place: dict) -> bool:
    """
    Determine if a business meets quality criteria.
    
    Criteria:
    - Rating ≥ 4.0
    - Reviews ≥ 20
    - No website present
    """
    pass

def transform_place(place: dict, query: str) -> dict:
    """
    Transform SerpAPI place data into structured lead record.
    
    Returns lead dictionary with all required fields.
    """
    pass
```

**Lead Record Structure**:
```python
{
    "business_name": str,
    "category": str,
    "city": str,
    "state": str | None,
    "country": str,
    "rating": float,
    "reviews_count": int,
    "phone": str | None,
    "website_url": str | None,
    "has_website": bool,
    "maps_url": str,
    "place_id": str,
    "created_at": str,  # ISO 8601 timestamp
    "source_query": str,
    "status": str  # "Not Contacted"
}
```

### 5. Deduplication Module (`dedupe.py`)

**Responsibility**: Track processed Place IDs to prevent duplicate leads.

**Interface**:
```python
def load_seen_ids(path: str = "data/processed_ids.txt") -> set[str]:
    """Load previously processed Place IDs from file."""
    pass

def save_seen_ids(ids: set[str], path: str = "data/processed_ids.txt") -> None:
    """Append new Place IDs to the processed IDs file."""
    pass
```

**Storage Format**: Plain text file with one Place ID per line.

### 6. Storage Module (`storage.py`)

**Responsibility**: Persist leads to Google Sheets and local CSV.

**Interface**:
```python
def get_sheet() -> gspread.Worksheet:
    """Authenticate and return Google Sheets worksheet object."""
    pass

def append_to_sheet(leads: list[dict]) -> None:
    """Append lead rows to Google Sheet."""
    pass

def append_to_csv(leads: list[dict], path: str = "data/all_leads.csv") -> None:
    """Append leads to local CSV file."""
    pass
```

**Google Sheets Authentication**:
- Service account JSON key file
- Scopes: `spreadsheets` and `drive`
- Sheet must be shared with service account email (Editor access)

**CSV Format**: UTF-8 encoded with headers matching lead record fields.

### 7. Main Orchestrator (`main.py`)

**Responsibility**: Execute the complete lead generation workflow.

**Workflow**:
1. Load configuration
2. Initialize logging
3. Load previously processed Place IDs
4. Generate search queries
5. For each query:
   - Fetch results from SerpAPI
   - Filter results
   - Check for duplicates
   - Add qualified leads to collection
   - Stop if MAX_LEADS_PER_RUN reached
6. Store leads to Google Sheets and CSV
7. Save new Place IDs
8. Log execution summary

**Interface**:
```python
def run() -> None:
    """Execute the complete lead generation workflow."""
    pass

if __name__ == "__main__":
    run()
```

## Data Models

### Lead Record

The core data structure representing a qualified business lead.

**Fields**:
- `business_name` (str): Name of the business
- `category` (str): Business type/category
- `city` (str): City name
- `state` (str | None): State/province (may be null for some countries)
- `country` (str): Country name
- `rating` (float): Google Maps rating (0.0 - 5.0)
- `reviews_count` (int): Number of Google reviews
- `phone` (str | None): Phone number if available
- `website_url` (str | None): Website URL if present (should be None for qualified leads)
- `has_website` (bool): Flag indicating website presence
- `maps_url` (str): Google Maps URL for the business
- `place_id` (str): Unique Google Maps Place ID
- `created_at` (str): ISO 8601 timestamp when lead was created
- `source_query` (str): Original search query that found this lead
- `status` (str): Lead status ("Not Contacted", "Contacted", "Interested", "Closed")

### Configuration Schema

**Fields**:
- `SERPAPI_KEY` (str): SerpAPI authentication key
- `GOOGLE_SHEET_ID` (str): Google Sheets document ID
- `GOOGLE_SERVICE_ACCOUNT_JSON` (str): Path to service account JSON key
- `MIN_RATING` (float): Minimum rating threshold (default: 4.0)
- `MIN_REVIEWS` (int): Minimum review count threshold (default: 20)
- `MAX_LEADS_PER_RUN` (int): Maximum leads to generate per execution (default: 50)

### Processed IDs Storage

**Format**: Plain text file, one Place ID per line
**Purpose**: Deduplication across multiple executions
**Location**: `data/processed_ids.txt`

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Query generation produces cartesian product

*For any* list of N cities and M categories, the query generation function should produce exactly N × M unique queries, where each query is a unique combination of one city and one category.

**Validates: Requirements 1.1**

### Property 2: API requests include correct parameters

*For any* generated query string, when submitted to the scraper, the resulting SerpAPI request should include the "google_maps" engine parameter and the exact query string.

**Validates: Requirements 1.2**

### Property 3: Scraper extracts local results

*For any* valid SerpAPI response containing a "local_results" field, the scraper should extract and return the contents of that field as a list.

**Validates: Requirements 1.3**

### Property 4: Query failures don't halt processing

*For any* list of queries where some queries fail, the system should continue processing all remaining queries and return results from successful queries.

**Validates: Requirements 1.5**

### Property 5: Filter rejects unqualified businesses

*For any* business record, the filter should reject it if any of these conditions are true: rating < 4.0, reviews < 20, or website URL is present. The filter should accept it only if all conditions are met: rating ≥ 4.0, reviews ≥ 20, and no website.

**Validates: Requirements 2.1, 2.2, 2.3**

### Property 6: Transformation produces complete lead records

*For any* business that passes filtering, the transformation function should produce a lead record containing all required fields (business_name, category, city, state, country, rating, reviews_count, phone, website_url, has_website, maps_url, place_id, created_at, source_query, status) with appropriate types.

**Validates: Requirements 2.4**

### Property 7: Processed IDs are loaded at startup

*For any* processed IDs file containing a set of Place IDs, loading the file should return a set containing exactly those Place IDs.

**Validates: Requirements 3.1**

### Property 8: Duplicate Place IDs are skipped

*For any* business with a Place ID that exists in the processed IDs set, the deduplication check should return false (skip), and for any business with a Place ID not in the set, it should return true (process).

**Validates: Requirements 3.2**

### Property 9: New Place IDs are added to collection

*For any* lead that is successfully stored, its Place ID should be added to the processed IDs collection.

**Validates: Requirements 3.3**

### Property 10: Place ID persistence round-trip

*For any* set of Place IDs, saving them to storage and then loading from storage should return an equivalent set containing all the original Place IDs.

**Validates: Requirements 3.4**

### Property 11: Sheet rows contain all required fields

*For any* lead appended to Google Sheets, the resulting row should contain all required columns (business_name, category, city, state, country, rating, reviews_count, phone, website_url, has_website, maps_url, place_id, created_at, source_query, status) with the status field set to "Not Contacted".

**Validates: Requirements 4.3, 4.4**

### Property 12: Sheet API failures are logged and handled

*For any* Google Sheets API call that fails, the system should log an error message containing exception details and continue execution without terminating.

**Validates: Requirements 4.5**

### Property 13: CSV append preserves data

*For any* list of leads appended to a CSV file, reading the CSV file should return all the appended leads with all fields intact, encoded in UTF-8.

**Validates: Requirements 5.1, 5.3, 5.4**

### Property 14: CSV write failures are logged and handled

*For any* CSV write operation that fails, the system should log an error message and continue execution without terminating.

**Validates: Requirements 5.5**

### Property 15: Lead limit is enforced

*For any* execution with a configured maximum limit of N leads, the system should generate no more than N leads, counting only leads that pass filtering and deduplication.

**Validates: Requirements 6.2, 6.5**

### Property 16: Limit reached terminates search

*For any* execution where the lead limit is reached, the system should stop processing additional queries and proceed directly to storage operations.

**Validates: Requirements 6.3**

### Property 17: Execution summary reports correct counts

*For any* completed execution, the output summary should report the actual number of new leads added, matching the count of leads stored.

**Validates: Requirements 7.2**

### Property 18: Errors are logged with details

*For any* error that occurs during execution, the system should write a log entry containing the error message and full exception details.

**Validates: Requirements 7.3**

### Property 19: Configuration loads all required fields

*For any* valid configuration file containing all required fields (SERPAPI_KEY, GOOGLE_SHEET_ID, GOOGLE_SERVICE_ACCOUNT_JSON, MIN_RATING, MIN_REVIEWS, MAX_LEADS_PER_RUN), the configuration loader should successfully load and return all field values.

**Validates: Requirements 8.1**

### Property 20: Invalid configuration produces descriptive errors

*For any* configuration file with missing or invalid required fields, the configuration loader should raise an exception with a descriptive error message indicating which field is problematic.

**Validates: Requirements 8.4**

### Property 21: Log entries include ISO 8601 timestamps

*For any* log entry written during execution, the entry should contain a valid ISO 8601 formatted timestamp.

**Validates: Requirements 10.1**

### Property 22: Error logs include exception details

*For any* error that is logged, the log entry should contain the exception type, message, and stack trace.

**Validates: Requirements 10.2**

### Property 23: Execution summary logs all metrics

*For any* completed execution cycle, the final log entry should include counts for queries processed, leads found, leads filtered out, and leads stored.

**Validates: Requirements 10.3**

### Property 24: Log files are named by date

*For any* execution on a given date, log entries should be written to a file whose name contains that date in a consistent format.

**Validates: Requirements 10.4**

## Error
 Handling

### Error Categories

**1. Configuration Errors** (Fatal - Terminate Execution)
- Missing configuration file
- Invalid JSON syntax in configuration
- Missing required configuration fields
- Invalid service account JSON file
- Invalid Google Sheet ID

**Strategy**: Validate all configuration at startup. Fail fast with clear error messages indicating exactly what is wrong and how to fix it.

**2. Authentication Errors** (Fatal - Terminate Execution)
- Invalid SerpAPI key
- Invalid Google service account credentials
- Insufficient Google Sheets permissions

**Strategy**: Attempt authentication during initialization. If authentication fails, log the error with details and terminate with instructions for the user.

**3. Network Errors** (Recoverable - Retry)
- SerpAPI timeout
- SerpAPI rate limit exceeded
- Google Sheets API timeout
- Network connectivity issues

**Strategy**: 
- Implement exponential backoff retry (3 attempts)
- Log each retry attempt
- If all retries fail, log error and skip the current operation
- Continue with remaining operations

**4. Data Errors** (Recoverable - Skip)
- Malformed SerpAPI response
- Missing required fields in business data
- Invalid Place ID format

**Strategy**: Log the error with the problematic data, skip the current item, and continue processing remaining items.

**5. Storage Errors** (Recoverable - Log and Continue)
- CSV write failure (disk full, permissions)
- Google Sheets append failure

**Strategy**: Log the error with full details. The system should continue execution since one storage mechanism may succeed even if the other fails.

### Error Logging Format

All errors should be logged with:
- ISO 8601 timestamp
- Error severity level (ERROR, WARNING, INFO)
- Component/module name
- Error message
- Exception type and stack trace (for exceptions)
- Context data (e.g., query being processed, Place ID)

Example:
```
2025-12-02T09:15:23.456Z [ERROR] scraper.py - SerpAPI request failed for query "day care in Gurgaon"
Exception: requests.exceptions.Timeout
Retrying in 2 seconds (attempt 1/3)
```

## Testing Strategy

The Lead Generation Bot will be tested using a dual approach combining unit tests for specific scenarios and property-based tests for universal correctness properties.

### Unit Testing

**Framework**: `pytest`

**Coverage Areas**:
1. **Configuration Loading**
   - Valid configuration file loads correctly
   - Missing file raises appropriate error
   - Invalid JSON raises appropriate error
   - Missing required fields raises appropriate error

2. **Query Generation**
   - Empty city list produces empty queries
   - Empty category list produces empty queries
   - Single city and category produces one query

3. **Filtering Edge Cases**
   - Business with exactly 4.0 rating passes
   - Business with exactly 20 reviews passes
   - Business with null website passes
   - Business with empty string website is handled correctly

4. **Deduplication Edge Cases**
   - Loading from non-existent file returns empty set
   - Saving to new file creates file
   - Appending to existing file preserves previous IDs

5. **Storage Edge Cases**
   - CSV creation with headers when file doesn't exist
   - CSV append without headers when file exists
   - Google Sheets authentication with valid credentials

6. **Error Handling**
   - Network timeout triggers retry
   - Max retries exceeded logs error and continues
   - Invalid API response is logged and skipped

### Property-Based Testing

**Framework**: `hypothesis` (Python property-based testing library)

**Configuration**: Each property test should run a minimum of 100 iterations to ensure thorough coverage of the input space.

**Test Tagging**: Each property-based test must include a comment explicitly referencing the correctness property from the design document using this format:
```python
# Feature: lead-generation-bot, Property 1: Query generation produces cartesian product
```

**Coverage Areas**:

1. **Query Generation (Property 1)**
   - Generate random lists of cities and categories
   - Verify output count equals N × M
   - Verify all combinations are present and unique

2. **Filtering (Property 5)**
   - Generate random business records with varying ratings, reviews, and website presence
   - Verify filter correctly accepts/rejects based on all criteria

3. **Transformation (Property 6)**
   - Generate random valid business data
   - Verify transformed lead contains all required fields
   - Verify field types are correct

4. **Deduplication (Property 8)**
   - Generate random Place IDs and processed ID sets
   - Verify businesses with matching IDs are skipped
   - Verify businesses with new IDs are processed

5. **Place ID Persistence (Property 10)**
   - Generate random sets of Place IDs
   - Save and reload
   - Verify all IDs are preserved (round-trip property)

6. **Lead Limit Enforcement (Property 15)**
   - Generate random lead limits and result sets
   - Verify exactly limit number of leads are processed
   - Verify only qualified leads count toward limit

7. **CSV Round-Trip (Property 13)**
   - Generate random lead records
   - Write to CSV and read back
   - Verify all data is preserved with correct encoding

8. **Configuration Loading (Property 19)**
   - Generate random valid configuration dictionaries
   - Verify all fields are correctly loaded

9. **Log Timestamp Format (Property 21)**
   - Execute random operations
   - Verify all log entries contain valid ISO 8601 timestamps

10. **Error Logging (Property 22)**
    - Trigger random errors
    - Verify log entries contain exception type, message, and stack trace

### Integration Testing

**Scope**: End-to-end workflow testing with mocked external services

**Test Scenarios**:
1. Complete execution with mocked SerpAPI and Google Sheets
2. Execution with some query failures
3. Execution hitting lead limit mid-processing
4. Execution with duplicate Place IDs
5. Execution with storage failures

**Mocking Strategy**:
- Mock SerpAPI responses with realistic test data
- Mock Google Sheets API to verify correct data is sent
- Use temporary files for CSV and processed IDs storage

### Test Data Generators

For property-based testing, implement smart generators that produce realistic test data:

**Business Generator**:
```python
@st.composite
def business_strategy(draw):
    return {
        "title": draw(st.text(min_size=1, max_size=100)),
        "rating": draw(st.floats(min_value=0.0, max_value=5.0)),
        "reviews": draw(st.integers(min_value=0, max_value=10000)),
        "type": draw(st.sampled_from(CATEGORIES)),
        "address": draw(st.text(min_size=10)),
        "phone": draw(st.one_of(st.none(), st.text())),
        "website": draw(st.one_of(st.none(), st.text(min_size=10))),
        "place_id": draw(st.text(min_size=20, max_size=50)),
        "gps_coordinates": {"link": draw(st.text())}
    }
```

**Configuration Generator**:
```python
@st.composite
def config_strategy(draw):
    return {
        "SERPAPI_KEY": draw(st.text(min_size=20)),
        "GOOGLE_SHEET_ID": draw(st.text(min_size=40)),
        "GOOGLE_SERVICE_ACCOUNT_JSON": draw(st.text()),
        "MIN_RATING": draw(st.floats(min_value=0.0, max_value=5.0)),
        "MIN_REVIEWS": draw(st.integers(min_value=0, max_value=100)),
        "MAX_LEADS_PER_RUN": draw(st.integers(min_value=1, max_value=1000))
    }
```

### Testing Best Practices

1. **Isolation**: Each test should be independent and not rely on external state
2. **Cleanup**: Use pytest fixtures to create and cleanup temporary files
3. **Mocking**: Mock external API calls to avoid rate limits and costs during testing
4. **Assertions**: Use descriptive assertion messages
5. **Coverage**: Aim for >80% code coverage, with 100% coverage of critical paths (filtering, deduplication, storage)

## Performance Considerations

### Expected Performance

- **Query Processing**: 1-2 seconds per query (SerpAPI latency)
- **Filtering**: <1ms per business
- **Deduplication**: O(1) lookup with set-based storage
- **CSV Write**: <10ms for 50 leads
- **Google Sheets Append**: 1-2 seconds for batch of 50 leads
- **Total Execution Time**: 5-10 minutes for 50 leads (dominated by API calls)

### Scalability

**Current Design Limits**:
- 50 leads/day = 1,500 leads/month
- ~100 API calls/day (assuming 2-3 leads per query)
- Single-threaded execution

**Scaling Options** (Future Enhancements):
1. **Parallel Query Processing**: Use `concurrent.futures` to process multiple queries simultaneously
2. **Pagination**: Fetch more results per query using SerpAPI pagination
3. **Batch Processing**: Increase MAX_LEADS_PER_RUN to 100-500
4. **Multiple Sheets**: Separate sheets per country/region for better organization
5. **Database Storage**: Replace CSV with SQLite or PostgreSQL for better query performance

### Resource Requirements

- **Memory**: <100MB (storing ~1000 Place IDs in memory)
- **Disk**: ~1MB per 1000 leads (CSV storage)
- **Network**: ~10MB per execution (API requests/responses)
- **CPU**: Minimal (I/O bound, not CPU bound)

## Deployment

### Prerequisites

1. **Python Environment**:
   - Python 3.10 or higher
   - Virtual environment recommended

2. **API Accounts**:
   - SerpAPI account with active subscription
   - Google Cloud project with Sheets API enabled
   - Service account with JSON key downloaded

3. **Google Sheets Setup**:
   - Create new Google Sheet
   - Share sheet with service account email (Editor access)
   - Copy Sheet ID from URL

### Installation Steps

1. Clone repository and create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure settings:
```bash
cp config/settings.example.json config/settings.json
# Edit settings.json with your API keys and configuration
```

4. Create directory structure:
```bash
mkdir -p data logs
```

5. Test execution:
```bash
python src/main.py
```

### Scheduler Setup

**Unix/Linux (cron)**:
```bash
crontab -e
# Add line:
0 9 * * * /path/to/venv/bin/python /path/to/lead-machine/src/main.py >> /path/to/lead-machine/logs/cron.log 2>&1
```

**Windows (Task Scheduler)**:
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 9:00 AM
4. Action: Start a program
5. Program: `C:\path\to\venv\Scripts\python.exe`
6. Arguments: `C:\path\to\lead-machine\src\main.py`
7. Start in: `C:\path\to\lead-machine`

### Monitoring

**Daily Checks**:
- Review log files in `logs/` directory
- Check Google Sheet for new leads
- Verify `data/processed_ids.txt` is growing
- Monitor SerpAPI usage dashboard

**Weekly Checks**:
- Review lead quality (ratings, reviews)
- Check for duplicate leads (shouldn't happen, but verify)
- Analyze which cities/categories produce best leads
- Adjust MIN_RATING, MIN_REVIEWS if needed

**Monthly Checks**:
- Review SerpAPI costs vs. lead value
- Consider expanding city/category lists
- Archive old logs
- Backup CSV files

## Future Enhancements

### Phase 2: Outreach Automation
- Email finder integration (Hunter.io, Apollo.io)
- Automated email campaign generation
- WhatsApp Business API integration
- CRM integration (HubSpot, Salesforce)

### Phase 3: Intelligence Layer
- AI-powered lead scoring
- Personalized outreach message generation
- Website analysis for pain point identification
- Competitor analysis

### Phase 4: Multi-Channel
- LinkedIn profile enrichment
- Social media presence detection
- Review sentiment analysis
- Business growth indicators

### Phase 5: Scale
- Multi-region deployment
- Real-time lead generation
- Webhook notifications for new leads
- Team collaboration features
