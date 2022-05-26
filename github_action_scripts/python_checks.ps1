$ErrorActionPreference = "Stop"
cd "$env:USERPROFILE"
python -m venv venv
.\venv\Scripts\activate
python -VV
python -m site
python -m pip install -U pip
echo dumping pre-installed packages
python -m pip freeze
echo installing pip packages
python -m pip install -e .
echo running tests
$env:CRATE_RUN_WITHOUT_LOCAL_SETTINGS = "True"
$env:CRATE_ANON_CONFIG = "$env:USERPROFILE\crate_anon_config.ini"
crate_anon_demo_config > "$env:CRATE_ANON_CONFIG"
cd "$env:GITHUB_WORKSPACE"
pytest -v
