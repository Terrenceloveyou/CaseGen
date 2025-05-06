import json

class SwaggerParser:
    def __init__(self, swagger_file):
        with open(swagger_file, 'r') as file:
            self.parser = json.load(file)
        self.paths = self.parser.get('paths', {})
        self.definitions = self.parser.get('definitions', {})

    def api_list(self):
        api_list = []
        for path, methods in self.paths.items():
            for method, details in methods.items():
                api_info = {
                    'path': path,
                    'method': method,
                    'req': self.process_parameters(details.get('parameters', [])),
                    'resp': self.process_responses(details.get('responses', {}))
                }
                api_list.append(api_info)


        return api_list
    
    def process_parameters(self, parameters):
        processed_params = []
        for param in parameters:
            schema = param.get('schema')
            if schema:
                ref = schema.get('$ref')
                if ref:
                    schema_name = ref.split('/')[-1]
                    param['schema'] = self.definitions.get(schema_name, {})
            processed_params.append(param)
        return processed_params
    
    def process_responses(self, responses):
        processed_responses = {}
        for status_code, response_detail in responses.items():
            schema = response_detail.get('schema')
            if schema:
                ref = schema.get('$ref')
                if ref:
                    schema_name = ref.split('/')[-1]
                    response_detail['schema'] = self.definitions.get(schema_name, {})
            processed_responses[status_code] = response_detail
        return processed_responses

if __name__ == "__main__":
    swagger_file =  "C:\\Users\\HP1\\Desktop\\paper\\vulnerable-petstore\\petstore.json"
    parser = SwaggerParser(swagger_file)
    api_list = parser.api_list()
    print(json.dumps(api_list, indent=2))