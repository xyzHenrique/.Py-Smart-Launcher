::[Bat To Exe Converter]
::
::fBE1pAF6MU+EWHreyHcjLQlHcAyHMnmzOpEZ++Pv4Pq7p1UhUOssbLP9woOLIswS/0vnfZM/6SkXz4ZcQgFRbnI=
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFBNRQhaLAE+/Fb4I5/jH6vK7pkQOQN42dpzP27iCJfJe40bre9gk1XU6
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSDk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSTk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpSI=
::egkzugNsPRvcWATEpSI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAjk
::YxY4rhs+aU+IeA==
::cxY6rQJ7JhzQF1fEqQJQ
::ZQ05rAF9IBncCkqN+0xwdVsHAlPMbAs=
::ZQ05rAF9IAHYFVzEqQIWMCxRTiiDKWW5DrAOiA==
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATE/FYkOAgOA0uFNX+yE7dS6+f2oNiuq04WGbJuK8C7
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCyDJGyX8VAjFBNRQhaLAE+/Fb4I5/jH6vK7pkQOQN4ZYLje2JiPNe4Q4kD2OJc4wnVTltgYDRdUewDlaxcxyQ==
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
:: -----------------------------
:: ~ Henrique Rodrigues Pereira
:: -----------------------------

@ECHO OFF

pushd %~dp0
if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit /b)

SET current_dir=%cd%

SET archive_input=FxWebLauncher_3-7-0.zip
SET archive_output=.\extract\

SET target_1=FxWebLauncher
SET target_2=C:
SET target_3=FxWebLauncher_3-7-0

ECHO Starting file verification...
ECHO.

:: Check if input exists
IF EXIST "%archive_input%" (
	COLOR 2

	SET input=1
	
	ECHO "%archive_input%" OK!
	ECHO.
	
	PING -n 3 127.0.0.1 > nul
	
	) ELSE (
	COLOR 4

	ECHO the file "%archive_input%" does not exist.
	PING -n 3 127.0.0.1 > nul

	PAUSE
	EXIT
)

:: Main
IF "%input%"=="1" (		
	
	:: Extract 
	IF %ERRORLEVEL% == 0 (
		CLS
		COLOR 6
		
		ECHO Extracting: "%archive_input%" please wait...
		ECHO.

		:: Check if output exists
		IF EXIST %archive_output% (
			RMDIR "%archive_output%" /S /Q
			PING -n 3 127.0.0.1 > nul
		) 
		
		powershell.exe -NoP -NonI -Command "Expand-Archive '%archive_input%' '%archive_output%'

		ECHO Files extracted to: "%archive_output%"
		ECHO.

		PING -n 3 127.0.0.1 > nul

	) ELSE (
		COLOR 4
		
		ECHO Failed to extract: "%archive_input%"
		PING -n 3 127.0.0.1 > nul
		
		PAUSE
		EXIT
	)
	
	:: Move
	IF %ERRORLEVEL% == 0 (
		CLS

		ECHO Moving "%target_1%" to "%target_2%"
		ECHO.

		mkdir "%target_2%\%target_3%\"
		CD %archive_output%
		robocopy "%target_1%" "%target_2%\%target_3%" /E /MOVE

		ECHO.

		CD %~dp0
		@RD /S /Q "%archive_output%"

		PING -n 2 127.0.0.1 > nul
	
	) ELSE (
		COLOR 4
		
		ECHO Failed to "%target_1%" to "%target_2%"
		PING -n 2 127.0.0.1 > nul
		
		PAUSE
		EXIT
	)

) ELSE (
	COLOR 4
	
	ECHO Failed to run.
	PING -n 2 127.0.0.1 > nul
	
	PAUSE
	EXIT
)

cd %current_dir%

@ECHO ON
set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = "%userprofile%\Start Menu\Programs\Startup\%target_1%.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "%target_2%\%target_3%\%target_1%.exe" >> %SCRIPT%
echo oLink.WorkingDirectory = "%target_2%\%target_3%" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%
cscript /nologo %SCRIPT%
del %SCRIPT%

set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = "%userprofile%\Desktop\%target_1%.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "%target_2%\%target_3%\%target_1%.exe" >> %SCRIPT%
echo oLink.WorkingDirectory = "%target_2%\%target_3%" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%
cscript /nologo %SCRIPT%
del %SCRIPT%

@ECHO OFF
PING -n 2 127.0.0.1 > nul
COLOR 2
ECHO.
ECHO END
ECHO.

PAUSE
EXIT

