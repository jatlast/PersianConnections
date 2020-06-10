if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[changeEmailAddress]') and OBJECTPROPERTY(id, N'IsProcedure') = 1)
drop procedure [dbo].[changeEmailAddress]
GO

if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[createLoginInfo]') and OBJECTPROPERTY(id, N'IsProcedure') = 1)
drop procedure [dbo].[createLoginInfo]
GO

if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[genMemberHome]') and OBJECTPROPERTY(id, N'IsProcedure') = 1)
drop procedure [dbo].[genMemberHome]
GO

if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[getLoginInfoByEmailMaidenName]') and OBJECTPROPERTY(id, N'IsProcedure') = 1)
drop procedure [dbo].[getLoginInfoByEmailMaidenName]
GO

if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[getLoginInfoByNamePassword]') and OBJECTPROPERTY(id, N'IsProcedure') = 1)
drop procedure [dbo].[getLoginInfoByNamePassword]
GO

if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[getLoginInfoByUserNameMaidenName]') and OBJECTPROPERTY(id, N'IsProcedure') = 1)
drop procedure [dbo].[getLoginInfoByUserNameMaidenName]
GO

if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[simpleSearch]') and OBJECTPROPERTY(id, N'IsProcedure') = 1)
drop procedure [dbo].[simpleSearch]
GO

if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[singleProfile]') and OBJECTPROPERTY(id, N'IsProcedure') = 1)
drop procedure [dbo].[singleProfile]
GO

if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[transaction_credit_card_send]') and OBJECTPROPERTY(id, N'IsProcedure') = 1)
drop procedure [dbo].[transaction_credit_card_send]
GO

if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[transaction_manual_check_post]') and OBJECTPROPERTY(id, N'IsProcedure') = 1)
drop procedure [dbo].[transaction_manual_check_post]
GO

if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[updateLoginInfo]') and OBJECTPROPERTY(id, N'IsProcedure') = 1)
drop procedure [dbo].[updateLoginInfo]
GO

if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[verifyEmailAddress]') and OBJECTPROPERTY(id, N'IsProcedure') = 1)
drop procedure [dbo].[verifyEmailAddress]
GO

if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[verifyMembershipTypePermissions]') and OBJECTPROPERTY(id, N'IsProcedure') = 1)
drop procedure [dbo].[verifyMembershipTypePermissions]
GO

SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS OFF 
GO

CREATE PROCEDURE [changeEmailAddress]
@UserName varchar(32)
, @Password varchar(16)
, @Email varchar(64)
, @NewEmail varchar(64)
, @EmailVerificationCode varchar(20)

 AS

-- Determine if the user_name, email, and password match before updating email in login_info table...
IF ( (SELECT password FROM login_info WHERE user_name = @UserName AND email = @Email) = @Password)
	BEGIN
		-- Update email in login_info table
		print 'changing email for user (' + @UserName + ') from (' + @Email + ') to (' + @NewEmail + ')'
		update login_info 
			set email = @NewEmail
				, email_verification_code = @EmailVerificationCode
				, is_email_verified = '0'
			where user_name = @UserName
				AND password = @Password
				AND email = @Email
		return 1
	END
ELSE
	BEGIN
		-- If the user_name, email and password do not match exit with a return value of 666 
		PRINT 'user_name and password did not match so we are unable to update email address for user (' + @UserName + ') from (' + @Email + ') to (' + @NewEmail + ')' -- the first part of this string must remain as "user_name and password did not match" because it is being checked for in "msg_handler" 
		RETURN 666
	END
GO
SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS ON 
GO

SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS ON 
GO

CREATE PROCEDURE [createLoginInfo]
@UserId int-- not used 
, @UserName varchar(32)
, @MembershipType char -- not used 
, @Password varchar(16)
, @PasswordHint varchar(64)
, @Email varchar(64)
, @Sex char
, @CreationDate varchar(32)-- not used 
, @LastLogin varchar(32) -- not used 
, @PhotoSubmitted int -- not used 
, @DateStartedPaying VARCHAR(32) = ''
, @EmailVerificationCode VARCHAR(17) = ''
, @IsEmilVerified VARCHAR(2) = ''
, @WhereDidYouHearAboutUs VARCHAR(128) = ''
, @AdvertisingCampaignCode VARCHAR(32) = ''
, @CustomerIP CHAR(15) = ''

 AS
-- clean up database by removing all bad profiles
print 'Cleaning up Database'
EXEC admin_DeleteBadProfiles

-- UserId must be declared 
DECLARE @@UserId int
DECLARE @@return_status int
-- membership_type, creation_date, and last_login must be declared 
DECLARE @@membership_type char
DECLARE @@creation_date datetime
DECLARE @@last_login datetime

DECLARE @@WhichConnections varchar(32)
select @@WhichConnections = 'Administrator'

-- Get the maximum +1 user_id number fron the login_info table 
select @@UserId = max(user_id + 1) from login_info

--  If there are no user ids in the database this is the first and therefore #1 
if @@UserId is NULL
select @@UserId = 1

print 'Add a new IP address to the customer_IP table'
INSERT INTO customer_IP (user_name
				, user_id
				, IP_address
				) 
		VALUES (@UserName
			, @@UserID
			, @CustomerIP
			)

-- Set the default values 
select @@creation_date = getdate()
select @@last_login = getdate()

select @@membership_type = '0' -- 0 = basic
--select @@membership_type = '1' -- 0 = premium

-- Determine if the user_name is unique in the login_info table
if exists (select user_name from login_info where user_name = @UserName)
BEGIN
	-- If the user_name is not unique exit with a return value of 666 
	print 'user_name is not unique in login_info' -- the first part of this string must remain as "user_name is not unique" because it is being checked for in "msg_handler" 
	return 666
END
else
BEGIN
	-- If the user_name is unique add the user to the login_info table and exit with a return value of 1 
	print 'user_name IS unique in login_info'
	insert into login_info (user_id
			, user_name
			, password
			, password_hint
			, email
			, sex
			, membership_type
			, creation_date
			, last_login
			, photo_submitted
			, date_started_paying
			, email_verification_code
			, is_email_verified
			, where_did_you_hear_about_us
			, advertising_campaign_code
			) 
	values (@@UserId
		, @UserName
		, @Password
		, @PasswordHint
		, @Email
		, @Sex
		, @@membership_type
		, @@creation_date
		, @@last_login
		, 0
		, NULL
		, CONVERT( VARCHAR(10), CONVERT( INT, RAND() * 100000000 ) ) -- Create a random numerical character sequence no larger than 10 chars long
		, '0'
		, @WhereDidYouHearAboutUs
		, @AdvertisingCampaignCode
		)
END
-- Determine if the user_name is unique in the contact_info table
if exists (select user_name from contact_info where user_name = @UserName)
BEGIN
	-- If the user_name is not unique exit with a return value of 665
	print 'user_name is not unique in contact_info' -- the first part of this string must remain as "user_name is not unique" because it is being checked for in "msg_handler" 
	return 665
END
else
BEGIN
	-- If the user_name is unique add the user to the contact_info table and exit with a return value of 1 
	print 'user_name IS unique in contact_info'
	insert into contact_info (user_name
			, first_name
			, last_name
			, street_address
			, city
			, state
			, country
			, zip
			, telephone
			) 
	values (@UserName
		, ''
		, ''
		, ''
		, ''
		, '0'
		, '0'
		, ''
		, ''
		)
