import requests #REST Access to FHIR Server
print('Search patient by name, name + birthdate, or name + gender')
print('How would you like to search for a patient? Enter 1, 2 or 3')
option = input('Enter 1 -to search by name, 2 -to search by name and birthdate, 3 -to search by name and gender-:')
while not(option == '1' or option == '2' or option == '3'):
  print('Invalid option. Please enter 1, 2, or 3')
  option = input('Enter 1 -to search by name, 2 -to search by name and birthdate, 3 -to search by name and gender-:')
  
name = input("Enter patient's name -try Salcedo309 :")
birthdate = ''
gender = ''
# given=input('Given Name -try Catalina187-:')
# family=input('Family Name -try Nunez242-:')
url = 'http://hapi.fhir.org/baseR4/Patient?_profile=http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient&name='+name
if option == '2':
  birthdate = input('Enter birthdate -try 1946-01-08 :')
  url += '&birthdate='+birthdate
  print('Searching for Patient by name+birthdate...@'+url)
elif option == '3':
  gender = input("Enter gender -try male :")
  url += '&gender='+gender
  print('Searching for Patient by name+gender...@'+url)
else:
  print('Searching for Patient by name...@'+url)
# url='http://fhir.hl7fundamentals.org/r4/Patient?family='+family+'&given='+given

response = requests.get(url)
json_response = response.json()
#
#
#
try:
  key='entry'
  EntryArray=json_response[key]
  FirstEntry=EntryArray[0]
  key='resource'
  resource=FirstEntry['resource']
  id=resource['id']
  PatientServerId= id
  patientName = resource['name'][0]['given'][0] + ' ' +resource['name'][0]['family']
  print('Patient Found')
  print('Patient Id @ endpoint:'+id)
#
# Searching for Vital Signs
  url='http://hapi.fhir.org/baseR4/Observation?patient='+id 

# url='http://fhir.hl7fundamentals.org/r4/Procedure?patient='+id

  print('Now Searching for Vital Signs...@'+url)
  vital_response = requests.get(url).json()
  key='entry'
  EntryArray=vital_response[key]
  print (f'Vital sign(s) found for the patient {patientName}')
  for entry in EntryArray:
    vital=entry['resource']
    print('-------------------------')
    ISODate=vital['effectiveDateTime']
    print ('date: '+ISODate)
    print ('status: '+vital['status'])
    print ('observation type: '+vital['category'][0]['coding'][0]['code'])
    loincCode = vital['code']['coding'][0]['code']
    loincText = vital['code']['text']
    print(f'description: {loincText} ({loincCode})')
    value = vital['valueQuantity'] if 'valueQuantity' in vital else ''
    absentReason = vital['dataAbsentReason'] if 'dataAbsentReason' in vital else ''
    if value:
      print('observed value: '+str(value['value']) + ' ' +value['unit'])
    elif absentReason:
      print('reason for absent result: '+absentReason['text'])
    
    component = vital['component'] if 'component' in vital else []
    if component:
      for entry in component:
        coding = entry['code']['coding'][0]
        code = coding['code']
        text = coding['display']
        value = entry['valueQuantity']['value']
        unit = entry['valueQuantity']['unit']
        print(f'{text} ({code}): {value} {unit}')
except Exception as e:
  print ('Patient/Observation Not Found '+e)
   