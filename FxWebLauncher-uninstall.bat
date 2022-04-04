:: -----------------------------
:: ~ Henrique R.
:: -----------------------------

@ECHO OFF

pushd %~dp0
if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit /b)

CHOICE /C yn /M "(Y) Yes uninstall, (N) No uninstall"
ECHO.

PING -n 3 127.0.0.1 > nul

IF %ERRORLEVEL% == 0 ( 
    ECHO Deleting FOLDER: "C:\S2SLauncher_3-7-0\" and shortcuts...
    ECHO.

    @RD /S /Q "C:\S2SLauncher_3-7-0\" 
    DEL "%userprofile%\Start Menu\Programs\Startup\S2SLauncher.lnk"
    DEL "%userprofile%\Desktop\S2SLauncher.lnk"
    
    COLOR 2 
    ECHO OK
) ELSE (
    COLOR 4
    
    ECHO Failed to delete FOLDER "C:\S2SLauncher_3-7-0\"
    PING -n 2 127.0.0.1 > nul
)

PING -n 3 127.0.0.1 > nul

PAUSE
EXIT