END

-- Determine if the user_name is unique in the relationship table
if exists (select user_name from relationship where user_name = @UserName)
BEGIN
	-- If the user_name is not unique exit with a return value of 664
	print 'user_name is not unique in relationship' -- the first part of this string must remain as "user_name is not unique" because it is being checked for in "msg_handler" 
	return 664
END
else
BEGIN
	-- If the user_name is unique add the user to the relationship table and exit with a return value of 1 
	print 'user_name IS unique in relationship'
		insert into relationship (user_name
				, prefer_not_to_say
				, any_relationship
				, hang_out
				, short_term
				, long_term
				, talk_email
				, photo_exchange
				, marriage
				, other
				) 
		values (@UserName
			, '1'
			, '0'
			, '0'
			, '0'
			, '0'
			, '0'
			, '0'
			, '0'
			, '0'
			)
END

-- Determine if the user_name is unique in the personal_info table
if exists (select user_name from personal_info where user_name = @UserName)
BEGIN
	-- If the user_name is not unique exit with a return value of 663
	print 'user_name is not unique in personal_info' -- the first part of this string must remain as "user_name is not unique" because it is being checked for in "msg_handler" 
	return 663
END
else
BEGIN
	-- If the user_name is unique add the user to the personal_info table and exit with a return value of 1 
	print 'user_name IS unique in personal_info'
		insert into personal_info(user_name
				, sex_preference
				, age
				, marital_status
				, profession
				, income
				, education
				, religion
				, height
				, weight
				, eyes
				, hair
				, min_age_desired
				, max_age_desired
				, cook
				, smoke
				, drink
				, party
				, political
				, housing_status
				) 
		values (@UserName
			, '1'
			, '18'
			, '0'
			, '0'
			, '0'
			, '0'
			, '0'
			, '0'
			, '0'
			, '0'
			, '0'
			, '18'
			, '99'
			, '0'
			, '0'
			, '0'
			, '0'
			, '0'
			, '0'
			)
END
-- Determine if the user_name is unique in the about_info table
if exists (select user_name from about_info where user_name = @UserName)
BEGIN
	-- If the user_name is not unique exit with a return value of 662 
	print 'user_name is not unique in about_info' -- the first part of this string must remain as "user_name is not unique" because it is being checked for in "msg_handler" 
	return 662
END
else
BEGIN
	-- If the user_name is unique add the user to the about_info table and exit with a return value of 1 
	print 'user_name IS unique in about_info'
	insert into about_info (user_name
			, screen_quote
			, about_yourself
			, questionable
			) 
	values (@UserName
		, ''
		, ''
		, '0'
		)
END

-- Determine if the user_name is unique in the about_info table
if exists (select user_name from pictures where user_name = @UserName)
BEGIN
	-- If the user_name is not unique exit with a return value of 662 
	print 'user_name is not unique in pictures' -- the first part of this string must remain as "user_name is not unique" because it is being checked for in "msg_handler" 
	return 661
END
else
BEGIN
	-- If the user_name is unique add the user to the pictures table and exit with a return value of 1 
print 'user_name IS unique in pictures'
insert into pictures (user_name
		, photo_1
		, photo_2
		, photo_3
		, photo_4
		, photo_5
		) 
values (@UserName
	, 'Nothing'
	, 'Nothing'
	, 'Nothing'
	, 'Nothing'
	, 'Nothing'
	)
END

exec @@return_status = mailSendNewUserWelcome @@WhichConnections, @UserName

if(@@return_status = 666)
	BEGIN
		print 'Mail could not be sent'
		return 666
	END
else
	BEGIN
		print 'Mail has been sent'
	END
GO
SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS ON 
GO

SET QUOTED_IDENTIFIER ON 
GO
SET ANSI_NULLS OFF 
GO

CREATE PROCEDURE [genMemberHome]
	@UserName			 varchar(32)
	, @Password 			varchar (16)
	, @CustomerIP 			varchar(15)	 = ' '
	, @WhereDidYouHearAboutUs	varchar(128)	 = ' '
	, @AdvertisingCampaignCode	varchar(32)	 = ' '
 AS

DECLARE @@PromoDaysRemaining		CHAR(8)
DECLARE @@PremiumDaysRemaining	CHAR(8)
DECLARE @@MembershipType 		CHAR(4)
DECLARE @@IsMembershipActive		CHAR(1)
DECLARE @@DateMembershipExpires	DATETIME
DECLARE @@UserID				CHAR(10)

-- Get membership_type from login_info table...
SELECT @@MembershipType = (SELECT membership_type FROM login_info WHERE user_name = @UserName)
-- Get is_membership_active from billing_info table...
SELECT @@IsMembershipActive = (SELECT is_membership_active from billing_info where user_name = @UserName)
-- Get date_membership_expires from billing_info table...
SELECT @@DateMembershipExpires = (SELECT date_membership_expires from billing_info where user_name = @UserName)
-- Get user_id from login_info table...
SELECT @@UserID = (SELECT user_id FROM login_info WHERE user_name = @UserName)

-- Only change the default value of @PromoDaysRemaining if the membership_type_id is promotional...
if (
	select datediff(day, getdate(), membership_type.date_promotion_ended) 
	from membership_type
		, login_info
	where login_info.user_name = @UserName
	and login_info.membership_type = membership_type.membership_type_id
  ) != NULL
	BEGIN
		print 'Get PromoDaysRemaining'
		select @@PromoDaysRemaining = (
							select datediff(day, getdate(), membership_type.date_promotion_ended) 
							from membership_type
								, login_info
							where login_info.user_name = @UserName
							and login_info.membership_type = membership_type.membership_type_id
						    )
	END
ELSE
	BEGIN
		print 'Dont get PromoDaysRemaining'
	END

select @@PremiumDaysRemaining = ''
IF(@@IsMembershipActive = '0' AND( @@MembershipType = '1' OR  @@MembershipType = '2') )
	BEGIN
		print 'Get PremiumDaysRemaining'
		select @@PremiumDaysRemaining = (
							select datediff(day, getdate(), @@DateMembershipExpires) 
							from billing_info
							where billing_info.user_name = @UserName
						    )
	END
ELSE
	BEGIN
		print 'Dont get PremiumDaysRemaining'
	END


