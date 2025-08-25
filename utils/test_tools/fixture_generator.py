import json
from faker import Faker as __Faker
from faker.providers import DynamicProvider as __DynamicProvider


__faker = __Faker()

class __MyStr(str):
    __args = dict()
    
    def set_args(self, args):
        self.__args = args
    
    @property
    def args(self):
        return self.__args
    

def parametered_fake(fake_type, **args):
    fake_type = __MyStr(fake_type)
    fake_type.set_args(args)
    return fake_type


def __generate_json(count, structure):
    final_list = list()
    cached_providers = dict()
    errored_providers = set()
    
    for _ in range(count):
        result = dict()
        for key, properties in structure.items():
            args = dict()
            if type(properties).__name__ == 'list':
                try:
                    provider = cached_providers[key]
                except:
                    candidate_elements = properties
                    provider = __DynamicProvider(
                        provider_name=key,
                        elements=candidate_elements
                    )
                    cached_providers[key] = provider
                __faker.add_provider(provider)
                fake_data_generator_func = getattr(__faker, key)
                result[key] = fake_data_generator_func()
            else:
                data_type = properties
                try:
                    fake_data_generator_func = getattr(__faker, data_type)
                    if hasattr(properties, 'args'):
                        args = properties.args
                    result[key] = fake_data_generator_func(**args)
                except:
                    message = f'WARNING: The data_type "{key}":"{data_type}" in properties not supported by faker'
                    errored_providers.add(message)
                
        final_list.append(result)
    
    for message in errored_providers:
        print(message)
    
    return final_list


def make_fixture_file(data_properties, data_count, fixture_address, file_name, pipeline_functions=None, reusable_data_keys=None):
    data = __generate_json(count=data_count, structure=data_properties)
    
    if pipeline_functions is not None:
        try:
            for function in pipeline_functions:
                data = function(data)
        except:
            print(f'pipeline function: "{function.__name__}" raised error:')
            raise
    
    json_string = json.dumps(data, indent=4)
    json_file_address = f'{fixture_address}/{file_name}'
    json_file = open(json_file_address, "w")
    json_file.write(json_string)
    json_file.close()
    
    print(f'JSON file created: {json_file_address}')
    
    all_keys = list(data[0].keys())
    if reusable_data_keys is not None:
        for key in all_keys:
            if key not in reusable_data_keys:
                for item in data:
                    if key in item.keys():
                        item.__delitem__(key)
    
        return data
