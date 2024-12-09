SELECT signup_date, COUNT(*) AS user_count
FROM user_data
GROUP BY signup_date
ORDER BY signup_date;