if ( (select password from login_info where user_name = @UserName) = @Password)
	BEGIN
		-- Determine if the x_customer_IP is present in the restricted_IP table
		IF EXISTS (select IP_address from customer_IP where  IP_address = @CustomerIP AND  user_name = @UserName AND  user_id = @@UserID)
			BEGIN
				PRINT 'IP address already exists(' + @UserName + '):(' + @CustomerIP + ')'
			END
		ELSE
			BEGIN
				-- If the IP_address does not already exist for this user add it to the customer_IP table
				print 'Add a new IP address to the customer_IP table'
				insert into customer_IP (user_name
						, user_id
						, IP_address
						) 
				values (@UserName
					, @@UserID
					, @CustomerIP
					)
			END
			
		-- If the user_name is unique add the user to the login_info table and exit with a return value of 1 
		print 'Get login_info table information'
		select login_info.user_name
			, login_info.membership_type
			, membership_type.membership_type_name
			, login_info.photo_submitted
			, login_info.email_verification_code
			, login_info.is_email_verified
			, login_info.where_did_you_hear_about_us
			, login_info.advertising_campaign_code
			, about_info.questionable
			, @@PromoDaysRemaining AS 'PromoDaysRemaining'
			, @@IsMembershipActive AS 'IsMembershipActive'
			, @@PremiumDaysRemaining AS 'PremiumDaysRemaining'
		from login_info
			, about_info
			, membership_type
		where login_info.user_name = @UserName
			and login_info.password = @Password
			and login_info.user_name = about_info.user_name
			and login_info.membership_type = membership_type.membership_type_id
	
		print 'Get messages sent to the user'
		select mail.mail_id
			, mail.sent_to
			, mail.sent_from
			, mail.subject
			, mail.message_text
			, mail.when_sent
			, mail.when_read
			, mail.sender_deleted
			, mail.receiver_deleted
		from mail
		where mail.sent_to = @UserName
	
		PRINT 'Update last_login'
		UPDATE login_info
		SET last_login =  GETDATE()
		WHERE user_name = @UserName
	return 0
	END
ELSE
	BEGIN
		print 'ERROR: User Name and Password did not match.'
		return 666
	END
GO
SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS ON 
GO

SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS OFF 
GO




CREATE PROCEDURE [getLoginInfoByEmailMaidenName]
	@Email varchar(32)
	, @MaidenName varchar (32)

 AS

if ( (select password_hint from login_info where email = @Email) = @MaidenName)
BEGIN
/* Get raw login_info data */
	select	user_id
		, user_name
		, membership_type
		, password
		, password_hint
		, email
		, sex
		, creation_date
		, last_login
		, photo_submitted
		, date_started_paying
		, email_verification_code
		, is_email_verified
		, where_did_you_hear_about_us
		, advertising_campaign_code
	from login_info
	where email = @Email
		and password_hint = @MaidenName

/* Get textual login_info data using a join */
	select	user_id
		, user_name
		, membership_type
		, password
		, password_hint
		, email
		, sex.choice as "sex"
		, creation_date
		, last_login
		, photo_submitted
		, date_started_paying
		, email_verification_code
		, is_email_verified
		, where_did_you_hear_about_us
		, advertising_campaign_code
	from login_info
		, sex
	where login_info.email = @Email
		and login_info.password_hint = @MaidenName
			and login_info.sex = sex.value
	return 1
END

else
BEGIN
	print 'ERROR: User Name and Password did not match.'
	return 666
END
GO
SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS ON 
GO

SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS ON 
GO




CREATE PROCEDURE [getLoginInfoByNamePassword]
	@UserName varchar(32)
	, @Password varchar (16)
 AS

if ( (select password from login_info where user_name = @UserName) = @Password)

BEGIN
/* Get raw login_info data */
	select	user_id
		, user_name
		, membership_type
		, password
		, password_hint
		, email
		, sex
		, creation_date
		, last_login
		, photo_submitted
		, date_started_paying
		, email_verification_code
		, is_email_verified
		, where_did_you_hear_about_us
		, advertising_campaign_code
	from login_info
	where user_name = @UserName
			and password = @Password

/* Get textual login_info data using a join */
	select	user_id
		, user_name
		, membership_type
		, password
		, password_hint
		, email
		, sex.choice as "sex"
		, creation_date
		, last_login
		, photo_submitted
		, date_started_paying
		, email_verification_code
		, is_email_verified
		, where_did_you_hear_about_us
		, advertising_campaign_code
	from login_info, sex
	where user_name = @UserName
			and password = @Password
			and login_info.sex = sex.value
	return 1
END

else
BEGIN
	print 'ERROR: User Name and Password did not match.'
	return 666
END
GO
SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS ON 
GO

SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS OFF 
GO




CREATE PROCEDURE [getLoginInfoByUserNameMaidenName]
	@UserName varchar(32)
	, @MaidenName varchar (16)

 AS

if ( (select password_hint from login_info where user_name = @UserName) = @MaidenName)
BEGIN
/* Get raw login_info data */
	select	user_id
		, user_name
		, membership_type
		, password
		, password_hint
		, email
		, sex
		, creation_date
		, last_login
		, photo_submitted
		, date_started_paying
		, email_verification_code
		, is_email_verified
		, where_did_you_hear_about_us
		, advertising_campaign_code
	from login_info
	where user_name = @UserName
		and password_hint = @MaidenName

/* Get textual login_info data using a join */
	select	user_id
		, user_name
		, membership_type
		, password
		, password_hint
		, email
		, sex.choice as "sex"
		, creation_date
		, last_login
		, photo_submitted
		, date_started_paying
		, email_verification_code
		, is_email_verified
		, where_did_you_hear_about_us
		, advertising_campaign_code
	from login_info
		, sex
	where login_info.user_name = @UserName
		and login_info.password_hint = @MaidenName
			and login_info.sex = sex.value
	return 1
END

else
BEGIN
	print 'ERROR: User Name and Password did not match.'
	return 666
END
GO
SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS ON 
GO

SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS ON 
GO


CREATE PROCEDURE [simpleSearch]
 @Search int
, @IAm char(1)
, @Seeking char(1)
, @City varchar(32)
, @State varchar(2)
, @Country varchar(3)
, @MinAgeDesired varchar(2)
, @MaxAgeDesired varchar(2)
, @Limit int
, @Sort varchar(16)
, @Index varchar(6)
, @UserName VARCHAR(32)

 AS

-- START Verify Permissions
DECLARE @@ReturnValue char(4)

EXEC @@ReturnValue = verifyMembershipTypePermissions  @UserName, 'allow_search_simple'
-- Check membership_type for permission
if ( @@ReturnValue != 1	)
	BEGIN--  DENIED
		print 'You must upgrade your membership to use this feature'
		return @@ReturnValue
	END
-- END Verify Permissions


-- the SET string provides a slight performance gain for stored procedures
SET NOCOUNT ON

declare @GlobalRowCount INT
SELECT @GlobalRowCount = 500;

DECLARE @AlternativeMin	INT		-- Used as lower bound for sex_preference searches
DECLARE @AlternativeMax 	INT		-- Used as upper bound for sex_preference searches

-- Determine what sexual preference search needs to be performed...
IF (@IAm = @Seeking AND @IAm > "0")
BEGIN
	-- Same sex search...
	PRINT 'same sex search'
	SELECT @AlternativeMin = 2
	SELECT @AlternativeMax = 4
END
ELSE
	BEGIN
		-- Opposite sex search...
		PRINT 'opposite sex search'
		SELECT @AlternativeMin = 0
		SELECT @AlternativeMax = 1
	END
-- Check for city variable...
IF (@City = "")
BEGIN
	-- If no city has been entered then default to the match any string wildcard...
	SELECT @City = '%'
	PRINT 'City = ' + @City
END

-- Check for city variable...
IF (@State = "0")
BEGIN
	-- If no state has been entered then default to the match any string wildcard...
	SELECT @State = '%'
	PRINT 'State = ' + @State
END

