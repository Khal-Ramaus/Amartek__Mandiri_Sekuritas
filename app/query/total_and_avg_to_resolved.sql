select 'Closed' as response, sum(total_minutes) as total_minutes, sum(average_duration_minutes) as average_duration_minutes
from
(SELECT
    events.company_response_to_consumer,
    ROUND(EXTRACT(EPOCH FROM SUM(ser_time::interval)) / 60, 2) AS total_minutes,
    ROUND(AVG(EXTRACT(EPOCH FROM logs.ser_time::interval) / 60), 2) AS average_duration_minutes
FROM
    crm_call_center_logs AS logs
JOIN
    crm_events AS events 
    ON logs.complaint_id = events.complaint_id
WHERE
    logs.complaint_id IS NOT NULL
	AND company_response_to_consumer not in ('In progress', 'Untimely response')
GROUP BY
	events.company_response_to_consumer) as table1