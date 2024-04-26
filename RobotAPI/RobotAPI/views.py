import os
import tempfile

from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from robot.api import TestSuiteBuilder
from django.http import HttpResponse
from robot.model import TestSuite, TestCase, Keyword


def index(request):
    return HttpResponse("Welcome to the root URL.")


def create_robot_file(data, file_path):
    with open(file_path, 'w') as file:
        file.write("*** Settings ***\n")
        file.write("Library    SeleniumLibrary\n\n")
        file.write("*** Test Cases ***\n")
        for test in data['tests']:
            title = test['title']
            steps = test['steps']
            file.write(f"{title}\n")

            # Add WebDriver initialization step
            file.write(f"    Open Browser    url=about:blank    browser=chrome\n")
            for step in steps:
                file.write(f"    {step}\n")
    return file_path

@csrf_exempt
def execute_tests(request):
    path = "test_case.robot"
    # Ensure the request method is POST
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

    # Ensure the request content type is JSON
    if request.content_type != 'application/json':
        return JsonResponse({'error': 'Content-Type must be application/json'}, status=400)

    try:
        # Load JSON data from the request body
        data = json.loads(request.body)
        tests = data.get('tests', [])

        # Checking data contents
        #print(data)

        robo_file_path = create_robot_file(data, path)

        # Create a new test suite
        builder = TestSuiteBuilder()
        suite = builder.build(robo_file_path)

        # Run the test suite
        result = suite.run(output=None)

        # Get the result of the test suite
        test_suite_result = result.return_code

        # Create a list to store individual test results
        test_results = []

        # Iterate through each test and store the individual test results
        for test in tests:
            title = test['title']
            test_case_result = result.return_code
            test_results.append({'title': title, 'result': test_case_result})

        # Return the test results
        return JsonResponse({'message': 'Tests executed successfully', 'results': test_results})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON Payload'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)

    finally:
        os.remove(path)
        #print("Robo file removed Successfully")