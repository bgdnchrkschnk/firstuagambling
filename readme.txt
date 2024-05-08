Use python interpreter 3.11+
1. Create and activate separate venv
2. Install all needed dependencies using command 'pip install -Ur requirements.txt'
3. Install playwright browser drivers using command 'playwright install'

To run e2e tests:
pytest -s -v -k TestRegistrationFlow --headed --browser=firefox --slowmo=500 --alluredir=${HOME}/PycharmProjects/allure_reports

pytest -s -v -k TestRegistrationForm --headed --browser=firefox --slowmo=500 --alluredir=${HOME}/PycharmProjects/allure_reports

To run integration tests:
pytest -s -v -k TestsIntegration --alluredir=${HOME}/PycharmProjects/allure_reports