-- Check for country variable...
IF (@Country = "0")
BEGIN
	-- If no country has been entered then default to the match any string wildcard...
	SELECT @Country = '%'
	PRINT 'Country = ' + @Country
END

-- Determin how the user whats the results ordered...
DECLARE @OrderBy CHAR(32) 	-- Holds the order by clause condition
IF( @Sort = 'user_name' )
	BEGIN
		SELECT @OrderBy = 'contact_info.user_name'
	END
ELSE
	IF( @Sort = 'state' )
		BEGIN
			SELECT @OrderBy = 'contact_info.state'
		END
	ELSE
		IF( @Sort = 'age' )
		BEGIN
			SELECT @OrderBy = 'personal_info.age'
		END
		ELSE
			IF( @Sort = 'creation_date' )
			BEGIN
				SELECT @OrderBy = 'login_info.creation_date DESC'
			END

PRINT 'Order by ' + @OrderBy

-- the SET ROWCOUNT limits the number of rows affected
SET ROWCOUNT @GlobalRowCount

/* Select the raw information by joining just the personal_info and relationship tables... */
SELECT CASE 
		WHEN COUNT(*) >= @GlobalRowCount THEN @GlobalRowCount
		ELSE COUNT(*)
	END 'Number of Rows'
	FROM login_info
		, contact_info
		, personal_info
		, about_info
	WHERE login_info.sex like @Seeking
	AND login_info.photo_submitted >= @Search
	AND personal_info.sex_preference >= @AlternativeMin
	AND personal_info.sex_preference <= @AlternativeMax
	AND contact_info.city like @City
	AND contact_info.state like @State
	AND contact_info.country like @Country
	AND personal_info.age >= @MinAgeDesired
	AND personal_info.age <= @MaxAgeDesired
	AND about_info.questionable = 0
	AND login_info.user_name = contact_info.user_name
	AND login_info.user_name = personal_info.user_name
	AND login_info.user_name = about_info.user_name

DECLARE @RowCount	INT -- Used to set the rowcount based on index and limit
SELECT @RowCount = ( @Index + @Limit + 2 )

SET ROWCOUNT @RowCount

-- Select the all the information by joining the tables... 
EXEC ('SELECT login_info.user_name as "user_name"
	, contact_info.city as "city"
	, state.choice as "state"
	, country.choice as "country"
	, personal_info.age as "age"
	, about_info.screen_quote as "screen_quote"
	, about_info.about_yourself as "about_yourself"
	, pictures.photo_1 as "pic 1"

FROM login_info
	, contact_info
	, personal_info
	, about_info
	, state
	, country
	, pictures
WHERE login_info.user_name = contact_info.user_name
	AND login_info.user_name = personal_info.user_name
	AND login_info.user_name = about_info.user_name
	AND login_info.user_name = pictures.user_name
	AND contact_info.state = state.value
	AND contact_info.country = country.value
	AND login_info.user_name in 
	(
	SELECT login_info.user_name

		FROM login_info
			, contact_info
			, personal_info
			, about_info
		WHERE login_info.sex LIKE ''' + @Seeking +'''
		AND login_info.photo_submitted >= '''+ @Search + '''
		AND personal_info.sex_preference >= ''' + @AlternativeMin + '''
		AND personal_info.sex_preference <= ''' + @AlternativeMax + '''
		AND contact_info.city LIKE ''' + @City + '''
		AND contact_info.state LIKE ''' + @State + '''
		AND contact_info.country LIKE ''' + @Country + '''
		AND personal_info.age >= ''' + @MinAgeDesired + '''
		AND personal_info.age <= ''' + @MaxAgeDesired + '''
		AND about_info.questionable = 0
		AND login_info.user_name = contact_info.user_name
		AND login_info.user_name = personal_info.user_name
		AND login_info.user_name = about_info.user_name
	)

ORDER BY ' + @OrderBy
)

SET ROWCOUNT 0
GO
SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS ON 
GO

SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS ON 
GO

CREATE PROCEDURE [singleProfile]
@UserNameBeingSearched varchar(32)
, @UserNameSearching varchar(32)

 AS

-- START Verify Permissions
DECLARE @@ReturnValue char(4)
DECLARE @@ViewMyOwnProfile char(2)

IF(@UserNameBeingSearched = @UserNameSearching )
	BEGIN
		SELECT @@ViewMyOwnProfile = '1'
	END
ELSE
	BEGIN
		SELECT @@ViewMyOwnProfile = '0'
	END

IF(@UserNameBeingSearched = 'administrator' OR @@ViewMyOwnProfile = '1')
	BEGIN
		/* Select the raw information by joining just the personal_info and relationship tables... */
		print 'select all the info to generate the single profile information'
		select login_info.user_id as "user_id"
			, login_info.user_name as "user_name"
			, login_info.membership_type as "membership_type"
			, sex.choice as "sex"
			, login_info.creation_date as "creation_date"
			, login_info.last_login as "last_login"
			, contact_info.city as "city"
			, state.choice as "state"
			, country.choice as "country"
			, sex_preference.choice as "sex_preference"
			, personal_info.age as "age"
			, marital_status.choice as "marital_status"
			, profession.choice as "profession"
			, income.choice as "income"
			, education.choice as "education"
			, religion.choice as "religion"
			, height.choice as "height"
			, weight.choice  as "weight"
			, eyes.choice as "eyes"
			, hair.choice as "hair"
			, personal_info.min_age_desired
			, personal_info.max_age_desired
			, cook.choice as "cook"
			, smoke.choice as "smoke"
			, drink.choice as "drink"
			, party.choice as "party"
			, political.choice as "political"
			, housing_status.choice as "housing_status"
			, relationship.prefer_not_to_say as "prefer_not_to_say"
			, relationship.any_relationship as "any_relationship"
			, relationship.hang_out as "hang_out"
			, relationship.short_term as "short_term"
			, relationship.long_term as "long_term"
			, relationship.talk_email as "talk_email"
			, relationship.photo_exchange as "photo_exchange"
			, relationship.marriage as "marriage"
			, relationship.other as "other"
			, about_info.screen_quote as "screen_quote"
			, about_info.about_yourself as "about_yourself"
			, pictures.photo_1 as "pic 1"
			, pictures.photo_2 as "pic 2"
			, pictures.photo_3 as "pic 3"
			, pictures.photo_4 as "pic 4"
			, pictures.photo_5 as "pic 5"
		from login_info
			, contact_info
			, personal_info
			, relationship
			, about_info
			, sex_preference
			, marital_status
			, profession
			, income
			, education
			, religion
			, height
			, weight
			, eyes
			, hair
			, cook
			, smoke
			, drink
			, party
			, political
			, housing_status
			, sex
			, state
			, country
			, pictures
		where login_info.user_name = contact_info.user_name
			and login_info.user_name = personal_info.user_name
			and login_info.user_name = relationship.user_name
			and login_info.user_name = about_info.user_name
			and login_info.user_name = pictures.user_name
			and login_info.sex = sex.value
			and ( 
				about_info.questionable = 0 
				OR 
				@@ViewMyOwnProfile = '1' 
			         )
			and contact_info.state = state.value
			and contact_info.country = country.value
			and personal_info.sex_preference = sex_preference.value
			and personal_info.marital_status = marital_status.value
			and personal_info.profession = profession.value
			and personal_info.income = income.value
			and personal_info.education = education.value
			and personal_info.religion = religion.value
			and personal_info.height = height.value
			and personal_info.weight = weight.value
			and personal_info.eyes = eyes.value
			and personal_info.hair = hair.value
			and personal_info.cook = cook.value
			and personal_info.smoke = smoke.value
			and personal_info.drink = drink.value
			and personal_info.party = party.value
			and personal_info.political = political.value
			and personal_info.housing_status = housing_status.value
			and personal_info.user_name = @UserNameBeingSearched
		return 1
	END
