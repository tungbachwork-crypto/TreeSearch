@echo off
setlocal enabledelayedexpansion
echo ===================================================
echo     AUTOMATED BATCH TESTING FOR SEARCH AGENTS
echo ===================================================
echo.
echo Available Methods: DFS, BFS, GBFS, AS, CUS1, CUS2
echo.

:: Prompt the user to enter the desired algorithm
set /p METHOD="Enter the algorithm you want to test: "

:: Automatically set the output file name based on the chosen method
set OUTPUT_FILE=results_%METHOD%.txt

echo.
echo Running %METHOD% on all map files...
echo Please wait...
echo.

:: Initialize the output file with a header
echo === %METHOD% BATCH TEST RESULTS === > %OUTPUT_FILE%
echo. >> %OUTPUT_FILE%

:: Loop through every .txt file inside the 'maps' folder
for %%f in (maps\*.txt) do (
    echo Testing map: %%f
    
    :: Write the map name to the output file
    echo -------------------------------------------------- >> %OUTPUT_FILE%
    echo Map File: %%f >> %OUTPUT_FILE%
    
    :: Execute the Python script with the user's chosen method
    python search.py "%%f" %METHOD% >> %OUTPUT_FILE%
    
    :: Add a blank line for readability
    echo. >> %OUTPUT_FILE%
)

echo.
echo ===================================================
echo ALL TESTS COMPLETED SUCCESSFULLY!
echo The results have been saved to "%OUTPUT_FILE%".
echo ===================================================
pause