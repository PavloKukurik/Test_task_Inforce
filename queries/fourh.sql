SELECT user_id, name, email, domain
FROM user_data
WHERE domain = (
    SELECT domain
    FROM user_data
    GROUP BY domain
    ORDER BY COUNT(*) DESC
    LIMIT 1
);