ELSE
	BEGIN
		EXEC @@ReturnValue = verifyMembershipTypePermissions @UserNameSearching, 'allow_view_profiles'
		-- Check membership_type for permission
		IF ( @@ReturnValue != 1 AND  @@ViewMyOwnProfile = '0' )
			BEGIN--  DENIED
				print 'You must upgrade your membership to use this feature'
				return @@ReturnValue
			END
		-- END Verify Permissions
		
		-- Check if the UserNameBeingSearched is hidden...
		SELECT @@ReturnValue = (select questionable from about_info where user_name = @UserNameBeingSearched)
		if ( @@ReturnValue = 1 AND @@ViewMyOwnProfile = '0' )
			BEGIN--  DENIED
				print 'The user you are trying to view currently has a hidden profile'
				return 205
			END
		
		/* Select the raw information by joining just the personal_info and relationship tables... */
		print 'select all the info to generate the single profile information'
		select login_info.user_id as "user_id"
			, login_info.user_name as "user_name"
			, login_info.membership_type as "membership_type"
			, sex.choice as "sex"
			, login_info.creation_date as "creation_date"
			, login_info.last_login as "last_login"
			, contact_info.city as "city"
			, state.choice as "state"
			, country.choice as "country"
			, sex_preference.choice as "sex_preference"
			, personal_info.age as "age"
			, marital_status.choice as "marital_status"
			, profession.choice as "profession"
			, income.choice as "income"
			, education.choice as "education"
			, religion.choice as "religion"
			, height.choice as "height"
			, weight.choice  as "weight"
			, eyes.choice as "eyes"
			, hair.choice as "hair"
			, personal_info.min_age_desired
			, personal_info.max_age_desired
			, cook.choice as "cook"
			, smoke.choice as "smoke"
			, drink.choice as "drink"
			, party.choice as "party"
			, political.choice as "political"
			, housing_status.choice as "housing_status"
			, relationship.prefer_not_to_say as "prefer_not_to_say"
			, relationship.any_relationship as "any_relationship"
			, relationship.hang_out as "hang_out"
			, relationship.short_term as "short_term"
			, relationship.long_term as "long_term"
			, relationship.talk_email as "talk_email"
			, relationship.photo_exchange as "photo_exchange"
			, relationship.marriage as "marriage"
			, relationship.other as "other"
			, about_info.screen_quote as "screen_quote"
			, about_info.about_yourself as "about_yourself"
			, pictures.photo_1 as "pic 1"
			, pictures.photo_2 as "pic 2"
			, pictures.photo_3 as "pic 3"
			, pictures.photo_4 as "pic 4"
			, pictures.photo_5 as "pic 5"
		from login_info
			, contact_info
			, personal_info
			, relationship
			, about_info
			, sex_preference
			, marital_status
			, profession
			, income
			, education
			, religion
			, height
			, weight
			, eyes
			, hair
			, cook
			, smoke
			, drink
			, party
			, political
			, housing_status
			, sex
			, state
			, country
			, pictures
		where login_info.user_name = contact_info.user_name
			and login_info.user_name = personal_info.user_name
			and login_info.user_name = relationship.user_name
			and login_info.user_name = about_info.user_name
			and login_info.user_name = pictures.user_name
			and login_info.sex = sex.value
			and ( 
				about_info.questionable = 0 
				OR 
				@@ViewMyOwnProfile = '1' 
			         )
			and contact_info.state = state.value
			and contact_info.country = country.value
			and personal_info.sex_preference = sex_preference.value
			and personal_info.marital_status = marital_status.value
			and personal_info.profession = profession.value
			and personal_info.income = income.value
			and personal_info.education = education.value
			and personal_info.religion = religion.value
			and personal_info.height = height.value
			and personal_info.weight = weight.value
			and personal_info.eyes = eyes.value
			and personal_info.hair = hair.value
			and personal_info.cook = cook.value
			and personal_info.smoke = smoke.value
			and personal_info.drink = drink.value
			and personal_info.party = party.value
			and personal_info.political = political.value
			and personal_info.housing_status = housing_status.value
			and personal_info.user_name = @UserNameBeingSearched
		
		return 1
	END
GO
SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS ON 
GO

SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS OFF 
GO

CREATE PROCEDURE [transaction_credit_card_send]
@TransactionID CHAR(52)
, @BatchTransactionID VARCHAR(60)
, @UserName VARCHAR(32)
, @XCustomerIP VARCHAR(15)
, @MonthsJoined VARCHAR(3)
, @Amount VARCHAR(8)
, @NameOnCard VARCHAR(64)
, @CardType CHAR(1)
, @CVV2Code CHAR(4)
, @AccountNumber VARCHAR(32)
, @ExpirationMonth CHAR(2)
, @ExpirationYear CHAR(4)
, @TransactionType VARCHAR(18)
, @XTransID CHAR(9)
, @XDescription VARCHAR(256)
, @XMethod VARCHAR(18)
, @BankABACode VARCHAR(9)
, @BankAccountNumber VARCHAR(32)

 AS

-- Check email has been verified
if ( (SELECT is_email_verified FROM login_info WHERE user_name = @UserName) = '0' )
	BEGIN--  DENIED
		print 'email address has not been verified'
		return 201
	END
-- END Verify Permissions

DECLARE @@DateOfThisTransaction DATETIME
DECLARE @@DateOfNextTransaction DATETIME

DECLARE @@MembershipType 	CHAR(4)
DECLARE @@IsMembershipActive	CHAR(1)

DECLARE @@UserId			VARCHAR(10)
SELECT @@UserId = (SELECT user_id from login_info where user_name = @UserName)

-- Get user info from billing_info table...
SELECT @@IsMembershipActive = (SELECT is_membership_active from billing_info where user_name = @UserName)
	
print 'Method = ' + @XMethod

-- Check if user is already a paying member...
SELECT @@MembershipType = (SELECT membership_type from login_info where user_name = @UserName)
IF( 
	(@@MembershipType != '1' AND @@MembershipType != '2') 
	OR (@TransactionType = 'CREDIT' OR @TransactionType = 'VOID')
	OR ( @@IsMembershipActive = '0' AND (@@MembershipType = '1' OR @@MembershipType = '2') ) )
	BEGIN
	
		-- Set the current date 
		SELECT @@DateOfThisTransaction = GETDATE()
		
		-- Add @MonthsJoined to the DateOfThisTransaction to initialize the DateOfNextTransaction
		SELECT @@DateOfNextTransaction = DATEADD(MONTH, CONVERT (INT, @MonthsJoined), @@DateOfThisTransaction)

