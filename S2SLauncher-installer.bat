:: -----------------------------
:: ~ Henrique R.
:: -----------------------------

@ECHO OFF

pushd %~dp0
if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit /b)

SET install_dir=%cd%

SET archive_input=S2SLauncher_3-7-0.zip
SET archive_output=.\extract\

SET target_1=S2SLauncher
SET target_2=C:

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

	ECHO the file "%_archive_input%" does not exist.
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

		mkdir "C:\S2SLauncher_3-7-0\"
		CD %archive_output%
		robocopy "S2SLauncher" "C:\S2SLauncher_3-7-0" /E /MOVE

		ECHO.
		ECHO.

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

cd %install_dir%

:: STARTUP
set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = "%userprofile%\Start Menu\Programs\Startup\S2SLauncher.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "c:\S2SLauncher_3-7-0\S2SLauncher.exe" >> %SCRIPT%
echo oLink.WorkingDirectory = "C:\S2SLauncher_3-7-0" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%
cscript /nologo %SCRIPT%
del %SCRIPT%

:: DESKTOP
set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = "%userprofile%\Desktop\S2SLauncher.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "C:\S2SLauncher_3-7-0\S2SLauncher.exe" >> %SCRIPT%
echo oLink.WorkingDirectory = "C:\S2SLauncher_3-7-0" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%
cscript /nologo %SCRIPT%
del %SCRIPT%

PING -n 2 127.0.0.1 > nul
COLOR 2
ECHO.
ECHO OK
ECHO.
PING -n 2 127.0.0.1 > nul

CD %~dp0
@RD /S /Q "%archive_output%"

PAUSE
EXIT

