SELECT *
FROM user_data
WHERE signup_date >= CURRENT_DATE - INTERVAL '7 days';
