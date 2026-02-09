@echo off
echo ==========================================
echo      Starting Reddit Insights App
echo ==========================================

echo.
echo [1/3] Starting Backend Server...
echo ------------------------------------------
start /min "Reddit Backend" python server.py
echo Backend server started in new window.

echo.
echo [2/3] Fetching initial data...
echo ------------------------------------------
python execution/fetch_reddit_posts.py --subreddits n8n automation --limit 100 --top 5 --output reddit-viewer/public/data.json

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to fetch posts. Check logs for details.
    pause
    exit /b %errorlevel%
)

echo.
echo [3/3] Starting Web Interface...
echo ------------------------------------------
cd reddit-viewer
call npm install
npm run dev
