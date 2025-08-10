SELECT 
    date_received as "Date Received",ROUND(EXTRACT(EPOCH FROM SUM(ser_time::interval)) / 60, 2) AS "Total Minutes"
FROM crm_call_center_logs
GROUP BY date_received
order by date_received