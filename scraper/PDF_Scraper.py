from PyPDF2 import PdfFileReader

class PdfParser:
    def __init__(self, file_name):
        self.file_name=file_name
        
    def parse(self):
        record_list=[]
        with open('202010297.pdf', 'rb') as f:
            pdf = PdfFileReader(f)
            for page_number in range(pdf.numPages):
            text = pdf.getPage(page_number).extractText()
            if 'VEHICLE IDENTIFICATION #' in text:
                record_list.append(
                    self.get_unit_record(text)
                )
        return record_list

    def get_unit_record(self, text):
        record={}
        record['vehicle']={}
        record['insurance']={}
        owner={}
        address={}
        lines=list(filter(str.strip,text.splitlines()))
        for line_no in range(0,len(lines)):
            line_text=lines[line_no].strip()
            # print(line_text)
            if    line_text=='OWNER NAME:':                 owner['last'],owner['first'],owner['mid'] = lines[line_no+3].split(', ')
            elif  line_text=='OWNER ADDRESS:':              address['street'],address['city'],address['state'],address['zip'] = lines[line_no+3].split(', ')
            elif  line_text=='UNIT #':                      record['unit']                       = lines[line_no+1]
            elif  line_text=='VEHICLE IDENTIFICATION #':    record['vehicle']['Vehicle ID']      = lines[line_no+1]
            elif  line_text=='INSURANCE POLICY #':          record['insurance']['no #']          = lines[line_no+1]
            elif  line_text=='COLOR':                       record['vehicle']['Color']           = lines[line_no+1]
            elif  line_text=='INSURANCE COMPANY':           record['insurance']['company']       = lines[line_no+1]
            elif  line_text=='VEHICLE MAKE':                record['vehicle']['Make']            = lines[line_no+1]
            elif  line_text=='VEHICLE MODEL':               record['vehicle']['model']           = lines[line_no+1]
            elif  line_text=='LICENSE PLATE #':             record['vehicle']['License Plate #'] = lines[line_no+1]
            record['Owner']={}
            record['Owner']['Name']=owner
            record['Owner']['Address']=address
        return record