import pytest

from tests.test_setup import TestSetup


@pytest.mark.usefixtures("pages_login")
class TestApiLocation(TestSetup):

    @pytest.mark.api
    def test_api_info(self):
        personal_response = self.session.get(
            "https://opensource-demo.orangehrmlive.com/web/index.php/api/v2/pim/employees/7/personal-details"
        )

        assert (
            personal_response.status_code == 200
        ), f"Expected status code 200, but got {personal_response.status_code}"

        employee_response = self.session.get(
            "https://opensource-demo.orangehrmlive.com/web/index.php/api/v2/pim/employees"
        )

        assert (
            employee_response.status_code == 200
        ), f"Expected status code 200, but got {personal_response.status_code}"

        try:
            personal_data = personal_response.json()
            employee_data = employee_response.json()

            emp_number = personal_data.get("data", {}).get("empNumber")
            last_name = personal_data.get("data", {}).get("lastName")
            first_name = personal_data.get("data", {}).get("firstName")
            employee_id = personal_data.get("data", {}).get("employeeId")

            matched_data = None

            for employee in employee_data.get("data", []):
                if employee.get("empNumber") == emp_number:
                    matched_data = employee
                    break
            
            assert matched_data is not None, f"Can not find data match with empNum = {emp_number}"
            assert last_name == matched_data.get("lastName")
            assert first_name == matched_data.get("firstName")
            assert employee_id == matched_data.get("employeeId")
        except ValueError:
            assert False, "Response body is not in JSON format"
