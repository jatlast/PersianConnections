ALTER TABLE login_info
ADD email_verification_code		VARCHAR(17)	NULL	DEFAULT CONVERT( VARCHAR(10), CONVERT( INT, RAND() * 100000000 ) )
	, is_email_verified		CHAR(1)		NULL	DEFAULT '0'
	, where_did_you_hear_about_us	VARCHAR(128)	NULL	DEFAULT ''
	, advertising_campaign_code	VARCHAR(32)	NULL	DEFAULT ''
GO

update login_info 
set email_verification_code = CONVERT( VARCHAR(10), CONVERT( INT, RAND(user_id) * 100000000 ) )
	, is_email_verified = '0'
	, where_did_you_hear_about_us = ''
	, advertising_campaign_code = ''

select * from login_info
