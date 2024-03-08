import json
import re

PYTHON_RUNNER = """# declare main function here
{{code}}

# execute main function, and return the result
# inputs is a dict, and it
output = main(**{{inputs}})

# convert output to json and print
result = '''
<<RESULT>>
{output}
<<RESULT>>
'''

print(result)
"""


class PythonTemplateTransformer:
    @classmethod
    def transform_caller(cls, code: str, inputs: dict) -> str:
        """
        Transform code to python runner
        :param code: code
        :param inputs: inputs
        :return:
        """
        
        # transform inputs to json string
        inputs_str = json.dumps(inputs, indent=4)

        # replace code and inputs
        runner = PYTHON_RUNNER.replace('{{code}}', code)
        runner = runner.replace('{{inputs}}', inputs_str)

        return runner
    
    @classmethod
    def transform_response(cls, response: str) -> dict:
        """
        Transform response to dict
        :param response: response
        :return:
        """
        
        # extract result
        result = re.search(r'<<RESULT>>(.*)<<RESULT>>', response, re.DOTALL)
        if not result:
            raise ValueError('Failed to parse result')
        
        result = result.group(1)
        return json.loads(result)