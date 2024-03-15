-- SET GLOBAL log_bin_trust_function_creators = 1;

-- CS 121 24wi: Password Management (A6 and Final Project)

-- (Provided) This function generates a specified number of characters for using as a
-- salt in passwords.
DELIMITER !
CREATE FUNCTION make_salt(num_chars INT)
RETURNS VARCHAR(20) NOT DETERMINISTIC
BEGIN
    DECLARE salt VARCHAR(20) DEFAULT '';

    -- Don't want to generate more than 20 characters of salt.
    SET num_chars = LEAST(20, num_chars);

    -- Generate the salt!  Characters used are ASCII code 32 (space)
    -- through 126 ('z').
    WHILE num_chars > 0 DO
        SET salt = CONCAT(salt, CHAR(32 + FLOOR(RAND() * 95)));
        SET num_chars = num_chars - 1;
    END WHILE;

    RETURN salt;
END !
DELIMITER ;

-- Provided (you may modify in your FP if you choose)
-- This table holds information for authenticating users based on
-- a password.  Passwords are not stored plaintext so that they
-- cannot be used by people that shouldn't have them.
-- You may extend that table to include an is_admin or role attribute if you
-- have admin or other roles for users in your application
-- (e.g. store managers, data managers, etc.)
CREATE TABLE user_info (
    -- Usernames are up to 20 characters.
    username VARCHAR(20) PRIMARY KEY,

    -- Salt will be 8 characters all the time, so we can make this 8.
    salt CHAR(8) NOT NULL,

    -- We use SHA-2 with 256-bit hashes.  MySQL returns the hash
    -- value as a hexadecimal string, which means that each byte is
    -- represented as 2 characters.  Thus, 256 / 8 * 2 = 64.
    -- We can use BINARY or CHAR here; BINARY simply has a different
    -- definition for comparison/sorting than CHAR.
    password_hash BINARY(64) NOT NULL
);

-- [Problem 1a]
-- Adds a new user to the user_info table, using the specified password (max
-- of 20 characters). Salts the password with a newly-generated salt value,
-- and then the salt and hash values are both stored in the table.
DELIMITER !
CREATE PROCEDURE sp_add_user(new_username VARCHAR(20), password VARCHAR(20))
BEGIN
    DECLARE salt_new_one VARCHAR(8);
    DECLARE password_hash_with_salted BINARY(64);

    -- Generate a new 8-character salt.
    SET salt_new_one = make_salt(8);

    -- Hash the concatenated salt and password.
    SET password_hash_with_salted = SHA2(CONCAT(salt_new_one, password), 256);

    -- Insert the new user record into the user_info table.
    INSERT INTO user_info (username, salt, password_hash)
    VALUES (new_username, salt_new_one, password_hash_with_salted);
END !
DELIMITER ;

-- [Problem 1b]
-- Authenticates the specified username and password against the data
-- in the user_info table.  Returns 1 if the user appears in the table, and the
-- specified password hashes to the value for the user. Otherwise returns 0.
DELIMITER !
CREATE FUNCTION authenticate(username VARCHAR(20), password VARCHAR(20))
RETURNS TINYINT DETERMINISTIC
BEGIN
    DECLARE salt_new_one CHAR(8);
    DECLARE hash_password BINARY(64);
    DECLARE user_count INT;

    -- Check whether the username exists in the database
    SELECT COUNT(*) INTO user_count FROM user_info WHERE user_info.username = username;
    
    -- If the username does not exist, return 0
    IF user_count = 0 THEN RETURN 0;
    END IF;

    -- Retrieve the salt and hashed password for the username
    SELECT user_info.salt, user_info.password_hash INTO salt_new_one, hash_password 
    FROM user_info 
    WHERE user_info.username = username;

    -- Compare the provided password's hash (with the user's salt) against the stored hash
    IF SHA2(CONCAT(salt_new_one, password), 256) = hash_password THEN
        RETURN 1;
    ELSE
        RETURN 0; 
    END IF;
END !
DELIMITER ;

-- [Problem 1c]
-- Add at least two users into your user_info table so that when we run this file,
-- we will have examples users in the database.
CALL sp_add_user('user1', 'password123');
CALL sp_add_user('user2', 'password456');

-- [Problem 1d]
-- Create a procedure sp_change_password to generate a new salt and change the given
-- user's password to the given password (after salting and hashing)

DELIMITER !
CREATE PROCEDURE sp_change_password(
  username VARCHAR(20), new_password VARCHAR(20)
)
BEGIN
    DECLARE salt_new_one CHAR(8);
    DECLARE password_hash_new_one BINARY(64);

    SELECT make_salt(8) INTO salt_new_one;

    -- Hash the concatenated new salt and new password, and directly assign it to new_password_hash variable.
    SELECT SHA2(CONCAT(salt_new_one, new_password), 256) INTO password_hash_new_one;

    -- Update the existing user record in the user_info table with the new salt and new hashed password.
    UPDATE user_info
    SET salt = salt_new_one, password_hash = password_hash_new_one
    WHERE user_info.username = username;

END !

DELIMITER ; 
