from django.test import TestCase
from django import db
import datetime

from business.models import Employee, DailyTimeCard, \
    PayCheck, EmploymentRecord, Location


class EmployeeTestCase(TestCase):
    ############
    # Employee #
    ############
    def test_create_employee(self):
        data = {
            "emplId": 0,
            "name": "test name 0",
            "contact": "test contact 0"
        }

        self.assertEqual(Employee.objects.count(), 0)

        employee = Employee.objects.create(**data)

        self.assertEqual(Employee.objects.count(), 1)

        self.assertEqual(employee.emplId, data["emplId"])
        self.assertEqual(employee.name, data["name"])
        self.assertEqual(employee.contact, data["contact"])


    #############
    # Pay Check #
    #############
    def test_create_paycheck(self):
        employee = Employee.objects.create(
            emplId=0,
            name="test name 0",
            contact="test contact 0"
        )

        data = {
            "id": 1,
            "startDate": datetime.date(2020, 6, 1),
            "endDate": datetime.date(2020, 6, 30),
            "total": 520.31
        }

        self.assertEqual(PayCheck.objects.count(), 0)

        PayCheck.objects.create(**data)

        self.assertEqual(PayCheck.objects.count(), 1)

        paycheck = PayCheck.objects.get(id=data["id"])

        self.assertEqual(paycheck.id, data["id"])
        self.assertEqual(paycheck.startDate, data["startDate"])
        self.assertEqual(paycheck.endDate, data["endDate"])
        self.assertEqual(paycheck.total, data["total"])


    def test_delete_employee_doesnt_cascade_paycheck(self):
        employee = Employee.objects.create(
            emplId=0,
            name="test name 0",
            contact="test contact 0"
        )

        data = {
            "id": 1,
            "startDate": datetime.date(2020, 6, 1),
            "endDate": datetime.date(2020, 6, 30),
            "total": 520.31
        }

        self.assertEqual(PayCheck.objects.count(), 0)

        paycheck = PayCheck.objects.create(**data)

        self.assertEqual(PayCheck.objects.count(), 1)

        employee.delete()
        self.assertEqual(Employee.objects.count(), 0)
        self.assertEqual(PayCheck.objects.count(), 1)


    ###################
    # Daily Time Card #
    ###################
    def test_create_daily_time_card(self):
        employee = Employee.objects.create(
            emplId=0,
            name="test name 0",
            contact="test contact 0"
            )

        paycheck_data = {
            "id": 1,
            "startDate": datetime.date(2020, 6, 1),
            "endDate": datetime.date(2020, 6, 30),
            "total": 520.31
        }

        paycheck = PayCheck.objects.create(**paycheck_data)

        time_card_data = {
            "emplId": employee,
            "date": datetime.date(2020, 6, 1),
            "hours": 8.0,
            "rate": 12.50,
            "payCheck": paycheck
        }

        self.assertEqual(DailyTimeCard.objects.count(), 0)

        time_card = DailyTimeCard.objects.create(**time_card_data)

        self.assertEqual(DailyTimeCard.objects.count(), 1)

        self.assertEqual(time_card.emplId, time_card_data["emplId"])
        self.assertEqual(time_card.date, time_card_data["date"])
        self.assertEqual(time_card.hours, time_card_data["hours"])
        self.assertEqual(time_card.rate, time_card_data["rate"])


    def test_fail_create_daily_time_card_no_paycheck(self):
        employee = Employee.objects.create(
            emplId=0,
            name="test name 0",
            contact="test contact 0"
        )

        time_card_data = {
            "emplId": employee,
            "date": datetime.date(2020, 6, 1),
            "hours": 8.0,
            "rate": 12.50,
            "payCheck": ""
        }

        self.assertRaises(
            ValueError,
            lambda: DailyTimeCard.objects.create(**time_card_data)
        )


    def test_delete_paycheck_cascade_daily_time_card(self):
        employee = Employee.objects.create(
            emplId=0,
            name="test name 0",
            contact="test contact 0"
        )

        time_card_data = {
            "emplId": employee,
            "date": datetime.date(2020, 6, 1),
            "hours": 8.0,
            "rate": 12.50
        }

        paycheck_data = {
            "id": 0,
            "startDate": datetime.date(2020, 6, 1),
            "endDate": datetime.date(2020, 6, 30),
            "total": 520.31
        }

        self.assertEqual(DailyTimeCard.objects.count(), 0)

        paycheck = PayCheck.objects.create(**paycheck_data)
        time_card = DailyTimeCard.objects.create(**time_card_data)

        self.assertEqual(DailyTimeCard.objects.count(), 1)

        paycheck.delete()
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(PayCheck.objects.count(), 0)
        self.assertEqual(DailyTimeCard.objects.count(), 0)



    def test_delete_employee_doesnt_cascade_daily_time_card(self):
        employee = Employee.objects.create(
            emplId=0,
            name="test name 0",
            contact="test contact 0"
        )

        time_card_data = {
            "emplId": employee,
            "date": datetime.date(2020, 6, 1),
            "hours": 8.0,
            "rate": 12.50
        }

        paycheck_data = {
            "id": 0,
            "startDate": datetime.date(2020, 6, 1),
            "endDate": datetime.date(2020, 6, 30),
            "total": 520.31
        }

        self.assertEqual(DailyTimeCard.objects.count(), 0)

        paycheck = PayCheck.objects.create(**paycheck_data)
        time_card = DailyTimeCard.objects.create(**time_card_data)

        self.assertEqual(DailyTimeCard.objects.count(), 1)

        employee.delete()
        self.assertEqual(Employee.objects.count(), 0)
        self.assertEqual(DailyTimeCard.objects.count(), 1)
        self.assertEqual(PayCheck.objects.count(), 1)


    #####################
    # Employment Record #
    #####################
    def test_create_employment_record(self):
        employee = Employee.objects.create(
            emplId=0,
            name="test name 0",
            contact="test contact 0"
        )

        data = {
            "emplId": employee,
            "startDate": datetime.date(2020, 6, 1),
            "endDate": datetime.date(2020, 6, 30),
            "position": "E",
            "role": "cashier"
        }

        location = Location.objects.create(
            id=0,
            name="test location 0"
        )

        self.assertEqual(EmploymentRecord.objects.count(), 0)

        record = EmploymentRecord.objects.create(**data)

        self.assertEqual(EmploymentRecord.objects.count(), 1)

        self.assertEqual(record.emplId, data["emplId"])
        self.assertEqual(record.startDate, data["startDate"])
        self.assertEqual(record.endDate, data["endDate"])
        self.assertEqual(record.position, data["position"])
        self.assertEqual(record.role, data["role"])


    def test_create_employment_record_no_role(self):
        employee = Employee.objects.create(
            emplId=0,
            name="test name 0",
            contact="test contact 0"
        )

        data = {
            "emplId": employee,
            "startDate": datetime.date(2020, 6, 1),
            "endDate": datetime.date(2020, 6, 30),
            "position": "M"
        }

        location = Location.objects.create(
            id=0,
            name="test location 0"
        )

        self.assertEqual(EmploymentRecord.objects.count(), 0)

        record = EmploymentRecord.objects.create(**data)

        self.assertEqual(EmploymentRecord.objects.count(), 1)

        self.assertEqual(record.emplId, data["emplId"])
        self.assertEqual(record.startDate, data["startDate"])
        self.assertEqual(record.endDate, data["endDate"])
        self.assertEqual(record.position, data["position"])
        self.assertEqual(record.role, "unassigned")


    def test_delete_employee_doesnt_cascade_employment_record(self):
        employee = Employee.objects.create(
            emplId=0,
            name="test name 0",
            contact="test contact 0"
        )

        data = {
            "emplId": employee,
            "startDate": datetime.date(2020, 6, 1),
            "endDate": datetime.date(2020, 6, 30),
            "position": "M"
        }

        location = Location.objects.create(
            id=0,
            name="test location 0"
        )

        self.assertEqual(EmploymentRecord.objects.count(), 0)

        record = EmploymentRecord.objects.create(**data)

        self.assertEqual(EmploymentRecord.objects.count(), 1)

        employee.delete()

        self.assertEqual(Employee.objects.count(), 0)
        self.assertEqual(EmploymentRecord.objects.count(), 1)


    def test_create_employment_record_no_location(self):
        employee = Employee.objects.create(
            emplId=0,
            name="test name 0",
            contact="test contact 0"
        )

        data = {
            "emplId": employee,
            "startDate": datetime.date(2020, 6, 1),
            "endDate": datetime.date(2020, 6, 30),
            "position": "M",
            "location": ""
        }

        self.assertEqual(EmploymentRecord.objects.count(), 0)

        self.assertRaises(
            ValueError,
            lambda: EmploymentRecord.objects.create(**data)
        )