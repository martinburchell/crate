cd %GITHUB_WORKSPACE%
python -m venv "%HOME%\venv"
%HOME%\venv\Scripts\activate
python -VV
python -m site
python -m pip install -U pip
echo dumping pre-installed packages
python -m pip freeze
echo installing pip packages
python -m pip install -e .
echo running tests
set CRATE_RUN_WITHOUT_LOCAL_SETTINGS=True
pytest -v