---------------------------------------
-- transactions_log
---------------------------------------
		PRINT 'Enter new transaction into transactions_log table'
		INSERT INTO transactions_log (transaction_id
				, batch_transaction_id
				, user_id
				, user_name
				, x_customer_IP
				, card_type
				, name_on_card
				, cvv2_code
				, account_number
				, expiration_month
				, expiration_year
				, transaction_type
				, x_response_code
				, months_joined
				, amount
				, date_of_this_transaction
				, date_of_next_transaction
				, x_response_reason_text
				, x_trans_id
				, x_description
				, x_method
				, bank_ABA_code
				, bank_account_number
				) 
		VALUES ( @TransactionID
			, @BatchTransactionID
			, @@UserId
			, @UserName
			, @XCustomerIP
			, @CardType
			, @NameOnCard
			, @CVV2Code
			, @AccountNumber
			, @ExpirationMonth
			, @ExpirationYear
			, @TransactionType
			, '0' -- @XResponseCode
			, @MonthsJoined
			, CONVERT (MONEY, @Amount)
			, @@DateOfThisTransaction
			, @@DateOfNextTransaction
			, 'ERROR: No Response From Server' -- @XResponseReasonText
			, @XTransID
			, @XDescription
			, @XMethod
			, @BankABACode
			, @BankAccountNumber
			)

		-- Determine if the current user has ever used a restricted IP...
		IF EXISTS (SELECT IP_address FROM restricted_IP
				WHERE IP_address IN (SELECT IP_address FROM customer_IP WHERE user_name = @UserName AND user_id = @@UserId)
			     )
			BEGIN
				-- update the transactions_log table with the fields returned from Authorize.Net
				PRINT 'ERROR:  Restricted IP address (' + @UserName + ')'
				UPDATE transactions_log 
					SET x_response_code = '9' -- a value of '9' indicates that the user has used a restricted IP in the past
					WHERE transaction_id = @TransactionID
				RETURN 666
			END
	RETURN 1
	END
ELSE
	BEGIN
		PRINT 'ERROR:  User is already a paying member (' + @UserName + '):(' + @@MembershipType + ')'
		RETURN 666
	END
GO
SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS ON 
GO

SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS OFF 
GO




CREATE PROCEDURE [transaction_manual_check_post]
@TransactionID CHAR(52)
, @UserName VARCHAR(32)
, @MonthsJoined VARCHAR(3)
, @Amount VARCHAR(8)
, @XTransID CHAR(9)
, @XMd5Hash VARCHAR(50)
, @XDescription VARCHAR(256)
, @NameOnCard VARCHAR(64)
, @BankABACode VARCHAR(9)
, @BankAccountNumber VARCHAR(32)

 AS

-- Check email has been verified
if ( (SELECT is_email_verified FROM login_info WHERE user_name = @UserName) = '0' )
	BEGIN--  DENIED
		print 'email address has not been verified'
		return 201
	END
-- END Verify Permissions

DECLARE @@DateOfThisTransaction DATETIME
DECLARE @@DateOfNextTransaction DATETIME

DECLARE @@MembershipType 		CHAR(4)
DECLARE @@IsMembershipActive	CHAR(1)

DECLARE @@UserId VARCHAR(10)
SELECT @@UserId = (SELECT user_id from login_info where user_name = @UserName)

-- Get user info from billing_info table...
SELECT @@IsMembershipActive = (SELECT is_membership_active from billing_info where user_name = @UserName)
	
-- Check if user is already a paying member...
SELECT @@MembershipType = (SELECT membership_type from login_info where user_name = @UserName)
IF( (@@MembershipType != '1' AND @@MembershipType != '2') OR ( @@IsMembershipActive = '0' AND (@@MembershipType = '1' OR @@MembershipType = '2') ) )
	BEGIN
		-- Set the current date 
		SELECT @@DateOfThisTransaction = GETDATE()
		
		-- Add @MonthsJoined to the DateOfThisTransaction to initialize the DateOfNextTransaction
		SELECT @@DateOfNextTransaction = DATEADD(MONTH, CONVERT (INT, @MonthsJoined), @@DateOfThisTransaction)
		
---------------------------------------
-- login_info
---------------------------------------
--  update the membership type to 1
		print 'update login_info table'
		IF( (SELECT date_started_paying FROM login_info where user_name = @UserName) = NULL)
			BEGIN
				-- update login_info table to reflect the successful transaction
				UPDATE login_info 
					SET membership_type 	= '1'
						, date_started_paying = @@DateOfThisTransaction
					WHERE user_name = @UserName
			END
		ELSE
			BEGIN
				-- update login_info table to reflect the successful transaction
				UPDATE login_info 
					SET membership_type 	= '1'
					WHERE user_name = @UserName
			END
---------------------------------------
-- billing_info
---------------------------------------
			print 'Updating the Bank Info in the billing_info table'
			-- Determine if the user_name is unique in the billing_info table
			if exists (select user_name from billing_info where user_name = @UserName)
			BEGIN
				-- If the user_name is NOT unique update the billing_info table with the current information
				print 'update billing_info table'
				update billing_info 
					set  is_membership_active = '1'
						, date_membership_expires = @@DateOfNextTransaction
						, bank_ABA_code = @BankABACode
						, bank_account_number = @BankAccountNumber
					where user_name = @UserName
			END
			else -- user has no billing_inifo table
			BEGIN
				-- If the user_name is unique add the user to the billing_info table
				print 'user_name IS unique in billing_info'
				insert into billing_info (user_name
						, card_type
						, name_on_card
						, account_number
						, expiration_month
						, expiration_year
						, is_membership_active
						, date_membership_expires
						, bank_ABA_code
						, bank_account_number
						) 
				values (@UserName
					, '9' -- 9 = Manual Check
					, @NameOnCard
					, '0'
					, '00'
					, '0000'
					, '1'
					, @@DateOfThisTransaction
					, @BankABACode
					, @BankAccountNumber
					)
			END

---------------------------------------
-- recurring_transactions
---------------------------------------
			print 'Updating the Credit Card info in the recurring_transactions  table'
			-- Determine if the user_name is unique in the recurring_transactions table
			if exists (select user_name from recurring_transactions where user_name = @UserName)
			BEGIN
				-- If the user_name is NOT unique update the recurring_transactions table with the current information
				print 'update recurring_transactions table'
				update recurring_transactions 
					set sendable = '0' -- 0 = NOT ok to process
						, transaction_type = 'MANUAL_CHECK'
						, date_of_this_transaction = @@DateOfThisTransaction
						, date_of_next_transaction = @@DateOfNextTransaction
						, card_type = '9' -- 9 = Manual Check
						, name_on_card = @NameOnCard
						, account_number = ''
						, expiration_month = ''
						, expiration_year = ''
						, x_method = 'MANUAL'
						,  bank_ABA_code = @BankABACode
						, bank_account_number = @BankAccountNumber
					where user_name = @UserName
			END
			else
			BEGIN
				-- If the user_name is unique add the user to the recurring_transactions table
				print 'user_name IS unique in recurring_transactions'
				insert into recurring_transactions (user_name
								, sendable
								, transaction_type
								, date_of_this_transaction
								, date_of_next_transaction
								, card_type
								, name_on_card
								, account_number
								, expiration_month
								, expiration_year
								, x_method
								, bank_ABA_code
								, bank_account_number
								) 
						values (@UserName
							, '0' -- 0 = NOT ok to process
							, 'MANUAL_CHECK'
							, @@DateOfThisTransaction
							, @@DateOfNextTransaction
							, '9' -- 9 = Manual Check
							, @NameOnCard
							, '0'
							, '00'
							, '0000'
							, 'MANUAL'
							, @BankABACode
							, @BankAccountNumber
							)
			END


