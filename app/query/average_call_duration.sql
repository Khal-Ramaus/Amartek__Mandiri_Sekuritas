SELECT
    AVG(ser_time::interval) AS rata_rata_durasi_panggilan
FROM
    crm_call_center_logs
	where complaint_id is not null