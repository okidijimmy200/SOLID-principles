class ParserMeta(type):
    def __instancecheck__(cls, __instance):
        return cls.__subclasscheck__(type(__instance))

    def __subclasscheck__(cls, __subclass):
        return (hasattr(__subclass, 'load_data_source') and
                        callable(__subclass.load_data_source) and
                        hasattr(__subclass, 'extract_text') and
                        callable(__subclass.extract_text))

class UpdatedInformalParserInterface(metaclass=ParserMeta):
    pass

class PdfParser:
    '''extract text from PDF'''
    def load_data_source(self, str, file_path_name: str) -> str:
        '''overrides InformalParserInterface.load_data_source()'''
        pass

    def extract_text(self, full_file_name: str) -> dict:
        '''overrides InformalParserInterface.extract_text()'''
        pass

class EmlParser:
    '''extract text from Email'''
    def load_data_source(self, str, file_path_name: str) -> str:
        '''overrides InformalParserInterface.load_data_source()'''
        pass

    def extract_text_from_email(self, full_file_name: str) -> dict:
        '''doesnot override InformalParserInterface.extract_text()'''
        pass


print(issubclass(PdfParser, UpdatedInformalParserInterface))

print(issubclass(EmlParser, UpdatedInformalParserInterface))

print(PdfParser.__mro__)

# print(EmlParser.__mro__)