---------------------------------------
-- transactions_log
---------------------------------------
		PRINT 'Enter new transaction into transactions_log table'
		INSERT INTO transactions_log (transaction_id
				, batch_transaction_id
				, user_id
				, user_name
				, card_type
				, name_on_card
				, account_number
				, expiration_month
				, expiration_year
				, transaction_type
				, x_response_code
				, months_joined
				, amount
				, date_of_this_transaction
				, date_of_next_transaction
				, x_response_reason_text
				, x_trans_id
				, x_md5_hash
				, x_description
				, x_method
				, bank_ABA_code
				, bank_account_number
				) 
		VALUES ( @TransactionID
			, ''
			, @@UserId
			, @UserName
			, '9' -- 9 = Manual Check
			, @NameOnCard
			, '0'
			, '00'
			, '0000'
			, 'MANUAL_CHECK'
			, '0' -- @XResponseCode
			, @MonthsJoined
			, CONVERT (MONEY, @Amount)
			, @@DateOfThisTransaction
			, @@DateOfNextTransaction
			, 'Not Cleared' -- @XResponseCode
			, @XTransID
			, @XMd5Hash
			, @XDescription
			, 'MANUAL'
			, @BankABACode
			, @BankAccountNumber
			)
		RETURN 1
		
	END
ELSE
	BEGIN
		PRINT 'ERROR:  User is already a paying member (' + @UserName + '):(' + @@MembershipType + ')'
		RETURN 666
	END
GO
SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS ON 
GO

SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS ON 
GO


CREATE PROCEDURE [updateLoginInfo]
@UserId int
, @UserName varchar(32)
, @MembershipType char
, @Password varchar(16)
, @PasswordHint varchar(64)
, @Email varchar(64)
, @Sex char
, @CreationDate varchar(32)
, @LastLogin varchar(32)
, @PhotoSubmitted int -- not used 
, @DateStartedPaying VARCHAR(32) = ''
, @EmailVerificationCode VARCHAR(17) = ''
, @IsEmilVerified VARCHAR(2) = ''
, @WhereDidYouHearAboutUs VARCHAR(128) = ''
, @AdvertisingCampaignCode VARCHAR(32) = ''

 AS
-- UserId must be declared

-- membership_type, creation_date, and last_login must be declared
DECLARE @current_user_name varchar(32)

select @current_user_name = (select user_name from login_info where user_name = @UserName)

if (@current_user_name = @UserName)
BEGIN
	--If the user_name is unique add the user to the login_info table and exit with a return value of 1
	print 'user_name (' + @current_user_name + ')  IS remaining  (' + @UserName
	update login_info 
		set password = @Password
			, password_hint = @PasswordHint
--			, email = @Email	-- The user is no longer allowed to change their email using this page since 3-30-2002
			, sex = @Sex
		where user_id = @UserId
	return 1
END
ELSE
	BEGIN
		--Determine if the user_name is unique
		if exists (select user_name from login_info where user_name = @UserName)
		BEGIN
			--If the user_name is not unique exit with a return value of 666
			print 'user_name  is not unique'
			return 666
		END
	ELSE
	BEGIN
		select @current_user_name = (select user_name from login_info where user_id = @UserId)
		--If the user_name is unique add the user to the login_info table and exit with a return value of 1
		print 'user_name (' + @current_user_name + ')  IS unique and being changed to (' + @UserName + ')  in all tables'
		print 'Updating the login_info table'
		update login_info 
			set user_name = @UserName
				, password = @Password
				, password_hint = @PasswordHint
--				, email = @Email	-- The user is no longer allowed to change their email using this page since 3-30-2002
				, sex = @Sex
			where user_id = @UserId

		-- Update user_name in all other tables...

		-- Update contact_info table
		print 'Updating the contact_info table'
		update contact_info 
			set user_name = @UserName
			where user_name = @current_user_name

		-- Update personal_info table
		print 'Updating the personal_info table'
		update personal_info 
			set user_name = @UserName
			where user_name = @current_user_name

		-- Update about_info table
		print 'Updating the about_info table'
		update about_info 
			set user_name = @UserName
			where user_name = @current_user_name

		-- Update pictures table
		print 'Updating the pictures table'
		update pictures 
			set user_name = @UserName
			where user_name = @current_user_name

		-- Update relationship table
		print 'Updating the relationship table'
		update relationship 
			set user_name = @UserName
			where user_name = @current_user_name

		-- Update sent_to in mail table
		print 'Updating the sent_to field in the mail table'
		update mail 
			set sent_to = @UserName
			where sent_to = @current_user_name

		-- Update sent_from in mail table
		print 'Updating the sent_from field in the mail table'
		update mail 
			set sent_from = @UserName
			where sent_from = @current_user_name

		-- Update user_name in book_marks table
		print 'Updating the sent_to field in the book_marks table'
		update book_marks 
			set user_name = @UserName
			where user_name = @current_user_name

		-- Update book_mark in book_marks table
		print 'Updating the book_mark field in the book_marks table'
		update book_marks 
			set book_mark = @UserName
			where book_mark = @current_user_name

		-- Update billing_info table
		print 'Updating the billing_info table'
		update billing_info 
			set user_name = @UserName
			where user_name = @current_user_name

		-- Update recurring_transactions table
		print 'Updating the recurring_transactions table'
		update recurring_transactions 
			set user_name = @UserName
			where user_name = @current_user_name

		-- Update membership_cancellation table
		print 'Updating the membership_cancellation table'
		update membership_cancellation 
			set user_name = @UserName
			where user_name = @current_user_name

		-- Update transactions_log table
		print 'Updating the transactions_log table'
		update transactions_log 
			set user_name = @UserName
			where user_name = @current_user_name
			and user_id = @UserId

		return 1
	END
END
GO
SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS ON 
GO

SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS OFF 
GO

CREATE PROCEDURE [verifyEmailAddress]
@UserName varchar(32)
, @Password varchar(16)
, @Email varchar(64)
, @EmailVerificationCode varchar(20)

 AS

-- Determine if the user_name, email, password and email_verification_code match before validating email address...
IF ( (SELECT password FROM login_info WHERE user_name = @UserName AND email = @Email AND email_verification_code = @EmailVerificationCode) = @Password)
	BEGIN
		-- Update email in login_info table
		print 'Updating email_verification_code for user (' + @UserName + ')'
		update login_info 
			set is_email_verified = '1'
			where user_name = @UserName
				AND password = @Password
				AND email = @Email
				AND email_verification_code = @EmailVerificationCode
		return 1
	END
ELSE
	BEGIN
		-- If the user_name, email and password do not match exit with a return value of 666 
		PRINT 'user_name and password did not match or Email Verification Code is incorrect so we are unable to verify that (' + @Email + ') is the correct email address for user (' + @UserName + ')' -- the first part of this string must remain as "user_name and password did not match" because it is being checked for in "msg_handler" 
		RETURN 666
	END
