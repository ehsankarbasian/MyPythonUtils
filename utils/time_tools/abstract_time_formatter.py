from abc import ABC, abstractmethod

# No need to modify this file


class AbstractTimeFormatter(ABC):
    
    def format_duration(self, duration, _format, exactness):
        self.__exactness_diff = exactness
        converted_duration = self.convert_duration(duration, _format)
        normal_duration = self.__normalize_duration(converted_duration)
        exacted_duration = self.__make_exacted_duration(normal_duration, exactness)
        normal_exacted_duration = self.__normalize_duration(exacted_duration)
        return normal_exacted_duration

    def __normalize_duration(self, duration):
        duration = str(duration)
        if 'e' in duration:
            power = int(duration.split('-')[1])
            amount = str(duration.split('-')[0][:-1]).replace('.', '')
            result = f'0.{"0"*(power-1)}{amount}'
            return result
        else:
            return duration

    def __make_exacted_duration(self, duration, exactness):
        if float(duration) - int(float(duration)) == 0:
            return duration
        return self.__get_non_zero_exacted_duration(duration, exactness)
    
    def __get_non_zero_exacted_duration(self, duration, exactness):
        exacted_duration = '.'.join([str(int(float(duration))),
                                    str(duration).split('.')[1][:exactness]])
        if float(exacted_duration) == 0:
            exactness += self.__exactness_diff
            return self.__get_non_zero_exacted_duration(duration, exactness)
        return exacted_duration
    
    @property
    def format(self):
        return self.__format
    
    def set_format(self, _format):
        self.__format = _format
    
    
    @abstractmethod
    def convert_duration(self, duration, _format):
        # Implement the function as the example below:
        
        # if _format == 'second':
        #         return duration
        # elif _format == 'millisecond':
        #     return duration * 10**3
        # elif _format == 'microsecond':
        #     return duration * 10**6
        # elif _format == 'minute':
        #     return duration / 60
        # elif _format == 'hour':
        #     return duration / 60**2
        # else:
        #     self.set_format('millisecond')
        #     return duration * 10**3
        
        pass
