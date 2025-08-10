SELECT
    events.company_response_to_consumer,
    COUNT(*) AS total_number_of_data,
    ROUND(AVG(EXTRACT(EPOCH FROM logs.ser_time::interval) / 60), 2) AS average_duration_minutes
FROM
    crm_call_center_logs AS logs
JOIN
    crm_events AS events 
    ON logs.complaint_id = events.complaint_id
WHERE
    logs.complaint_id IS NOT NULL
GROUP BY
    events.company_response_to_consumer
ORDER BY
	events.company_response_to_consumer;