GO
SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS ON 
GO

SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS OFF 
GO



CREATE PROCEDURE [verifyMembershipTypePermissions]
	@UserName varchar(32)
	, @FeatureRequested varchar (32)
 AS

-- Check user_name is blank
if ( @UserName = '' )
	BEGIN--  DENIED
		print 'user_name does not exist'
		return 140
	END
-- END Verify Permissions

-- Check email has been verified
if ( (SELECT is_email_verified FROM login_info WHERE user_name = @UserName) != '1' )
	BEGIN--  DENIED
		print 'email address has not been verified'
		return 201
	END
-- END Verify Permissions

-- Check if this is a promotional membership_type
if (
	 (select membership_type.date_promotion_ended
		from login_info
		  , membership_type
		where login_info.membership_type = membership_type_id
		and login_info.user_name = @UserName
	) != NULL
   )
BEGIN
	print 'Promotional Membership'
	print 'Must check Promotion Date'
	if (
		 (select membership_type.date_promotion_ended
			from login_info
			  , membership_type
			where login_info.membership_type = membership_type_id
			and login_info.user_name = @UserName
		) > getdate()
	   )
	BEGIN
		print 'Promotion is active'
	END
	else
	BEGIN
		print 'Promotion Expired'
		return 600
	END	
END
else
BEGIN
	print 'Non-Promotional Membership'
END

if ( @FeatureRequested = 'allow_search_simple' )
BEGIN
	print 'Check allow_search_simple permissions'
	if (
		 (select membership_type.allow_search_simple
			from login_info
			  , membership_type
			where login_info.membership_type = membership_type_id
			and login_info.user_name = @UserName
		) = 1
	   )
	BEGIN
		print 'Permission GRANTED for allow_search_simple'
		return 1
	END
	else
	BEGIN
		print 'Permission DENIED for allow_search_simple'
		return 601
	END
END
if ( @FeatureRequested = 'allow_search_advanced' )
BEGIN
	print 'Check allow_search_advanced permissions'
	if (
		 (select membership_type.allow_search_advanced
			from login_info
			  , membership_type
			where login_info.membership_type = membership_type_id
			and login_info.user_name = @UserName
		) = 1
	   )
	BEGIN
		print 'Permission GRANTED for allow_search_advanced'
		return 1
	END
	else
	BEGIN
		print 'Permission DENIED for allow_search_advanced'
		return 602
	END
END
if ( @FeatureRequested = 'allow_view_profiles' )
BEGIN
	print 'Check allow_view_profiles permissions'
	if (
		 (select membership_type.allow_view_profiles
			from login_info
			  , membership_type
			where login_info.membership_type = membership_type_id
			and login_info.user_name = @UserName
		) = 1
	   )
	BEGIN
		print 'Permission GRANTED for allow_view_profiles'
		return 1
	END
	else
	BEGIN
		print 'Permission DENIED for allow_view_profiles'
		return 603
	END
END
if ( @FeatureRequested = 'allow_mail_receive' )
BEGIN
	print 'Check allow_mail_receive permissions'
	if (
		 (select membership_type.allow_mail_receive
			from login_info
			  , membership_type
			where login_info.membership_type = membership_type_id
			and login_info.user_name = @UserName
		) = 1
	   )
	BEGIN
		print 'Permission GRANTED for allow_mail_receive'
		return 1
	END
	else
	BEGIN
		print 'Permission DENIED for allow_mail_receive'
		return 604
	END
END
if ( @FeatureRequested = 'allow_mail_read' )
BEGIN
	print 'Check allow_mail_read permissions'
	if (
		 (select membership_type.allow_mail_read
			from login_info
			  , membership_type
			where login_info.membership_type = membership_type_id
			and login_info.user_name = @UserName
		) = 1
	   )
	BEGIN
		print 'Permission GRANTED for allow_mail_read'
		return 1
	END
	else
	BEGIN
		print 'Permission DENIED for allow_mail_read'
		return 605
	END
END
if ( @FeatureRequested = 'allow_mail_send' )
BEGIN
	print 'Check allow_mail_send permissions'
	if (
		 (select membership_type.allow_mail_send
			from login_info
			  , membership_type
			where login_info.membership_type = membership_type_id
			and login_info.user_name = @UserName
		) = 1
	   )
	BEGIN
		print 'Permission GRANTED for allow_mail_send'
		return 1
	END
	else
	BEGIN
		print 'Permission DENIED for allow_mail_send'
		return 606
	END
END
if ( @FeatureRequested = 'allow_mail_reply' )
BEGIN
	print 'Check allow_mail_reply permissions'
	if (
		 (select membership_type.allow_mail_reply
			from login_info
			  , membership_type
			where login_info.membership_type = membership_type_id
			and login_info.user_name = @UserName
		) = 1
	   )
	BEGIN
		print 'Permission GRANTED for allow_mail_reply'
		return 1
	END
	else
	BEGIN
		print 'Permission DENIED for allow_mail_reply'
		return 607
	END
END
if ( @FeatureRequested = 'allow_romance_wizard' )
BEGIN
	print 'Check allow_romance_wizard permissions'
	if (
		 (select membership_type.allow_romance_wizard
			from login_info
			  , membership_type
			where login_info.membership_type = membership_type_id
			and login_info.user_name = @UserName
		) = 1
	   )
	BEGIN
		print 'Permission GRANTED for allow_romance_wizard'
		return 1
	END
	else
	BEGIN
		print 'Permission DENIED for allow_romance_wizard'
		return 608
	END
END
if ( @FeatureRequested = 'allow_chat_view' )
BEGIN
	print 'Check allow_chat_view permissions'
	if (
		 (select membership_type.allow_chat_view
			from login_info
			  , membership_type
			where login_info.membership_type = membership_type_id
			and login_info.user_name = @UserName
		) = 1
	   )
	BEGIN
		print 'Permission GRANTED for allow_chat_view'
		return 1
	END
	else
	BEGIN
		print 'Permission DENIED for allow_chat_view'
		return 609
	END
END
if ( @FeatureRequested = 'allow_chat_use' )
BEGIN
	print 'Check allow_chat_use permissions'
	if (
		 (select membership_type.allow_chat_use
			from login_info
			  , membership_type
			where login_info.membership_type = membership_type_id
			and login_info.user_name = @UserName
		) = 1
	   )
	BEGIN
		print 'Permission GRANTED for allow_chat_use'
		return 1
	END
	else
	BEGIN
		print 'Permission DENIED for allow_chat_use'
		return 610
	END
END
if ( @FeatureRequested = 'allow_view_stats' )
BEGIN
	print 'Check allow_view_stats permissions'
	if (
		 (select membership_type.allow_view_stats
			from login_info
			  , membership_type
			where login_info.membership_type = membership_type_id
			and login_info.user_name = @UserName
		) = 1
	   )
	BEGIN
		print 'Permission GRANTED for allow_view_stats'
		return 1
	END
	else
	BEGIN
		print 'Permission DENIED for allow_view_stats'
		return 611
	END
END
GO
SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS ON 
GO

