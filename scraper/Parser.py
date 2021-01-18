from util.db import DatabaseManager
class Parser:
    def __init__(self):
        self.db=DatabaseManager()
    
    def get_verification_token(self, pageParser):
        return pageParser\
            .find('form',{'id':'Search'})\
            .find('input',{'name':'__RequestVerificationToken'})['value']

    def is_next_button_exists(self, pageParser):
        return pageParser.find('li',{'aria-label':'Next page'}) is not None

    def parse_result(self, pageParser, county_name):
        # TODO report error here with Sentry
        if pageParser.find('h2',{'aria-label':'Error Message'}) is not None:
            print(error.text)
        
        # TODO Report an error here with Sentry
        if pageParser.h1.text != "Crash Results":
            print('[x] There is an error occured')
            raise ValueError

        results=pageParser.find('table',{'id':'mySearchTable'}).findAll('tr', 'selectable')

        for row in results:
            fields = row.findAll('td')[1:]
            result = [field.text.strip() for field in fields]

            # Map all of the Fields data with with headers and make them a dictoinary
            record = dict(
                        zip(
                            ['Crash Number', 'Crash Date', 'Add Date', 'Location', 'Agency', 'Jurisdiction', 'Crash Severity', 'Document Number'],
                            result
                        )
                    )
            
            # Convert all of the string dates in datetime stamp for accessibility in database searching
            record['Scraped_date']=  datetime.now()
            record['Add Date']   = datetime.strptime( record['Add Date']  , '%m/%d/%Y')
            record['Crash Date'] = datetime.strptime( record['Crash Date'], '%m/%d/%Y')

            record['County'] = county_name
            
            # If record already exists - Don't save that in data
            if self.db.ifIndexExists(record['Crash Number']) : 
                return

            print(record)
            
            # TODO Send an email from here
            # TODO Sentry record it
            # Record is new will be added in Database and message will be sent.
            self.db.insert_record(record)