echo on
cd %GITHUB_WORKSPACE%
python -m venv "%USERPROFILE%\venv" || exit /b %errorlevel%
%USERPROFILE%\venv\Scripts\activate || exit /b %errorlevel%
python -VV || exit /b %errorlevel%
python -m site || exit /b %errorlevel%
python -m pip install -U pip || exit /b %errorlevel%
echo dumping pre-installed packages
python -m pip freeze || exit /b %errorlevel%
echo installing pip packages
python -m pip install -e . || exit /b %errorlevel%
echo running tests
set CRATE_RUN_WITHOUT_LOCAL_SETTINGS=True
pytest -v || exit /b %errorlevel%
