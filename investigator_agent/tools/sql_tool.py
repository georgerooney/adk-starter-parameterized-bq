from google.cloud import bigquery


def check_weather_event(
    state: str, year: str, month: str, day: str, event_type: str
) -> dict:
    """
    Checks if a specific weather event occurred in a given state on a specific date.

    Args:
        state: 2-letter state code (e.g., 'TN').
        year: 4-digit year (e.g., '1991').
        month: Month (e.g., '07').
        day: Day (e.g., '04').
        event_type: One of: fog, rain, snow, hail, thunder, tornado.
    """
    client = bigquery.Client()

    # Map user-friendly event names to actual BQ column names
    schema_map = {
        "fog": "fog",
        "rain": "rain_drizzle",
        "snow": "snow_ice_pellets",
        "hail": "hail",
        "thunder": "thunder",
        "tornado": "tornado_funnel_cloud",
    }

    # Validate the event_type to prevent SQL injection since we inject the column name
    if event_type not in schema_map:
        return {
            "error": f"Invalid event_type. Must be one of {list(schema_map.keys())}"
        }

    target_column = schema_map[event_type]
    table_id = f"bigquery-public-data.noaa_gsod.gsod{year}"

    query = f"""
        SELECT COUNT(*) as event_count
        FROM `{table_id}` y
        WHERE y.stn IN (
            SELECT s.usaf 
            FROM `bigquery-public-data.noaa_gsod.stations` s 
            WHERE state = @state
        )
        AND y.da = @day
        AND y.mo = @month
        AND y.{target_column} = "1"
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("state", "STRING", state),
            bigquery.ScalarQueryParameter("day", "STRING", day),
            bigquery.ScalarQueryParameter("month", "STRING", month),
        ]
    )

    print(f"DEBUG: Executing SQL Query:\n{query}")
    print(
        f"DEBUG: Parameters: state={state}, day={day}, month={month}, event_type={event_type}"
    )

    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()

        # Get the first row
        row = next(iter(results))
        found = row.event_count > 0

        print(f"DEBUG: SQL Result: event_count={row.event_count}, found={found}")

        return {
            "event_occurred": found,
            "station_count": row.event_count,
            "details": f"Found {row.event_count} stations in {state} reporting {event_type} on {month}/{day}/{year}.",
        }
    except Exception as e:
        print(f"DEBUG: SQL Error: {e}")
        return {"error": str(e)}
