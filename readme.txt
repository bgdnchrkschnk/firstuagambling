1. Create a separate venv
2. Install all needed dependencies using command 'pip install -Ur requirements.txt'

pytest -s -v -k TestRegistrationFlow --headed --browser=firefox --slowmo=500

pytest -s -v -k TestRegistrationForm --headed --browser=firefox --slowmo=500

pytest -s -v -k TestsIntegration