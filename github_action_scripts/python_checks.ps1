$ErrorActionPreference = "Stop"
python -m venv "$Env:USERPROFILE\venv"
$Env:USERPROFILE\venv\Scripts\activate.bat
python -VV
python -m site
python -m pip install -U pip
echo dumping pre-installed packages
python -m pip freeze
echo installing pip packages
python -m pip install -e .
echo running tests
set CRATE_RUN_WITHOUT_LOCAL_SETTINGS=True
crate_anon_demo_config > "$Env:USERPROFILE\crate_anon_config,ini"
Set-Variable -Name "CRATE_ANON_CONFIG" -Value "$Env:USERPROFILE\crate_anon_config.ini"
pytest -v
