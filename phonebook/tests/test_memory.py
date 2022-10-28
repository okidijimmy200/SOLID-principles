from memory import MemorySystem
import json



def test_create(helpers):
    tfile = helpers.input_variables()
    data = {"id": 1, "name": 'test', "phone": '0788926712.json'}
    test_cases = [
        {
            "name": "pass",
            "input-1": 'True',
            "input-2": f"{str(tfile.name)}.test.json",
            "output": f"Data created successfully in location {str(tfile.name)}.test.json"
        },
        {
            "name": "fail",
            "input-1": 'True',
            "input-2": "test/test.json",
            "output": "Failed to create data in location test/test.json"
        }
    ]
    for test_case in test_cases:
            # why do we have 3 args with self included as an arg
        k, result = MemorySystem.create(test_case["input-1"],test_case["input-2"], data)
        # to check if data is loaded from file
        # f = open(f'{str(tfile.name)}.test.json')
        # data = json.load(f)
        # print(data)
        assert result == test_case["output"]


def test_read(helpers):
    tfile = helpers.input_variables()
    test_cases = [
        {
            "name": "pass",
            "input-1": 'True',
            "input-2": f"{str(tfile.name)}.test.json",
            "output": f"Data read from {str(tfile.name)}.test.json"
        },
        {
            "name": "fail",
            "input-1": 'True',
            "input-2": "test/test.json",
            "output": "Failed to read data from location test/test.json"
        }
    ]
    for test_case in test_cases:
        # why do we have 3 args with self included as an arg
        MemorySystem.create(test_case["input-1"],test_case["input-2"], {"id": 1, "name": 'test', "phone": '0788926712.json'})
        k, result, data = MemorySystem.read(test_case["input-1"],test_case["input-2"])
        assert result == test_case["output"]

def test_update(helpers):
    tfile = helpers.input_variables()
    name_2 = 'jimmyjones'
    test_cases = [
        {
            "name": "pass",
            "input-1": 'True',
            "input-2": f"{str(tfile.name)}.test.json",
            "output": (True, "Data updated successfully in location")
        },
        {
            "name": "fail",
            "input-1": 'True',
            "input-2": "test/test.json",
            "output": (False, "Unexpected err=FileNotFoundError(2, 'No such file or directory'), type(err)=<class 'FileNotFoundError'>")
        }
    ]
    for test_case in test_cases:
        MemorySystem.create(test_case["input-1"],test_case["input-2"], {"id": 1, "name": 'test', "phone": '0788926712.json'})
        k, reason, data = MemorySystem.update(test_case["input-1"], test_case["input-2"], {"id": 1, "name": name_2, "phone": '0788926712.json'})
        assert (k, reason) == test_case["output"]

def test_delete(helpers):
    tfile = helpers.input_variables()
    test_cases = [
        {
            "name": "pass",
            "input-1": 'True',
            "input-2": f"{str(tfile.name)}.test.json",
            "output": f"JSON {str(tfile.name)}.test.json removed"
        },
        {
            "name": "fail",
            "input-1": 'True',
            "input-2": "test/test.json",
            "output": "File doesnot exist"
        }
    ]
    for test_case in test_cases:
        MemorySystem.create(test_case["input-1"],test_case["input-2"], {"id": 1, "name": 'test', "phone": '0788926712.json'})
        k, reason = MemorySystem.delete(test_case["input-1"],test_case["input-2"])
        assert reason == test_case["output"]


