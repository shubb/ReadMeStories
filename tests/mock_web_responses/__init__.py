import os

dir_path = os.path.dirname(os.path.realpath(__file__))
response_dir = os.path.join(dir_path, 'responses')

def GetMockResponse(mock_response_filename):
    with open(os.path.join(response_dir, mock_response_filename), 'r') as mock_response:
        return mock_response.read()