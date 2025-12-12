# Requirements Document

## Introduction

The Lead Generation Bot is an automated Python-based system that searches for businesses on Google Maps, filters them based on quality criteria, removes duplicates, and stores qualified leads in Google Sheets. The system runs daily via a scheduler to continuously generate new business leads across multiple cities and business categories.

## Glossary

- **Lead Generation Bot**: The automated Python application that orchestrates the entire lead generation workflow
- **Business Lead**: A business entity that meets the filtering criteria and is stored as a potential sales prospect
- **SerpAPI**: Third-party API service used to query Google Maps search results
- **Google Sheets API**: Google service that enables programmatic read/write access to spreadsheet data
- **Place ID**: Unique identifier assigned by Google Maps to each business location
- **Deduplication**: Process of identifying and removing duplicate business entries based on Place ID
- **Service Account**: Google Cloud authentication mechanism for server-to-server API access
- **Scheduler**: System-level task automation tool (cron on Unix/Linux, Task Scheduler on Windows)
- **Query**: Search string combining a business category and city (e.g., "day care in Gurgaon")

## Requirements

### Requirement 1

**User Story:** As a sales team lead, I want the system to search for businesses across multiple cities and categories, so that I can generate leads from diverse geographic and industry segments.

#### Acceptance Criteria

1. WHEN the Lead Generation Bot executes a search cycle, THE Lead Generation Bot SHALL generate queries by combining each city from a predefined city list with each category from a predefined category list
2. WHEN a query is generated, THE Lead Generation Bot SHALL submit the query to SerpAPI with the Google Maps search engine parameter
3. WHEN SerpAPI returns search results, THE Lead Generation Bot SHALL extract the local business results from the response
4. WHERE the city list contains N cities and the category list contains M categories, THE Lead Generation Bot SHALL generate N × M unique search queries per execution cycle
5. WHEN processing multiple queries, THE Lead Generation Bot SHALL continue processing subsequent queries if an individual query fails

### Requirement 2

**User Story:** As a sales team lead, I want the system to filter businesses based on quality metrics, so that I only receive leads that are likely to be legitimate and responsive businesses.

#### Acceptance Criteria

1. WHEN a business result is evaluated, THE Lead Generation Bot SHALL reject the business if the rating is below 4.0 stars
2. WHEN a business result is evaluated, THE Lead Generation Bot SHALL reject the business if the review count is below 20 reviews
3. WHEN a business result is evaluated, THE Lead Generation Bot SHALL reject the business if a website URL is present in the business data
4. WHEN a business passes all filter criteria, THE Lead Generation Bot SHALL transform the raw API data into a structured lead record
5. WHEN transforming business data, THE Lead Generation Bot SHALL extract business name, category, address components, rating, review count, phone number, maps URL, and Place ID

### Requirement 3

**User Story:** As a sales team lead, I want the system to prevent duplicate leads, so that my team does not waste time contacting the same business multiple times.

#### Acceptance Criteria

1. WHEN the Lead Generation Bot starts execution, THE Lead Generation Bot SHALL load all previously processed Place IDs from persistent storage
2. WHEN evaluating a business result, THE Lead Generation Bot SHALL skip the business if its Place ID exists in the processed IDs collection
3. WHEN a new lead is successfully stored, THE Lead Generation Bot SHALL add the lead's Place ID to the processed IDs collection
4. WHEN the execution cycle completes, THE Lead Generation Bot SHALL persist all newly processed Place IDs to storage
5. WHEN loading processed IDs fails due to missing storage file, THE Lead Generation Bot SHALL initialize an empty collection and continue execution

### Requirement 4

**User Story:** As a sales team lead, I want leads stored in Google Sheets, so that my team can easily access, review, and update lead status in a collaborative environment.

#### Acceptance Criteria

1. WHEN the Lead Generation Bot initializes Google Sheets access, THE Lead Generation Bot SHALL authenticate using a service account JSON key file
2. WHEN new leads are ready for storage, THE Lead Generation Bot SHALL append lead rows to the configured Google Sheet
3. WHEN appending leads to Google Sheets, THE Lead Generation Bot SHALL include columns for business name, category, city, state, country, rating, review count, phone, website URL, has website flag, maps URL, Place ID, creation timestamp, source query, and status
4. WHEN a lead is initially stored, THE Lead Generation Bot SHALL set the status field to "Not Contacted"
5. WHEN Google Sheets API calls fail, THE Lead Generation Bot SHALL log the error and continue execution without terminating

### Requirement 5

