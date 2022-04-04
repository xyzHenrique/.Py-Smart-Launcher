::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFBNRQhaLAE+/Fb4I5/jH6vK7pkQOQN4qdobVyaCPLOxe40bre9gk1XU6
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSDk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
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
::Zh4grVQjdCyDJGyX8VAjFBNRQhaLAE+/Fb4I5/jH6vK7pkQOQN4ZYLje2JiPNe4Q4kD2OJc4wnVPlsICHw9Zch7laxcxyQ==
::YB416Ek+ZW8=
::
::
::978f952a14a936cc963da21a135fa983
:: -----------------------------
:: ~ Henrique Rodrigues Pereira
:: -----------------------------

@ECHO OFF

pushd %~dp0
if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit /b)

CHOICE /C yn /M "(Y) Yes uninstall, (N) No uninstall"
ECHO.

PING -n 3 127.0.0.1 > nul

SET target_1=FxWebLauncher
SET target_2=C:
SET target_3=FxWebLauncher_3-7-0

IF %ERRORLEVEL% == 0 ( 
    ECHO Deleting FOLDER: "%target_2%\%target_3%\" and shortcuts
    ECHO.

    @RD /S /Q "%target_2%\%target_3%\" 
    
    COLOR 2 
    ECHO OK
) ELSE (
    COLOR 4
    
    ECHO Failed to delete FOLDER "%target_2%\%target_3%\"
    PING -n 2 127.0.0.1 > nul
)

IF %ERRORLEVEL% == 0 ( 
	DEL "%userprofile%\Start Menu\Programs\Startup\%target_1%.lnk"
	DEL "%userprofile%\Desktop\%target_1%.lnk"
) ELSE (
	DEL "%username%\Start Menu\Programs\Startup\%target_1%.lnk"
	DEL "%username%\Desktop\target_1.lnk"
)

PAUSE
EXIT