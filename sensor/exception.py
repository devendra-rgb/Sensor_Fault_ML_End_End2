
import sys
 
def exception_detail(error,error_detail:sys):

    _,_,exc_tb=error_detail.exc_info()
    
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_num = exc_tb.tb_lineno

    error_message="Error occured in python script  file name [{0}] line numer [{1}] error message [{2}]".format(file_name,line_num,str(error))
    
    return error_message





class SensorException(Exception):
    def __init__(self,error_message,error_detail:sys):

        super().__init__(error_message)

        self.error_message = exception_detail(error_message,error_detail=error_detail)

    def __str__(self) :
        return self.error_message