**User Story:** As a sales team lead, I want leads backed up locally in CSV format, so that I have a redundant data source independent of Google Sheets availability.

#### Acceptance Criteria

1. WHEN new leads are ready for storage, THE Lead Generation Bot SHALL append lead records to a local CSV file
2. WHEN the CSV file does not exist, THE Lead Generation Bot SHALL create the file and write column headers before appending data
3. WHEN the CSV file exists, THE Lead Generation Bot SHALL append new lead rows without rewriting headers
4. WHEN writing to CSV, THE Lead Generation Bot SHALL use UTF-8 encoding to support international characters
5. WHEN CSV write operations fail, THE Lead Generation Bot SHALL log the error and continue execution

### Requirement 6

**User Story:** As a sales team lead, I want the system to limit the number of leads generated per run, so that I can control API costs and ensure manageable daily lead volumes.

#### Acceptance Criteria

1. WHEN the Lead Generation Bot starts execution, THE Lead Generation Bot SHALL load the maximum leads per run limit from configuration
2. WHEN processing search results, THE Lead Generation Bot SHALL stop adding new leads once the maximum limit is reached
3. WHEN the maximum limit is reached during query processing, THE Lead Generation Bot SHALL terminate the search loop and proceed to storage operations
4. WHERE the maximum limit is configured as 50, THE Lead Generation Bot SHALL generate no more than 50 leads in a single execution
5. WHEN counting leads toward the limit, THE Lead Generation Bot SHALL only count leads that pass all filtering and deduplication checks

### Requirement 7

**User Story:** As a sales team lead, I want the system to run automatically on a daily schedule, so that new leads are generated consistently without manual intervention.

#### Acceptance Criteria

1. WHEN the scheduler triggers the Lead Generation Bot, THE Lead Generation Bot SHALL execute the complete lead generation workflow
2. WHEN execution completes, THE Lead Generation Bot SHALL output a summary of the number of new leads added
3. WHEN errors occur during scheduled execution, THE Lead Generation Bot SHALL log error details to a log file
4. WHERE the system runs on Unix or Linux, THE Lead Generation Bot SHALL support execution via cron scheduler
5. WHERE the system runs on Windows, THE Lead Generation Bot SHALL support execution via Task Scheduler

### Requirement 8

**User Story:** As a system administrator, I want all API keys and configuration stored securely in a configuration file, so that sensitive credentials are not hardcoded in the application source code.

#### Acceptance Criteria

1. WHEN the Lead Generation Bot initializes, THE Lead Generation Bot SHALL load configuration from a JSON settings file
2. WHEN loading configuration, THE Lead Generation Bot SHALL read SerpAPI key, Google Sheet ID, service account file path, minimum rating threshold, minimum review threshold, and maximum leads per run
3. WHEN the configuration file is missing, THE Lead Generation Bot SHALL terminate with a clear error message indicating the missing file
4. WHEN configuration values are invalid or missing required fields, THE Lead Generation Bot SHALL terminate with a descriptive error message
5. WHERE sensitive configuration exists, THE Lead Generation Bot SHALL support loading from environment variables as an alternative to JSON files

### Requirement 9

**User Story:** As a developer, I want the codebase organized into logical modules, so that the system is maintainable and individual components can be tested and modified independently.

#### Acceptance Criteria

1. WHEN the project structure is created, THE Lead Generation Bot SHALL organize code into separate modules for configuration, queries, scraping, filtering, storage, deduplication, and main orchestration
2. WHEN a module is modified, THE Lead Generation Bot SHALL ensure changes do not require modifications to unrelated modules
3. WHEN new business categories or cities are added, THE Lead Generation Bot SHALL require changes only to the queries module
4. WHEN the data source API changes, THE Lead Generation Bot SHALL require changes only to the scraper module
5. WHEN storage destinations change, THE Lead Generation Bot SHALL require changes only to the storage module

### Requirement 10

**User Story:** As a sales team lead, I want execution logs with timestamps, so that I can monitor system performance and troubleshoot issues when lead generation fails.

#### Acceptance Criteria

1. WHEN the Lead Generation Bot executes any operation, THE Lead Generation Bot SHALL write log entries with ISO 8601 timestamps
2. WHEN errors occur, THE Lead Generation Bot SHALL log error messages with full exception details
3. WHEN the execution cycle completes, THE Lead Generation Bot SHALL log the total number of queries processed, leads found, leads filtered out, and leads stored
4. WHEN writing logs, THE Lead Generation Bot SHALL append to daily log files named with the execution date
5. WHEN log files grow large, THE Lead Generation Bot SHALL continue appending without automatic rotation or deletion
